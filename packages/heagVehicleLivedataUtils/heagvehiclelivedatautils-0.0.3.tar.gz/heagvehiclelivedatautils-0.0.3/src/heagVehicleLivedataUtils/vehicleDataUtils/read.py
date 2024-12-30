"""
Methods for reading vehiclelivedata from json
"""

import pandas as pd
import json

from ..vehicleInformation import encode_line_name

vehicledata_columns = ["lineid", "category", "direction", "status", "latitude", "longitude", "bearing", "type"]
vehicledata_index_timestamp = 'timestamp'
vehicledata_index_vehicleid = 'vehicleid'
vehicledata_index_names = [vehicledata_index_timestamp, vehicledata_index_vehicleid]

def verify_vehicledata_format(dataframe: pd.DataFrame) -> bool:
    """
    checks if dataframe contains a valid vehicle data format
    Args:
        dataframe: dataframe to check

    Throws: Value error if dataframe is not formatted correctly

    """

    expected_columns = set(vehicledata_columns) # is set so that order does not matter -> TODO: is that necessary?
    if not expected_columns <= set(dataframe.columns):
        raise ValueError("dataframe columns do not contain expected columns")

    expected_index_names = set(vehicledata_index_names)
    if not expected_index_names == set(dataframe.index.names):
        raise ValueError("dataframe index names do not match expected names")

    return True

## data reading
def vehicledata_from_dict(vehicledata_dict: dict, *, file_path: str = None)-> pd.DataFrame:
    """ extracts service information of public transport vehicles into a Dataframe

    Args:
        vehicledata_dict (JSON dict): data structured like vehicleData from HEAG vehicleLivedata api
        file_path: used in error messages. If vehicledata_dict is taken from a json file, use its path, otherwise leave empty

    Returns:
        DataFrame: contains the information from the vehicleData, indexed with timestamp and vehicleId
    """
    if not {'timestamp', 'vehicles'} <= vehicledata_dict.keys():
        raise ValueError(
            f"json file {file_path} is not formatted correctly. Missing keys 'timestamp' and/or 'vehicles' ")

    vehicledata_df = pd.DataFrame.from_dict(vehicledata_dict['vehicles'])

    # lowercase colums work better with database
    vehicledata_df.columns = vehicledata_df.columns.str.lower()

    expected_entries_names = set(vehicledata_columns + [vehicledata_index_vehicleid])
    if not expected_entries_names <= set(vehicledata_df.columns):
        if file_path is None:
            message_begin = "vehicledata_dict"
        else:
            message_begin = f"json file {file_path}"

        missing_entries = expected_entries_names - set(vehicledata_df.columns)
        raise ValueError(message_begin + f"was not formatted correctly. Missing entries {missing_entries} in vehicles")

    # use timestamp vehicleId multiindex -> TODO: überlege ob das sinvoll ist (bei db sollte alles in colums stehen, sonnst ist vllt anders praktisch), ist jetzt aba alles darauf ausgelegt
    vehicledata_df.index = pd.MultiIndex.from_product(
                                            [[pd.Timestamp(vehicledata_dict['timestamp'])],
                                                    vehicledata_df[vehicledata_index_vehicleid]],
                                                    names= vehicledata_index_names )

    vehicledata_df['lineid'] = vehicledata_df['lineid'].map(encode_line_name)

    # make sure columns are the expected ones
    vehicledata_df = vehicledata_df.reindex(columns = vehicledata_columns)

    return vehicledata_df

def vehicledata_from_json_files(vehicledata_json_file_paths: list)-> pd.DataFrame:
    """ reads vehicleData from .json files and
    extracts service information of public transport vehicles into a Dataframe

    Args:
        vehicledata_json_file_paths (list): list of paths pointing to the .json files containing the vehicleData

    Returns:
        DataFrame: contains the information from the vehicleData, indexed with timestamp and vehicleId
    """

    vehicledata_df_list = []
    for file_path in vehicledata_json_file_paths:
        with open(file_path) as json_file:
            vehicledata_df_list.append(vehicledata_from_dict(json.load(json_file)))
    return pd.concat(vehicledata_df_list)

