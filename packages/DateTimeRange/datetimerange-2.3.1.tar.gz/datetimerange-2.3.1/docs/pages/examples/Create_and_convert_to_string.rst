Create a DateTimeRange instance from start and end datetime
-----------------------------------------------------------------
:Sample Code:
    .. code:: python

        from datetimerange import DateTimeRange
        time_range = DateTimeRange("2015-03-22T10:00:00+0900", "2015-03-22T10:10:00+0900")
        str(time_range)

:Output:
    ::

        '2015-03-22T10:00:00+0900 - 2015-03-22T10:10:00+0900'
