from django.db import models

class Serial(models.Model):
    identifier = models.CharField(max_length=45)  # was serial
    code_1 = models.CharField(max_length=45)      # was sscc
    code_2 = models.CharField(max_length=45)      # was sscc_2
    code_3 = models.CharField(max_length=45)      # was sscc_3
    code_4 = models.CharField(max_length=45)      # was sscc_4
    timestamp_1 = models.CharField(max_length=45)  # was serial_time
    product_code = models.CharField(max_length=45) # was gtin
    lot_number = models.CharField(max_length=45)   # was batch
    lot_subset = models.CharField(max_length=45)   # was sub_batch
    date_1 = models.CharField(max_length=45)       # was mfg_date
    date_2 = models.CharField(max_length=45)       # was exp_date
    status_1 = models.CharField(max_length=45)     # was usable
    device_1 = models.CharField(max_length=45)     # was serial_machine
    status_2 = models.CharField(max_length=45)     # was print_status
    timestamp_2 = models.CharField(max_length=45)  # was print_time
    device_2 = models.CharField(max_length=45)     # was print_machine
    status_3 = models.CharField(max_length=45)     # was serial_status
    status_4 = models.CharField(max_length=45)     # was verify_status
    timestamp_3 = models.CharField(max_length=45)  # was verify_time
    device_3 = models.CharField(max_length=45)     # was verify_machine
    status_5 = models.CharField(max_length=45)     # was verify_status_1
    timestamp_4 = models.CharField(max_length=45)  # was verify_status_1_time
    status_6 = models.CharField(max_length=45)     # was verify_status_2
    timestamp_5 = models.CharField(max_length=45)  # was verify_status_2_time
    status_7 = models.CharField(max_length=45)     # was verify_status_3
    timestamp_6 = models.CharField(max_length=45)  # was verify_status_3_time
    status_8 = models.CharField(max_length=45)     # was verify_status_4
    timestamp_7 = models.CharField(max_length=45)  # was verify_status_4_time
    status_9 = models.CharField(max_length=45)     # was verify_status_5

    class Meta:
        db_table = 'serials'
        indexes = [
            models.Index(fields=['identifier']),    # was serial
            models.Index(fields=['product_code']),  # was gtin
            models.Index(fields=['lot_number'])     # was batch
        ]