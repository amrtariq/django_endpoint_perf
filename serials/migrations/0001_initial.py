# Generated by Django 4.2.2 on 2025-03-17 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Serial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=45)),
                ('code_1', models.CharField(max_length=45)),
                ('code_2', models.CharField(max_length=45)),
                ('code_3', models.CharField(max_length=45)),
                ('code_4', models.CharField(max_length=45)),
                ('timestamp_1', models.CharField(max_length=45)),
                ('product_code', models.CharField(max_length=45)),
                ('lot_number', models.CharField(max_length=45)),
                ('lot_subset', models.CharField(max_length=45)),
                ('date_1', models.CharField(max_length=45)),
                ('date_2', models.CharField(max_length=45)),
                ('status_1', models.CharField(max_length=45)),
                ('device_1', models.CharField(max_length=45)),
                ('status_2', models.CharField(max_length=45)),
                ('timestamp_2', models.CharField(max_length=45)),
                ('device_2', models.CharField(max_length=45)),
                ('status_3', models.CharField(max_length=45)),
                ('status_4', models.CharField(max_length=45)),
                ('timestamp_3', models.CharField(max_length=45)),
                ('device_3', models.CharField(max_length=45)),
                ('status_5', models.CharField(max_length=45)),
                ('timestamp_4', models.CharField(max_length=45)),
                ('status_6', models.CharField(max_length=45)),
                ('timestamp_5', models.CharField(max_length=45)),
                ('status_7', models.CharField(max_length=45)),
                ('timestamp_6', models.CharField(max_length=45)),
                ('status_8', models.CharField(max_length=45)),
                ('timestamp_7', models.CharField(max_length=45)),
                ('status_9', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'serials',
                'indexes': [models.Index(fields=['identifier'], name='serials_identif_1b5f0d_idx'), models.Index(fields=['product_code'], name='serials_product_7f4a37_idx'), models.Index(fields=['lot_number'], name='serials_lot_num_40a745_idx')],
            },
        ),
    ]
