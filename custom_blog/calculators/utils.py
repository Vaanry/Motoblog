import pickle
from datetime import datetime
import os
from catboost import CatBoostRegressor
import pandas as pd
from django.core.exceptions import ValidationError



def year_validator(year):
    if not 1885 <= year <= datetime.now().year:
        raise ValidationError(
            'Ожидается год выпуска от 1885 до текущего года'
        )
        

def mileage_validator(mil):
    if not mil >= 0:
        raise ValidationError(
            'Ожидается неотрицательное значение'
        )


def age_counter(year):
    current_year = datetime.now().year
    age = current_year-year
    if age == 0:
        age = 1
    return age


def price_model(data):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, 'moto_scaler.pkl'), 'rb') as f:
        scaler = pickle.load(f)

    model = CatBoostRegressor()
    model.load_model(os.path.join(cur_dir, "motomodel.cbm"))
    
    expluation = data[4]/data[5]
    data.append(expluation)

    X = pd.DataFrame({col:value for col, value in zip(model.feature_names_, data)}, index=[0])
    X[model.feature_names_[2:]] = scaler.transform(X[model.feature_names_[2:]])
    result = int(model.predict(X)[0])
    return result


def mean_vollume(mark, model):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    mean_data = pd.read_csv(os.path.join(cur_dir, 'mean_data.csv'))
    filter_data = mean_data[(mean_data['mark']==mark)&(mean_data['model']==model)]
    vollume = int(filter_data.vollume.values[0])
    return vollume


def mean_power(mark, model):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    mean_data = pd.read_csv(os.path.join(cur_dir, 'mean_data.csv'))
    filter_data = mean_data[(mean_data['mark']==mark)&(mean_data['model']==model)]
    power = filter_data.power.values[0]
    return power


if __name__ == '__main__':
    example = ['Honda', 'Shadow 400', 400, mean_power('Honda', 'Shadow 400'), 44000, 25]
    print(price_model(example))
    print(mean_vollume('Honda', 'Shadow 400'))
    print(mean_power('Honda', 'Shadow 400'))

