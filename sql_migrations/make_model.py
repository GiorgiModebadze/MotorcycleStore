import pandas as pd
import sqlite3

data = pd.read_csv("data/January_2020_MPSOV.csv", index_col='ePID')
motorcylce_data = data[data['Vehicle Type'] == 'Motorcycle']
conn = sqlite3.connect("../database.db")

types = motorcylce_data['Motorcycle Type'].unique()
print(types)

# make_data = pd.DataFrame(motorcylce_data['Make'].unique()).reset_index()
# make_data.columns = ['id', 'make']
# make_data.to_sql('make', conn, if_exists='append', index=False)

# model data
# model_data = motorcylce_data[['Model', 'Make']].reset_index(drop=['ePID'])

# model_make_data = pd.merge(model_data, make_data,
#                            how="inner",  left_on="Make", right_on="make")

# model_make_data.rename({'id': "make_id"}, inplace=True, axis=1)
# model_make_data.drop_duplicates(inplace=True)
# model_make_data['id'] = model_make_data.index
# model_make_data[['id', 'Model', 'make_id']].to_sql(
#     'model', conn, if_exists='append', index=False)
