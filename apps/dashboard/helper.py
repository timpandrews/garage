import json
from datetime import date, datetime, timedelta

from dateutil.relativedelta import MO, relativedelta

from apps.garage.models import Doc


def rides_serializer(rides):
    """ Takes queryset obj of rides with normal sql fields & sql jsonb field
        Will create a dictionary of each ride & pull individual values from the
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
        if isinstance(ride.data, str):
            ride.data = json.loads(ride.data)
        for k, v in ride.data.items():
            if k == "start":
                v = datetime.strptime(v, "%m/%d/%Y %H:%M:%S")
                ride_dict[k] = v
            else:
                ride_dict[k] = v
        rides_list.append(ride_dict)

    return(rides_list)


def get_week_range(compare_to_day=date.today()):
    week_start = compare_to_day + relativedelta(weekday=MO(-1))
    week_start = week_start.strftime("%Y-%m-%d %H:%M:%S")
    week_start = datetime.strptime(week_start, "%Y-%m-%d %H:%M:%S")

    week_end = week_start + timedelta(days=6)
    week_end = datetime(week_end.year, week_end.month, week_end.day, 23, 59, 59)
    week_range = {
        "start": week_start,
        "end": week_end,
    }
    return(week_range)


def get_week_ranges(weeks):
    week_ranges = []
    for x in range(weeks):
        compare_to_day = date.today() - timedelta(days = (7*x))
        week_ranges.append(get_week_range(compare_to_day))

    return week_ranges


def get_weekly_rides(week_range, user):
    user_rides = rides_serializer(Doc.objects.filter(
        user = user,
        data_type = "ride",
        data_date__range=[week_range["start"], week_range["end"]],
        active = True,
        ))

    weekly_rides = []
    for ride in user_rides:
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

    sums["distance"] = round(distance)
    time_str = str(timedelta(seconds=time))
    time_parts = time_str.split(':')
    time_str = time_parts[0] + 'h ' + time_parts[1] + 'm ' + time_parts[2] + 's '
    sums["time"] = time_str
    sums["elevation"] = elevation
    sums["calories"] = calories
    return(sums)


def get_distance_history(user):
    week_ranges = get_week_ranges(12)
    distance_history = []
    for week_range in week_ranges:
        weekly_rides = get_weekly_rides(week_range, user)
        weekly_sums = get_weekly_sums(weekly_rides)
        distance_history.append(weekly_sums["distance"])

    return (week_ranges, distance_history)


def convert_ranges_to_str(input_ranges):
    output_ranges = []
    for range in input_ranges:
        start = str(range["start"].strftime("%d %b"))
        end = str(range["end"].strftime("%d %b"))
        range_str = start + " to " + end

        output_ranges.append(range_str)
    return output_ranges


def get_color(colors, index):
    """
    loops through list of colors if in returning next color, when you
    reach the end it will then start back at the begining.  Unlike
    the itertools.cycle() function this function always starts with
    colors[0]

    Args:
        colors (list): list of colors to be used
        index (int): position index (may be greater then number of colors)

    Returns:
        str: color code ie #827BC5
    """
    num_items = len(colors)
    color_found = False

    while not color_found:
        if index <= num_items -1:
            color = colors[index]
            color_found = True
        else:
            index = index - num_items
            color_found = False

    return color
