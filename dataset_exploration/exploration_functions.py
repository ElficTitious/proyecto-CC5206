import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def generate_plots():

    # First we generate the path of the dataset.
    this_path = os.path.dirname(os.path.realpath('__file__'))

    dataframe_list = []

    years = [year for year in range(2002, 2021)]

    for year in years:
        path_file_dataset = os.path.join(this_path, 
                                         "datasets/datasets_grouped/{0}/means_depe_{0}.csv".format(year))
                
        # Now we read the dataset.
        dataframe = pd.read_csv(path_file_dataset, encoding = "ISO-8859-1")
        dataframe_list.append(dataframe)

    # means_depe[0] for municipal, means_depe[1] for subvencionado, means_depe[1] for particular 
    means_depe = np.zeros((3, 19)) 
   
    for i in range(3):
        for j in range(19):
            dataframe = dataframe_list[j]
            means_depe[i][j] = dataframe[dataframe["COD_DEPE"] == i+1]["PROM_GRAL"]           

    plt.plot(years, means_depe[0], label="Promedio general para establecimientos municipales")
    plt.plot(years, means_depe[1], label="Promedio general para establecimientos subvencionados")
    plt.plot(years, means_depe[2], label="Promedio general para establecimientos particulares")
    plt.legend()
    plt.tight_layout()
    plt.show()

generate_plots()
 
     
