import datetime


def g(f: datetime.date):
    print(type(f))
    assert type(f) is datetime.date
    print(f.day)


g("01:02:2024")
