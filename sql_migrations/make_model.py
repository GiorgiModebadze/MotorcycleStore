import pandas as pd
import sqlite3

data = pd.read_csv("data/January_2020_MPSOV.csv", index_col='ePID')
motorcylce_data = data[data['Vehicle Type'] == 'Motorcycle']
make_data = pd.DataFrame(motorcylce_data['Make'].unique()).reset_index()
make_data.columns = ['id', 'make']
print(make_data)
conn = sqlite3.connect("../database.db")
make_data.to_sql('make', conn, if_exists='append', index=False)
