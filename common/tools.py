from datetime import datetime

import fitdecode


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