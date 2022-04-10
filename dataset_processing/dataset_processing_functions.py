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
    this_path = os.path.dirname(os.path.realpath('__file__'))
    path_file_to_clean = os.path.join(this_path, "datasets/originals", dataset_name)

    # Now we read the dataset.
    dataframe = pd.read_csv(path_file_to_clean, delimiter=';', na_values=' ',
                             encoding = "ISO-8859-1")

    # Because some datasets have the column names in lower case, we first change
    # all column names to uppercase.
    dataframe.columns = map(str.upper, dataframe.columns)
    
    # Next we drop the columns we dont use.
    all_columns = list(dataframe)
    columns_to_keep = ["NOM_RBD", "COD_REG_RBD", "COD_COM_RBD", "COD_DEPE", 
                       "COD_GRADO", "COD_ENSE", "MRUN", "AGNO", "PROM_GRAL",
                       "ASISTENCIA", "RURAL_RBD", "SIT_FIN"]
    columns_to_drop = list(set(all_columns) - set(columns_to_keep))
    dataframe.drop(columns_to_drop, axis=1, inplace=True)
    
    # In some cases, due to errors of encoding, we noticed the column AGNO gets deleted. 
    # In those cases we add it.
    years_with_encoding_error = {"rendimiento_2006.csv" : 2006, "rendimiento_2016.csv" : 2016, 
                                 "rendimiento_2018.csv" : 2018, "rendimiento_2019.csv" : 2019,
                                 "rendimiento_2020.csv" : 2020}
    if dataset_name in years_with_encoding_error.keys():
        dataframe["AGNO"] = years_with_encoding_error[dataset_name]    

    # Lets convert grades to the valid format (replacing commas for dots).
    dataframe["PROM_GRAL"] = dataframe["PROM_GRAL"].apply(lambda x : str(x.replace(',', '.')))

    dataframe.loc[dataframe["COD_DEPE"]==2, ["COD_DEPE"]] = 1
    for i in range(3, 7):
        dataframe.loc[dataframe["COD_DEPE"]==i, ["COD_DEPE"]] = i-1
        

    # Now we drop rows with invalid or useless entries.
    dataframe.drop(dataframe[dataframe["PROM_GRAL"] == '0'].index, inplace=True) 
    dataframe.dropna(inplace=True)

    # Now lets specify the types for each column.
    types_dict = {"NOM_RBD" : "object", "COD_REG_RBD" : "int64", 
                  "COD_COM_RBD" : "int64", "COD_DEPE" : "int64", 
                  "COD_GRADO" : "int64", "COD_ENSE" : "int64", "RURAL_RBD" : "int64", 
                  "MRUN" : "int64", "AGNO" : "int64", "PROM_GRAL" : "float64", 
                  "ASISTENCIA" : "int64", "SIT_FIN" : "object"}
    dataframe = dataframe.astype(types_dict)

    # Finally we write the cleansed dataset.
    path_file_to_write = os.path.join(this_path, "datasets/cleansed", dataset_name)
    dataframe.to_csv(path_file_to_write, index=False, encoding = "ISO-8859-1")


def generate_grouped_dataset(dataset_name, year):
    """Method used for generating the grouped datasets used in this project.
    Given the name of the cleansed dataset in the directory /../datasets/cleansed, and 
    the year that datasets corresponds to, it generates generates a number of grouped
    datasets aggregated by mean for PROM_GRAL and ASISTENCIA, and writes them in
    /../datasets/datasets_grouped/<year>.

    Parameters
    ----------
    dataset_name : [str] Name of the .csv file, in /../datasets/cleansed, that contains the
                   dataset for which to generate the new grouped datasets.
    year : [int] Year that dataset_name corresponds to.
    """
    
    # First we generate the path of the dataset.
    this_path = os.path.dirname(os.path.realpath('__file__'))
    path_file_dataset = os.path.join(this_path, "datasets/cleansed", dataset_name)

    # Now we read the dataset.
    dataframe = pd.read_csv(path_file_dataset, encoding = "ISO-8859-1")
   
    # We generate the new datasets. 
    means_depe_by_comuna = dataframe.groupby(["AGNO", "COD_REG_RBD", "COD_COM_RBD", "COD_DEPE"], as_index=False) \
                           [["PROM_GRAL", "ASISTENCIA"]].agg("mean").round(1)
    means_depe_by_region = dataframe.groupby(["AGNO", "COD_REG_RBD", "COD_DEPE"], as_index=False) \
                           [["PROM_GRAL", "ASISTENCIA"]].agg("mean").round(1)
    means_depe = dataframe.groupby(["AGNO", "COD_DEPE"], as_index=False)[["PROM_GRAL", "ASISTENCIA"]].agg("mean")
    means_comuna_by_region = dataframe.groupby(["AGNO", "COD_REG_RBD", "COD_COM_RBD"], as_index=False) \
                             [["PROM_GRAL", "ASISTENCIA"]].agg("mean").round(1)
    means_region = dataframe.groupby(["AGNO", "COD_REG_RBD"], as_index=False)[["PROM_GRAL", "ASISTENCIA"]].agg("mean").round(1)
    means_rural_by_region = dataframe.groupby(["AGNO", "COD_REG_RBD", "RURAL_RBD"], as_index=False)[["PROM_GRAL", "ASISTENCIA"]].agg("mean").round(1)
    means_colegio = dataframe.groupby(["AGNO", "NOM_RBD", "COD_REG_RBD", "COD_COM_RBD", 
                                       "COD_DEPE"], as_index=False)[["PROM_GRAL", "ASISTENCIA"]].agg("mean").round(1)
    
    # Dictionary for writing files.
    grouped_datasets_dict = {"means_depe_by_comuna" : means_depe_by_comuna, 
                             "means_depe_by_region" : means_depe_by_region,  
                             "means_depe" : means_depe, "means_comuna_by_region" : means_comuna_by_region, 
                             "means_region" : means_region, "means_colegio" : means_colegio,
                             "means_rural_by_region" : means_rural_by_region}

    # We write all the datasets for the given year
    for name in grouped_datasets_dict.keys():
        file_name = name + "_{}.csv".format(year)
        print("Writing ", file_name)
        path_file_to_write = os.path.join(this_path, "datasets/datasets_grouped/{}".format(year), file_name)
        
        grouped_datasets_dict[name].to_csv(path_file_to_write, index=False, encoding = "ISO-8859-1")
        
       
     
