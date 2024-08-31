from datetime import date
from datetime import datetime

today = date.today()
cal_time = today.strftime('%B %d, %Y') 
cal_time2 = datetime.now()
print(cal_time)
print(cal_time2.strftime("%Y-%m-%d %H:%M:%S"))