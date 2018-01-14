from dashboard.models import RawData
import time
from datetime import datetime

float1 = 1
float2 = 2.5
for item in range(1000):
    float1 += 0.5
    float2 += 1
    data = RawData(id=item, co=float1, oxi=float2, measuring_date=datetime.now())
    data.save()
    time.sleep(1)

