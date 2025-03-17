import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.apps import apps
apps.check_apps_ready()

from serials.models import Serial

def generate_random_string(length=10):
    return ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))

def generate_date():
    start_date = datetime.now() - timedelta(days=365)
    random_days = random.randint(0, 730)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

def create_test_data(num_records=100000):
    batch_size = 10000
    records_created = 0

    while records_created < num_records:
        batch_records = []
        for _ in range(min(batch_size, num_records - records_created)):
            serial_record = Serial(
                identifier=generate_random_string(20),
                code_1=generate_random_string(18),
                code_2=generate_random_string(18),
                code_3=generate_random_string(18),
                code_4=generate_random_string(18),
                timestamp_1=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                product_code=generate_random_string(14),
                lot_number=generate_random_string(10),
                lot_subset=generate_random_string(5),
                date_1=generate_date(),
                date_2=generate_date(),
                status_1='1',
                device_1=f'Machine-{random.randint(1, 5)}',
                status_2='1',
                timestamp_2=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                device_2=f'Printer-{random.randint(1, 3)}',
                status_3='1',
                status_4='1',
                timestamp_3=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                device_3=f'Verifier-{random.randint(1, 4)}',
                status_5='1',
                timestamp_4=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                status_6='1',
                timestamp_5=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                status_7='1',
                timestamp_6=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                status_8='1',
                timestamp_7=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                status_9='1'
            )
            batch_records.append(serial_record)
        
        Serial.objects.bulk_create(batch_records)
        records_created += len(batch_records)
        print(f'Created {records_created} records')

if __name__ == '__main__':
    create_test_data()