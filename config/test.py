from datetime import datetime, timedelta, date

print(datetime.now())
print(timedelta(days=1))
print(datetime.now() > datetime.now() - timedelta(days=1))
