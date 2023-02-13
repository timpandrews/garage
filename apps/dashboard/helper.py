from datetime import date
from dateutil.relativedelta import relativedelta, MO
from apps.garage.models import Doc
from datetime import datetime, timedelta


def rides_serializer(rides):
    """ Takes queryset obj of rides with normal sql fields & sql jsonb field
        Will create a dictionary of each ride pull individual values from the
        jsonb field
        Will then create and return a list of dictionaries
        ** converts the start str to datetime obj

    Args:
        rides (): queryset of rides
    """
    rides_list = []
    for ride in rides:
        ride_dict = {}
        ride_dict["id"] = ride.id
        ride_dict["user"] = ride.user
        ride_dict["data_type"] = ride.data_type
        ride_dict["created"] = ride.created
        ride_dict["updated"] = ride.updated
        for k, v in ride.data.items():
            if k == "start":
                v = datetime.strptime(v, "%m/%d/%Y %H:%M:%S")
                ride_dict[k] = v
            else:
                ride_dict[k] = v
        rides_list.append(ride_dict)

    return(rides_list)


def get_week_range():
    today = date.today()
    week_start = today + relativedelta(weekday=MO(-1))
    week_start = week_start.strftime("%Y-%m-%d %H:%M:%S")
    week_start = datetime.strptime(week_start, "%Y-%m-%d %H:%M:%S")

    week_end = week_start + timedelta(days=6)
    week_end = datetime(week_end.year, week_end.month, week_end.day, 23, 59, 59)
    week_range = {
        "start": week_start,
        "end": week_end,
    }
    return(week_range)


def get_weekly_rides(week_range, user):
    user_rides = rides_serializer(Doc.objects.filter(user = user, data_type = "ride"))

    weekly_rides = []
    for ride in user_rides:
        print("ride['start']", ride["start"], type(ride["start"]))
        if week_range["start"] <= ride["start"] <= week_range["end"]:
            # in range
            weekly_rides.append(ride)

    return(weekly_rides)


def get_weekly_sums(weekly_rides):
    sums = {}
    distance = 0
    time = 0
    elevation = 0
    calories = 0
    for ride in weekly_rides:
        distance += ride["distance"]
        time += ride["duration"]
        elevation += ride["elevation"]
        calories += ride["calories"]

    sums["distance"] = distance
    time_str = str(timedelta(seconds=time))
    time_parts = time_str.split(':')
    time_str = time_parts[0] + 'h ' + time_parts[1] + 'm ' + time_parts[2] + 's '
    sums["time"] = time_str
    sums["elevation"] = elevation
    sums["calories"] = calories
    return(sums)
