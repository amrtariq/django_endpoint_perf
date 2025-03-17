import time
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.db import connection
from django.db.models.base import ModelBase
from django.apps import apps
from .models import Serial
from .serializers import SerialSerializer
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor
from math import ceil
from functools import partial
import os
import django
from queue import Queue
from threading import Event
from django.http import StreamingHttpResponse
import json
import gzip
import base64

# Initialize Django for worker processes
def initialize_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class SerialViewSet(viewsets.ModelViewSet):
    queryset = Serial.objects.all()
    serializer_class = SerialSerializer
    pagination_class = CustomPagination
    
    def list(self, request, *args, **kwargs):
        try:
            start_time = time.time()
            response = super().list(request, *args, **kwargs)
            end_time = time.time()
            
            if isinstance(response.data, dict):
                response.data['metadata'] = {
                    'query_time': end_time - start_time,
                    'query_count': len(connection.queries)
                }
            return response
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
def get_serials_values(request):
    try:
        start_time = time.time()
        
        # Using values() with specific fields and force evaluation
        queryset = list(Serial.objects.all().values(
            'id', 'serial', 'sscc', 'sscc_2', 'sscc_3', 'sscc_4',
            'serial_time', 'gtin', 'batch', 'sub_batch', 'mfg_date',
            'exp_date', 'usable', 'serial_machine', 'print_status',
            'print_time', 'print_machine', 'serial_status', 'verify_status',
            'verify_time', 'verify_machine', 'verify_status_1',
            'verify_status_1_time', 'verify_status_2', 'verify_status_2_time',
            'verify_status_3', 'verify_status_3_time', 'verify_status_4',
            'verify_status_4_time', 'verify_status_5'
        ))
        
        # Compress data
        json_data = json.dumps(queryset).encode('utf-8')
        compressed_data = gzip.compress(json_data)
        compressed_b64 = base64.b64encode(compressed_data).decode('utf-8')
        
        end_time = time.time()
        
        return Response({
            'data': compressed_b64,
            'compressed': True,
            'metadata': {
                'total_records': len(queryset),
                'query_time': end_time - start_time,
                'query_count': len(connection.queries)
            }
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_serials_row(request):
    try:
        start_time = time.time()
        
        # Force queryset evaluation
        queryset = list(Serial.objects.all())  # Force immediate database query
        
        # Force serialization
        serializer = SerialSerializer(queryset, many=True)
        data = serializer.data  # Force serializer evaluation
        
        end_time = time.time()
        
        return Response({
            #'data': data,
            'metadata': {
                'total_records': len(queryset),
                'query_time': end_time - start_time,
                'query_count': len(connection.queries)
            }
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_serials_paginated(request):
    try:
        start_time = time.time()
        chunk_size = min(int(request.GET.get('chunk_size', 1000)), 5000)
        
        def generate_chunks():
            queryset = Serial.objects.all().values(
                'id', 'serial', 'sscc', 'sscc_2', 'sscc_3', 'sscc_4',
                'serial_time', 'gtin', 'batch', 'sub_batch', 'mfg_date',
                'exp_date', 'usable', 'serial_machine', 'print_status',
                'print_time', 'print_machine', 'serial_status', 'verify_status',
                'verify_time', 'verify_machine', 'verify_status_1',
                'verify_status_1_time', 'verify_status_2', 'verify_status_2_time',
                'verify_status_3', 'verify_status_3_time', 'verify_status_4',
                'verify_status_4_time', 'verify_status_5'
            )
            total_records = queryset.count()
            processed_records = 0
            
            while processed_records < total_records:
                chunk = list(queryset[processed_records:processed_records + chunk_size])
                
                # Create chunk metadata
                chunk_info = {
                    'chunk_number': processed_records // chunk_size + 1,
                    'records_in_chunk': len(chunk),
                    'total_records': total_records,
                    'data': chunk
                }
                
                yield f"data: {json.dumps(chunk_info)}\n\n"
                processed_records += chunk_size
            
            # Send final metadata
            end_time = time.time()
            final_metadata = {
                'complete': True,
                'total_records': total_records,
                'total_time': end_time - start_time,
                'query_count': len(connection.queries)
            }
            yield f"data: {json.dumps(final_metadata)}\n\n"
        
        response = StreamingHttpResponse(
            generate_chunks(),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response
        
    except ValueError as ve:
        return Response(
            {'error': 'Invalid parameters'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_serials_threaded(request):
    try:
        # Start timing
        start_time = time.time()
        
        # Get total records for chunking
        total_records = Serial.objects.count()
        
        # Configure thread pools and chunk sizes
        fetch_workers = cpu_count()
        process_workers = (cpu_count() * 2)
        chunk_size = 1000
        
        # Create thread-safe queue and completion event
        data_queue = Queue(maxsize=fetch_workers * 2)
        completion_event = Event()
        
        # Track metrics
        chunk_times = []
        combined_data = []
        
        def fetch_chunk(offset):
            try:
                chunk_start = time.time()
                # Fetch chunk from database
                chunk = list(Serial.objects.all()[offset:offset + chunk_size])
                chunk_end = time.time()
                
                if chunk:
                    data_queue.put({
                        'chunk_id': offset // chunk_size,
                        'data': chunk,
                        'fetch_time': chunk_end - chunk_start,
                        'records': len(chunk)
                    })
                return True
            except Exception as e:
                data_queue.put({
                    'chunk_id': offset // chunk_size,
                    'error': str(e)
                })
                return False
        
        def process_chunks():
            while not completion_event.is_set() or not data_queue.empty():
                try:
                    chunk_data = data_queue.get(timeout=1)
                    if 'error' in chunk_data:
                        chunk_times.append({
                            'chunk': chunk_data['chunk_id'],
                            'time': 0,
                            'error': chunk_data['error']
                        })
                        continue
                    
                    # Process and serialize the chunk
                    process_start = time.time()
                    serializer = SerialSerializer(chunk_data['data'], many=True)
                    process_end = time.time()
                    
                    # Calculate total chunk time
                    total_chunk_time = chunk_data['fetch_time'] + (process_end - process_start)
                    
                    # Store results
                    combined_data.extend(serializer.data)
                    chunk_times.append({
                        'chunk': chunk_data['chunk_id'],
                        'time': total_chunk_time,
                        'records': chunk_data['records']
                    })
                except Exception as e:
                    # Handle timeout and other errors
                    if not completion_event.is_set():
                        continue
                    break
        
        # Start processor threads
        with ThreadPoolExecutor(max_workers=process_workers) as process_executor:
            # Start processor threads
            processor_futures = [process_executor.submit(process_chunks) 
                               for _ in range(process_workers)]
            
            # Start fetcher threads
            with ThreadPoolExecutor(max_workers=fetch_workers) as fetch_executor:
                offset = 0
                fetch_futures = []
                
                while offset < total_records:
                    future = fetch_executor.submit(fetch_chunk, offset)
                    fetch_futures.append(future)
                    offset += chunk_size
                
                # Wait for all fetch operations to complete
                for future in fetch_futures:
                    future.result()
                
                # Signal completion to processor threads
                completion_event.set()
            
            # Wait for all processor threads to complete
            for future in processor_futures:
                future.result()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        return Response({
            #'data': combined_data,
            'metadata': {
                'total_records': total_records,
                'total_time': total_time,
                'chunk_times': chunk_times,
                'workers_used': process_workers,
                'chunk_size': chunk_size,
                'query_count': len(connection.queries)
            }
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )