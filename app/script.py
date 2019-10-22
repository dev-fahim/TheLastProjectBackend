import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.db.models import *
from bill.models import Bill, BillData

bill = Bill.objects.all().prefetch_related('bill_data')

for i in bill:
    print(i.discount)
