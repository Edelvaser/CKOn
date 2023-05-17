from datetime import datetime

def date_to_unix(s_date):
    return int(datetime.strptime(s_date, "%Y-%m-%d").timestamp())

def unix_to_date(n_date):
    return datetime.fromtimestamp(n_date).strftime("%Y-%m-%d")

# def get_now_unix():
#     return int(datetime(2023, 1, datetime.now().day).timestamp())

# a = date_to_unix("2018-07-22")
# b = unix_to_date(1532206800)
# print(a)
# print(b)
# print(get_now_unix())