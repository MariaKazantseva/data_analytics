import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date


'''1. Клиенты у которых Mitsubishi или Renault
2. Клиенты у которых более двух машин
3. Машины не старше 5 лет
4. Которые были более 2-х раз
5. Последний раз были не позднее 3-х месяцев назад'''


def old(cell):
    if cell == 'unknown':
        return -1
    return date.today().year - int(cell.split('.')[2])


def model(x):
    return x.split()[0]


cars = pd.read_excel('afb.xlsx', dtype={'number': str, 'year': str, 'data_zn': np.datetime64})
cars = cars.fillna('unknown')
# task 1
cars['model'] = cars['model_and_name'].apply(model)
filter_1 = cars['model'].isin(['RENAULT', 'MITSUBISHI'])
# task 2
cars['old'] = cars['year'].apply(old)
filter_2 = (cars['old'] > 0) & (cars['old'] < 5)
# task 3
temp = cars.groupby(['clients']).count()['vin'] > 2
list_clients = temp.index[temp].to_list()
filter_3 = cars["clients"].isin(list_clients)
# task 4
temp_2 = cars.groupby(['vin']).count()['data_zn'] > 2
list_vins = temp_2.index[temp_2].to_list()
filter_4 = cars["vin"].isin(list_vins)
# task 5
last_visit = datetime.today() - timedelta(days=90)
filter_5 = cars.data_zn >= last_visit
result = cars[filter_5 & filter_1 & filter_2 & filter_3 & filter_4].groupby(["clients", "link", "phone"])["vin"].count()
result.to_excel("result.xlsx")






