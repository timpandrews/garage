import json
from datetime import datetime, timedelta

import fitdecode
import folium


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
        for point in input_data["record"]:
            # Create a new dictionary without keys having value None
            point = {key: value for key, value in point.items() if value is not None}

            # Convert semicircles to degrees
            point["position_lat"] = point["position_lat"] * 180 / 2 ** 31
            point["position_long"] = point["position_long"] * 180 / 2 ** 31

            # Conver speed from m/s to km/h so multiply by 3.6 to get km/h
            point["speed"] = round(point["speed"] * 3.6, 1)
            point["enhanced_speed"] = round(point["speed"] * 3.6, 1)

            # Add point to detail list
            detail.append(point)

        print("detail: ", detail)

    elif format == "gpx":
        print("GPX file format not yet supported")

    else:
        print("Unknown file format")

    return detail


# Data Cleaning Functions #
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


# Maping Functions #
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
        data about the ride/activity as well as data from the .fit file including
        the coordinates of the route.

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
        for record in activity.fit_data["record"]:
            # This is the semicircles to/from degrees calc.
            #     degrees = semicircles * ( 180 / 2^31 )
            #     semicircles = degrees * ( 2^31 / 180 )
            lat = record["position_lat"] * 180 / 2 ** 31
            long = record["position_long"] * 180 / 2 ** 31
            coordinates = (lat, long)
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
