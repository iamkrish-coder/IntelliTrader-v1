import pandas as pd
import os
import datetime as dt

class Helper:
    def __init__(self, object):
        self.prop = object

    # Store output to a text file
    def write_output_text(self, filename, data):
        path = './output'
        if os.path.exists(path):
            with open(path + '/' + filename, 'w') as file:
                file.write(data)
        else :
            os.mkdir(path)
            with open(path + '/' + filename, 'w') as file:
                file.write(data)

    # Store output to a csv file
    def write_output_csv(self, filename, data):
        path = './output'
        if os.path.exists(path):
            csv_data = pd.DataFrame(data)
            csv_data.to_csv(path + '/' + filename, index=False)
        else :
            os.mkdir(path)
            csv_data = pd.DataFrame(data)
            csv_data.to_csv(path + '/' + filename, index=False)







