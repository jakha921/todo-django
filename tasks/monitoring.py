import time
from django.db import connection

while True:
    time.sleep(10)
    query_time = connection.queries[-1]['time'] if connection.queries else 0
    if query_time > 0.5:
        print('Slow query detected!', connection.queries[-1])
        # send notification to admin