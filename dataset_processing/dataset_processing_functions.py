"""This script holds functions used for processing datasets in
directory ../tablas
"""

import numpy as np
import pandas as pd
import os

def cleanse_dataset(dataset_name):
    """Method used for cleansing the datasets used in this project.
    Given the name of original the dataset in the directory /../datasets/originals, it cleans
    the dataset and writes a clean version, with the same name, in /../datasets/cleansed.

    Parameters
    ----------
    dataset_name : [str] Name of the .csv file, in /../datasets/originals, that contains the
                   dataset to be cleansed.
    """
    
    print(dataset_name)

    # First we generate the path of the dataset.
    this_file_path = os.path.dirname(os.path.realpath('__file__'))
    path_file_to_clean = os.path.join(this_file_path, "datasets/originals", dataset_name)

    # Now we read the dataset.
    data_frame = pd.read_csv(path_file_to_clean, delimiter=';', na_values=' ',
                             encoding = "ISO-8859-1")

    # Because some datasets have the column names in lower case, we first change
    # all column names to uppercase.
    data_frame.columns = map(str.upper, data_frame.columns)
    
    # Next we drop the columns we dont use.
    all_columns = list(data_frame)
    columns_to_keep = ["NOM_RBD", "COD_REG_RBD", "COD_COM_RBD", "COD_DEPE", 
                       "COD_GRADO", "COD_ENSE", "MRUN", "AGNO", "PROM_GRAL",
                       "ASISTENCIA", "SIT_FIN"]
    columns_to_drop = list(set(all_columns) - set(columns_to_keep))
    data_frame.drop(columns_to_drop, axis=1, inplace=True)
    
    # In some cases, due to errors of encoding, we noticed the column AGNO gets deleted. 
    # In those cases we add it.
    years_with_encoding_error = {"rendimiento_2006.csv" : 2006, "rendimiento_2016.csv" : 2016, 
                                 "rendimiento_2018.csv" : 2018, "rendimiento_2019.csv" : 2019,
                                 "rendimiento_2020.csv" : 2020}
    if dataset_name in years_with_encoding_error.keys():
        data_frame["AGNO"] = years_with_encoding_error[dataset_name]    

    # Lets convert grades to the valid format (replacing commas for dots).
    data_frame["PROM_GRAL"] = data_frame["PROM_GRAL"].apply(lambda x : str(x.replace(',', '.')))

    # Now we drop rows with invalid or useless entries.
    data_frame.drop(data_frame[data_frame["PROM_GRAL"] == '0'].index, inplace=True) 
    data_frame.dropna(inplace=True)

    # Now lets specify the types for each column.
    types_dict = {"NOM_RBD" : "object", "COD_REG_RBD" : "int64", 
                  "COD_COM_RBD" : "int64", "COD_DEPE" : "int64", 
                  "COD_GRADO" : "int64", "COD_ENSE" : "int64", 
                  "MRUN" : "int64", "AGNO" : "int64", "PROM_GRAL" : "float64", 
                  "ASISTENCIA" : "int64", "SIT_FIN" : "object"}
    data_frame = data_frame.astype(types_dict)

    # Finally we write the cleansed dataset.
    path_file_to_write = os.path.join(this_file_path, "datasets/cleansed", dataset_name)
    data_frame.to_csv(path_file_to_write)

