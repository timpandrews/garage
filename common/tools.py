import json
from datetime import datetime, timedelta

import fitdecode
import folium
import geopy.distance


# File Import Functions #
def import_fit_file(file_path):
    """
    Import a FIT file and return a dictionary of the data
    :param file_path: path to the FIT file
    :return: dictionary contain all userful data from the FIT file
    """
    data_types = []
    with fitdecode.FitReader(file_path) as fit:
        fit_file = {}
        for frame in fit:
            if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                if frame.name not in data_types:
                    fit_file[frame.name] = ""
                    data_types.append(frame.name)

    # loop through the fit file again for each data_type
    for data_type in data_types:
        data = []
        with fitdecode.FitReader(file_path) as fit:
            for frame in fit:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA and frame.name == data_type:
                    row = {}
                    for field in frame:
                        # TODO do I need to convert datatime to string if I don't convert to JSON?
                        if type(field.value) == datetime:
                            row[field.name] = field.value.strftime('%Y-%m-%d %H:%M:%S %Z')
                        else:
                            row[field.name] = field.value
                    data.append(row)
            fit_file[data_type] = data

    return fit_file


def get_detail_from_input_data(format, input_data):
    """_summary_

    Args:
        format (_str_):     "fit" or "gpx".  A string indicating the format of the
                            input data.
        input_data (_dict_): A dictionary of data from the input file.  Exact format of
                             the dictionary depends on the format and source of the input
                             file.

    Returns:
        _dict_: A dictionary of data formatted in a consistent manner regardless of
                the input file format.  This dictionary can be stored in the database
                and used to build ride maps and ride analysis charts.
    """
    detail = list()

    # FIT file format
    if format == "fit":
        for i, point in enumerate(input_data["record"]):
            # Create a new dictionary without keys having value None
            point = {key: value for key, value in point.items() if value is not None}

            # Convert semicircles to degrees
            point["position_lat"] = point["position_lat"] * 180 / 2 ** 31
            point["position_long"] = point["position_long"] * 180 / 2 ** 31

            # Conver speed from m/s to km/h so multiply by 3.6 to get km/h
            point["speed"] = round(point["speed"] * 3.6, 1)
            point["enhanced_speed"] = round(point["speed"] * 3.6, 1)

            # Build computed distance values
            if i == 0:
                point["computed_distance"] = 0
            else:
                cord1 = (point["position_lat"], point["position_long"])
                cord2 = (detail[-1]["position_lat"], detail[-1]["position_long"])

                distance = geopy.distance.distance(cord1, cord2).km
                point["computed_distance"] = detail[-1]["computed_distance"] + distance

            # Add point to detail list
            detail.append(point)

    elif format == "gpx":
        print("GPX file format not yet supported")

    else:
        print("Unknown file format")

    return detail


def get_weighted_average_power(power_data, interval_data):
    """
    Given a list of recorded power and a list of the duration of each interval
    return a single value for the weighted average power of the ride.

    Args:
        power_data (list): A list of power data points from a given interval
                           for the ride.
        interval_data (list): A list of intervals between power data points
                              (in seconds).

    Returns:
        float: Returns a single value for the weighted average power of the ride.
    """
    # FIXME: This solution does not assign a weight to each interval.  All power readigns
    #       are weighted equally.  This is not ideal.  Need to find a way to assign
    #       a weight to each interval based on power readings and power-duration curve
    #       for the rider.  Higher power readings are normally weighted more heavily
    #       than lower power readings.  https://github.com/timpandrews/garage/wiki/Calculate-Weighted-Power-Average

    if len(power_data) != len(interval_data):
        raise ValueError("Both lists must have the same length.")

    weighted_average_power = 0
    total_duration = 0

    for i, power in enumerate(power_data):
        weighted_average_power += power * interval_data[i]
        total_duration += interval_data[i]

    weighted_average_power = weighted_average_power / total_duration
    weighted_average_power = round(weighted_average_power)

    return weighted_average_power


def get_total_work(power_data, interval_data):
    """
    Given a list of recorded power and a list of the duration of each interval
    return a single value for the total work done during the ride in kilojoules.

    Args:
        power_data (list): A list of power data points from a given interval
                           for the ride.
        interval_data (list): A list of intervals between power data points
                              (in seconds).

    Returns:
        float: Returns a single value for the total work of the ride in kilojoules.
    """
    if len(power_data) != len(interval_data):
        raise ValueError("Both lists must have the same length.")

    total_work = 0

    for i, power in enumerate(power_data):
        total_work += power * interval_data[i]

    total_work = total_work / 1000
    total_work = round(total_work)

    return total_work


# Data Cleaning & Converting Functions #
def clean_data_for_db(data):
    """
    Takes a dictionary of data and cleans it for storage in the database.
    In particular it looks to convert date & time fields between human readable
    formats and formats that can be stored in the database.

    Args:
        data (dict): A dictionary of data to be stored in the database

    Returns:
        dict: returns the same input dictionry with the data cleaned for storage
    """
    # convert H:M:S duration field to total seconds
    try:
        data["duration"] = data["duration"].total_seconds()
    except:
        pass

    # convert datetime object to string to stor in JSON
    try:
        data["start"] = data["start"].strftime("%m/%d/%Y %H:%M:%S")
    except:
        pass

    return data


def clean_data_for_display(data):
    """
    Takes a dictionary of data from the db and cleans it for display in the UI.
    In particular it looks to convert date & time fields between human readable
    formats and formats that can be stored in the database.

    Args:
        data (dict): A dictionary of data to be stored in the database

    Returns:
        dict: returns the same input dictionry with the data cleaned for storage
    """
    # convert duration field from seconds to H:M:S format
    try:
        data["duration"] = str(timedelta(seconds=data["duration"]))
    except:
        pass

    return data


def clean_data_for_edit(data):
    """
    Takes a dictionary of data from the db and cleans it for use in editable forms.
    In particular it looks to convert date & time fields between human readable
    formats and formats that can be stored in the database.

    Args:
        data (dict): A dictionary of data to be stored in the database

    Returns:
        dict: returns the same input dictionry with the data cleaned for storage
    """
    # convert duration field from seconds to H:M:S format
    try:
        data["duration"] = str(timedelta(seconds=data["duration"]))
    except:
        pass

    # convert datetime string to datetime object for datetime formfield
    try:
        data["start"] = datetime.strptime(data["start"], "%m/%d/%Y %H:%M:%S")
    except:
        pass

    return data


def get_unit_names(units_display_preference):
    """
    Returns a dictionary of unit names for the given
    units_display_preference (imperial or metric)


    Args:
        units_display_preference (str): "imperial" or "metric"

    Returns:
        dict: A dictionary of unit names for the given
              units_display_preference (imperial or metric)
    """
    unit_names = dict()
    if units_display_preference == "imperial":
        unit_names["distance"] = "miles"
        unit_names["speed"] = "mph"
        unit_names["weight"] = "lbs"
        unit_names["elevation"] = "ft"
        unit_names["temperature"] = "F"

    else: # metric is the default setting
        unit_names["distance"] = "km"
        unit_names["speed"] = "km/h"
        unit_names["weight"] = "kg"
        unit_names["elevation"] = "m"
        unit_names["temperature"] = "C"

    # unit names that are the same for imperial and metric
    unit_names["power"] = "watts"
    unit_names["cadence"] = "rpm"
    unit_names["hr"] = "bpm"
    unit_names["duration"] = "H:M:S"
    unit_names["calories"] = "calories"

    return unit_names


def convert_to_imperial(data, type):
    """
    Converts data from metric to imperial units.  Data is always stored in the
    database in metric units.  This function is used to convert the data to
    imperial units for display in the UI if required by the user as defined in
    their profile settings (units_display_preference).

    Args:
        data (dict/list): A dictionary/list of data points from each activity.  Data is
                     stored in the database in metric units.
        type (str): A string indicating the type of activity.  Used to determine


    Returns:
        _dict_: The input dictionary converted to imperial units.
    """

    # convert HP weight from kg to lbs
    if type == "hp" and data["type"] == "weight":
        data["weight"] = round(data["weight"] * 2.20462)

    # convert ride distance units metric to imperial
    if type == "ride":
        if "distance" in data.keys() and data["distance"] != "None":
            data["distance"] = round(data["distance"] * 0.621371, 1)
        if "elevation" in data.keys() and data["elevation"] is not None:
            data["elevation"] = round(data["elevation"] * 3.28084)
        if "speed_max" in data.keys() and data["speed_max"] is not None:
            data["speed_max"] = round(data["speed_max"] * 0.621371, 1)
        if "speed_avg" in data.keys() and data["speed_avg"] is not None:
            data["speed_avg"] = round(data["speed_avg"] * 0.621371, 1)

    if type == "dashboard_week":
        if "distance" in data.keys() and data["distance"] != "None":
            data["distance"] = round(data["distance"] * 0.621371, 2)
        if "elevation" in data.keys() and data["elevation"] is not None:
            data["elevation"] = round(data["elevation"] * 3.28084, 2)

    if type == "dashboard_data":
        # convert each item in the data list
        for i, item in enumerate(data):
            data[i] = round(item * 0.621371 )

    return data


def convert_to_metric(data, type):
    """
    Converts data from imperial to metric units.  Data is always stored in the
    database in metric units.  This function is used to convert the data to
    metric units for storage if required by the user as defined in their profile
    settings (units_display_preference).


    Args:
        data (dict): A dictionary of data points from each activity.  Data is
                     stored in the database in metric units.
        type (str): A string indicating the type of activity.

    Returns:
        dict: The input dictionary converted to metric units.
    """
    # convert ride distance units imperial to metric
    if type == "ride":
        if "distance" in data.keys() and data["distance"] != "None":
            data["distance"] = round(data["distance"] * 1.60934, 1)
        if "elevation" in data.keys() and data["elevation"] is not None:
            data["elevation"] = round(data["elevation"] / 3.28084)
        if "speed_max" in data.keys() and data["speed_max"] is not None:
            data["speed_max"] = round(data["speed_max"] * 1.60934, 1)
        if "speed_avg" in data.keys() and data["speed_avg"] is not None:
            data["speed_avg"] = round(data["speed_avg"] * 1.60934, 1)

    # convert HP weight from lbs to kg
    if type == "weight":
        data["weight"] = round(data["weight"] / 2.20462, 2)

    return data


# Maping & Charting Functions #
def find_centroid(coordinates):
    """
    Given a list of coordinates (lat/long), will return the centroid (center point)

    Args:
        coordinates (list): A list of tuple pairs of Latitudes and Longitudes.
        Example: [(lat1, long1), (lat2, long2), ...]
        Latitutdes and Logitudes must be floats

    Returns:
        tuple: Returns a tuple of the centroid (lat, long) of the coordinates of
        the center point of the given coordinates.  For example: (lat, long) where
        lat and long are floats.
    """
    x = [float(x) for x, y in coordinates]
    y = [float(y) for x, y in coordinates]
    centroid = (sum(x) / len(coordinates), sum(y) / len(coordinates))

    return centroid


def build_map(activity):
    """
    Given an activity (ride with coordinates), will build a map of the route
    using the folium library.  Map will take coordinatres and build a polyline
    of the route.  Map will be centered on the centroid of the route.

    Args:
        activity (dict): Activity is a dict of the ride data.  It includes meta
        data about the ride/activity as well as data from the .fit or gpx files with
        detailed activity data, including the coordinates of the route. This data is
        converted to a standard format at stored in the detail field in the db.

    Returns:
        *if coordinates are available*
        folium map object: Returns a folium map object that can be rendered as html
        in a template..

        *if no coordinates are available*
        string: Returns a string that says "No Map Data" when the map cannot be
        built.

    """
    try:
        route = []
        for record in activity.detail:
            coordinates = (record["position_lat"], record["position_long"])
            route.append(coordinates)

        centroid = find_centroid(route)
        m = folium.Map(
            location=[centroid[0], centroid[1]],
            zoom_start=13,
            tiles='OpenStreetMap',
        )
        folium.PolyLine(route).add_to(m)
        return m._repr_html_()

    except Exception as e:
        return "No Map Data"


def build_elevation_chart(activity, units_display_preference):
    labels = list()
    elevation = list()

    if units_display_preference == "imperial":
        for record in activity.detail:
            labels.append(record["computed_distance"] * 0.621371)
            elevation.append(record["altitude"] * 3.28084)
    else:
        for record in activity.detail:
            labels.append(record["computed_distance"])
            elevation.append(record["altitude"])

    return labels, elevation