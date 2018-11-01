import datetime

def get_time():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return time
