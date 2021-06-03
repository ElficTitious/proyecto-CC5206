
from dataset_processing_functions import *

if __name__ == "__main__":
    
    years = ["02", "03", "04", "05", "06", "07", "08", "09", "10", "11", 
             "12", "13", "14", "15", "16", "17", "18", "19", "20"]

    dataset_file_names = ["rendimiento_20{}.csv".format(e) for e in years]

    y = 2002
    for file_name in dataset_file_names:
       generate_grouped_dataset(file_name, y)
       y += 1 
