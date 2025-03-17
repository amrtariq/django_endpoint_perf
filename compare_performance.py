import requests
import time
import statistics
import json

def test_endpoint(url, num_requests=1):
    times = []
    records = 0
    total_query_count = 0
    
    print(f"\nTesting {url}...")
    
    for i in range(num_requests):
        start_time = time.time()
        
        # Handle SSE endpoint differently
        if 'paginated' in url:
            total_chunks = 0
            total_records = 0
            chunk_data = []  # Store chunk data
            
            with requests.get(url, stream=True) as response:
                for line in response.iter_lines():
                    if line:
                        # Remove "data: " prefix and parse JSON
                        data = json.loads(line.decode('utf-8').replace('data: ', ''))
                        if 'complete' in data:
                            # Final metadata received
                            request_time = data['total_time']
                            total_query_count += data['query_count']
                            times.append(request_time)
                            break
                        else:
                            # Process chunk data
                            total_chunks += 1
                            total_records += data['records_in_chunk']
                            chunk_data.extend(data['data'])  # Store the chunk data
            
            records = total_records
            print(f"Received {total_chunks} chunks with {total_records} total records")
            
        else:
            # Rest of the code remains unchanged
            response = requests.get(url)
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                metadata = data.get('metadata', {})
                
                request_time = metadata.get('query_time') or metadata.get('total_time') or (end_time - start_time)
                times.append(request_time)
                records = len(data.get('data', []))
                total_query_count += metadata.get('query_count', 0)
                
                if 'chunk_times' in metadata:
                    print(f"\nRequest {i+1} Details:")
                    print(f"Workers used: {metadata.get('processes_used') or metadata.get('workers_used')}")
                    print("Chunk processing times:")
                    for chunk in metadata['chunk_times']:
                        print(f"  Chunk {chunk['chunk']}: {chunk['time']:.4f}s ({chunk['records']} records)")
        
        print(f"Request {i+1}: {request_time:.4f} seconds")
    
    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    std_dev = statistics.stdev(times) if len(times) > 1 else 0
    
    return {
        'endpoint': url.split('/')[-2] or 'root',
        'average_time': avg_time,
        'min_time': min_time,
        'max_time': max_time,
        'std_dev': std_dev,
        'records': records,
        'avg_queries': total_query_count / num_requests
    }

def main():
    base_url = 'http://localhost:8000/api/'
    endpoints = [
        #f"{base_url}threaded/",
        f"{base_url}values/",
        #f"{base_url}row/",
        #f"{base_url}paginated/",
        
    ]
    
    results = []
    for endpoint in endpoints:
        try:
            result = test_endpoint(endpoint)
            results.append(result)
        except Exception as e:
            print(f"Error testing {endpoint}: {str(e)}")
    
    print("\nPerformance Comparison Summary:")
    print("-" * 80)
    print(f"{'Endpoint':<15} {'Avg Time':<12} {'Min Time':<12} {'Max Time':<12} {'Std Dev':<12} {'Records':<10} {'Avg Queries':<12}")
    print("-" * 80)
    
    for result in results:
        print(
            f"{result['endpoint']:<15} "
            f"{result['average_time']:<12.4f} "
            f"{result['min_time']:<12.4f} "
            f"{result['max_time']:<12.4f} "
            f"{result['std_dev']:<12.4f} "
            f"{result['records']:<10} "
            f"{result['avg_queries']:<12.2f}"
        )

if __name__ == '__main__':
    main()