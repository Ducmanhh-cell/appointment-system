import os
from datetime import time, timedelta
os.environ.setdefault("DJANGO_SETTINGS_MODULE","config.settings")
import django
django.setup()
from django.utils import timezone
from appointments.models import Service, TimeSlot
data=[
 ("Tư vấn tổng quát","Tư vấn ban đầu và giải đáp nhu cầu.",30,150000),
 ("Tư vấn chuyên sâu","Buổi tư vấn chi tiết theo lịch hẹn.",60,300000),
 ("Hỗ trợ kỹ thuật","Kiểm tra và hỗ trợ vấn đề kỹ thuật.",45,200000),
]
services=[]
for name,description,duration,price in data:
 obj,_=Service.objects.update_or_create(name=name,defaults={"description":description,"duration_minutes":duration,"price":price,"is_active":True})
 services.append(obj)
times=[(time(9,0),time(9,30)),(time(10,0),time(10,30)),(time(14,0),time(14,30)),(time(15,0),time(15,30))]
created=0
for service in services:
 for offset in range(1,8):
  day=timezone.localdate()+timedelta(days=offset)
  for start,end in times:
   _,made=TimeSlot.objects.get_or_create(service=service,date=day,start_time=start,end_time=end,defaults={"is_active":True})
   created+=made
print(f"Seed complete: {len(services)} services processed; {created} new slots created.")
