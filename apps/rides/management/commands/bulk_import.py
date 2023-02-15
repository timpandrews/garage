import csv
import json
import os
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from apps.garage.models import Doc


def convert_to_number(str):
    if str == "" or str.isspace():
        return str

    try:
        number = int(str)
    except:
        number = float(str)
    else:
        return str

    return number


def build_ride_dict(row):
    ride = {}
    ride["strava_id"] = row[0]

    start = row[1]
    start = datetime.strptime(start, '%b %d, %Y, %H:%M:%S %p')
    start = start.strftime("%m-%d-%Y %H:%M:%S")
    ride["start"] = start

    ride["title"] = row[2]
    ride["activity_type"] = row[3]
    ride["notes"] = row[4]
    ride["duration"] = convert_to_number(row[16])
    ride["distance"] = convert_to_number(row[6])
    ride["hr_max"] = convert_to_number(row[7])
    ride["relative_effort"] = convert_to_number(row[8])
    ride["equipment"] = row[11]
    ride["gpx_file"] = row[12]
    ride["cadence_max"] = convert_to_number(row[28])
    ride["hr_max"] = convert_to_number(row[30])
    ride["power_max"] = convert_to_number(row[32])
    ride["relative_effort"] = row[8]

    try:
        if row[18] != "":
            ride["speed_max"] = round(float(row[18]), 1)
    except:
        pass

    try:
        ride["speed_avg"] = round(float(row[19]), 1)
    except:
        pass

    try:
        ride["elevation"] = round(float(row[20]))
    except:
        pass

    try:
        ride["cadence_avg"] = round(float(row[29]))
    except:
        pass

    try:
        ride["hr_avg"] = round(float(row[31]))
    except:
        pass


    try:
        ride["power_avg"] = round(float(row[33]))
    except:
        pass

    try:
        ride["calories"] = round(float(row[34]))
    except:
        pass

    return ride


def format_save_data_db(user_id, ride):
    data = {}
    data["import_type"] = "import from strava archive, activities.csv"
    data["strava_id"] = ride["strava_id"]
    data["start"] = ride["start"].replace("-", "/")
    data["title"] = ride["title"]
    data["activity_type"] = ride["activity_type"]
    data["notes"] = ride["notes"]
    data["duration"] = ride["duration"]
    data["distance"] = ride["distance"]
    data["hr_max"] = ride["hr_max"]
    data["relative_effort"] = ride["relative_effort"]
    data["equipment"] = ride["equipment"]
    data["gpx_file"] = ride["gpx_file"]
    data["cadence_max"] = ride["cadence_max"]
    data["hr_max"] = ride["hr_max"]
    if "power_max" in ride.keys():
        data["power_max"] = ride["power_max"]
    data["relative_effort"] = ride["relative_effort"]
    if "speed_max" in ride.keys():
        data["speed_max"] = ride["speed_max"]
    if "speed_avg" in ride.keys():
        data["speed_avg"] = ride["speed_avg"]
    if "elevation" in ride.keys():
        data["elevation"] = ride["elevation"]
    if "cadence_avg" in ride.keys():
        data["cadence_avg"] = ride["cadence_avg"]
    if "hr_avg" in ride.keys():
        data["hr_avg"] = ride["hr_avg"]
    if "power_avg" in ride.keys():
        data["power_avg"] = ride["power_avg"]
    if "calories" in ride.keys():
        data["calories"] = ride["calories"]
    json.dumps(data)

    data_date = data["start"]
    data_date = datetime.strptime(data_date, '%m/%d/%Y %H:%M:%S')
    r = Doc(
        user_id = user_id,
        data_type = "ride",
        data_date = data_date,
        data = data,
        created = datetime.now(),
        updated = datetime.now()
    )
    r.save()


class Command(BaseCommand):
    help = 'Bulk Import from Strava Files'

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=str)
        parser.add_argument('user_id', nargs='+', type=int)

    def handle(self, *args, **options):
        user_id = options['user_id'][0]
        os.chdir('data')
        fn = options['file_name'][0]

        rides = []
        with open(fn) as file_obj:
            reader_obj = csv.reader(file_obj)
            next(reader_obj)
            print("Read Files:")
            for i, row in enumerate(reader_obj):
                ride = build_ride_dict(row)
                rides.append(ride)
                print('.', end='')

        print("\nSave to db:")
        for ride in rides:
            format_save_data_db(user_id, ride)
            print('.', end='')
        print("\n")






