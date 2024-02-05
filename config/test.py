from datetime import datetime, timedelta

print(datetime.now())
print(timedelta(days=1))
print(datetime.now() > datetime.now() - timedelta(days=1))
