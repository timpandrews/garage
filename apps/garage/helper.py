import calendar
from datetime import date, datetime, timedelta

from apps.garage.models import Doc


def get_date_ranges(today, user):
    print("today:", today, type(today))
    print("user:", user)

    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    month_start = date(today.year, today.month, 1)
    month_end =date(
        today.year, today.month, calendar.monthrange(today.year, today.month)[1]
    )

    year_start = date(today.year, 1, 1)
    year_end = date(today.year, 12, 31)

    earliest_ride = Doc.objects.filter(user=user, active=True).earliest()
    start_date = earliest_ride.data_date
    lifetime_start = date(start_date.year, start_date.month, start_date.day)
    lifetime_end = year_end


    date_ranges = {}
    date_ranges["week_start"] = week_start
    date_ranges["week_end"] = week_end
    date_ranges["month_start"] = month_start
    date_ranges["month_end"] = month_end
    date_ranges["year_start"] = year_start
    date_ranges["year_end"] = year_end
    date_ranges["lifetime_start"] = lifetime_start
    date_ranges["lifetime_end"] = lifetime_end

    return date_ranges


def rides_serializer(rides_qs):
    """ Takes queryset obj of rides with normal sql fields & sql jsonb field
        Will create a dictionary of each ride & pull individual values from the
        jsonb field
        Will then create and return a list of dictionaries
        ** converts the start str to datetime obj

    Args:
        rides_qs (): queryset of rides
    """

    rides = []
    for ride in rides_qs:
        ride_dict = {}
        ride_dict["id"] = ride.id
        ride_dict["user"] = ride.user
        ride_dict["data_type"] = ride.data_type
        ride_dict["created"] = ride.created
        ride_dict["updated"] = ride.updated
        if isinstance(ride.data, str):
            ride.data = json.loads(ride.data)
        for k, v in ride.data.items():
            if k == "start":
                v = datetime.strptime(v, "%m/%d/%Y %H:%M:%S")
                ride_dict[k] = v
            else:
                ride_dict[k] = v
        rides.append(ride_dict)

    return(rides)


def get_rides_in_range(user, start, end):
    rides = rides_serializer(Doc.objects.filter(
        user = user,
        data_type = "ride",
        data_date__range=[start, end],
        active = True,
        ))

    return rides