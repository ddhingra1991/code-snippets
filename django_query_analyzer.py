"""
Source: https://openfolder.sh/django-faster-speed-tutorial
"""
from timeit import default_timer as timer
from django.db import connection, reset_queries


def django_query_analyze(func):
    """decorator to perform analysis on Django queries
    Usage:
    place this decorator on the top of any method where you are hitting
    some database query through ORM. This returns:
    - no. of queries
    - total time taken in ms
    Eg:
    @django_query_analyze
    def some_method():
        ..
        ..
        some_query = SomeModel.objects.all()
        ..
        return result

    output:
    ran function some_method
    --------------------
    number of queries: 1
    Time of execution: 0.01481s
    """

    def wrapper(*args, **kwargs):

        avs = []
        query_counts = []
        for _ in range(20):
            reset_queries()
            start = timer()
            func(*args, **kwargs)
            end = timer()
            avs.append(end - start)
            query_counts.append(len(connection.queries))
            reset_queries()

        print()
        print(f"ran function {func.__name__}")
        print(f"-" * 20)
        print(f"number of queries: {int(sum(query_counts) / len(query_counts))}")
        print(f"Time of execution: {float(format(min(avs), '.5f'))}s")
        print()
        return func(*args, **kwargs)

    return wrapper
