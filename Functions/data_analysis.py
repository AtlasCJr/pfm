import pandas as pd
from Functions.classes import enrichedData
import numpy as np

def getTimeCycle(data: pd.DataFrame, cycle: str, pos: int = 0) -> pd.DataFrame:
    """
    Groups the data by the specified time cycle (Day, Week, Month, Year) and positions it based on the pos parameter.

    Parameters:
    data (pd.DataFrame): The input DataFrame with a 'CREATED_AT' column.
    cycle (str): The time cycle to group by. Allowed values are "DAY", "WEEK", "MONTH", "YEAR".
    pos (int): The position offset for the time period.

    Returns:
    pd.DataFrame: The DataFrame grouped by the specified time cycle.
    """

    cycle = str.upper(cycle)
    if cycle not in ["DAY", "WEEK", "MONTH", "YEAR"]:
        return

    frequency = {'DAY': 'D', 'WEEK': 'W', 'MONTH': 'ME', 'YEAR': 'YE'}[cycle]

    data['CREATED_AT'] = pd.to_datetime(data['CREATED_AT'])
    data = data.drop(columns=['UPDATED_AT', 'TRANSACTION_ID', 'ITEM', 'USERNAME']).set_index('CREATED_AT')

    latest_date = data.index.max()

    if cycle == 'DAY':
        start_date = (latest_date - pd.DateOffset(days=(pos+1)*7)).replace(hour=0, minute=0, second=0)
        end_date = (latest_date - pd.DateOffset(days=pos*7)).replace(hour=23, minute=59, second=59)
    elif cycle == 'WEEK':
        start_date = (latest_date - pd.DateOffset(weeks=(pos+1)*5)).replace(hour=0, minute=0, second=0)
        end_date = (latest_date - pd.DateOffset(weeks=pos*5)).replace(hour=23, minute=59, second=59)
    elif cycle == 'MONTH':
        start_date = (latest_date - pd.DateOffset(months=(pos+1)*12)).replace(hour=0, minute=0, second=0)
        end_date = (latest_date - pd.DateOffset(months=pos*12)).replace(hour=23, minute=59, second=59)
    elif cycle == 'YEAR':
        start_date = data.index.min()
        end_date = latest_date

    print(start_date, end_date)

    data = data[(data.index >= start_date) & (data.index <= end_date)]

    expenses = pd.concat([
        data[(data['CATEGORY'] == 0) & (data['TYPE'] == i)]
        .drop(columns=['CATEGORY', 'TYPE'])
        .resample(frequency)
        .sum()
        .rename(columns={'VALUE': f'{i}'})
        for i in data[data['CATEGORY'] == 0]['TYPE'].unique()
    ], axis=1)

    revenue = pd.concat([
        data[(data['CATEGORY'] == 1) & (data['TYPE'] == i)]
        .drop(columns=['CATEGORY', 'TYPE'])
        .resample(frequency)
        .sum()
        .rename(columns={'VALUE': f'{i}'})
        for i in data[data['CATEGORY'] == 1]['TYPE'].unique()
    ], axis=1)

    expenses.columns = pd.MultiIndex.from_product([['Expenses'], expenses.columns])
    revenue.columns = pd.MultiIndex.from_product([['Revenue'], revenue.columns])

    expenses['Expenses', 'TOTAL'] = expenses.sum(axis=1)
    revenue['Revenue', 'TOTAL'] = revenue.sum(axis=1)

    DATA = pd.concat([expenses, revenue], axis=1).fillna(0)

    DATA['TOTAL'] = DATA['Revenue', 'TOTAL'] - DATA['Expenses', 'TOTAL']

    if cycle == 'DAY':
        DATA.index = DATA.index.strftime('%Y-%m-%d')
    elif cycle == 'WEEK':
        DATA = DATA.groupby(DATA.index.to_period('W')).first()
        DATA.index = DATA.index.strftime('%Y-%m-%d')
    elif cycle == 'MONTH':
        DATA.index = DATA.index.strftime('%Y-%m')
    elif cycle == 'YEAR':
        DATA.index = DATA.index.strftime('%Y')

    DATA.index.name = cycle

    return DATA

def enrichData(df: pd.DataFrame) -> enrichedData:
    old_data = df.copy()
    
    def WoM(dt):
        first_day = dt.replace(day=1)
        dom = dt.day
        adjusted_dom = dom + first_day.weekday()
        return int(np.ceil(adjusted_dom / 7.0))
    
    df['CREATED_AT'] = pd.to_datetime(df['CREATED_AT'])
    df = df.drop(columns=['UPDATED_AT', 'TRANSACTION_ID', 'ITEM', 'USERNAME']).set_index('CREATED_AT').sort_index()

    expenses_list = [
        df[(df['CATEGORY'] == 0) & (df['TYPE'] == i)]
        .drop(columns=['CATEGORY', 'TYPE'])
        .resample('D')
        .sum()
        .rename(columns={'VALUE': f'{i}'})
        for i in df[df['CATEGORY'] == 0]['TYPE'].unique()
    ]

    expenses_list = [x for x in expenses_list if not x.empty]
    expenses = pd.concat(expenses_list, axis=1) if expenses_list else pd.DataFrame()

    revenue_list = [
        df[(df['CATEGORY'] == 1) & (df['TYPE'] == i)]
        .drop(columns=['CATEGORY', 'TYPE'])
        .resample('D')
        .sum()
        .rename(columns={'VALUE': f'{i}'})
        for i in df[df['CATEGORY'] == 1]['TYPE'].unique()
    ]
    revenue_list = [x for x in revenue_list if not x.empty]
    revenue = pd.concat(revenue_list, axis=1) if revenue_list else pd.DataFrame()

    if not expenses.empty:
        expenses = expenses.reindex(sorted(expenses.columns, key=lambda x: int(x)), axis=1)
        expenses.columns = pd.MultiIndex.from_product([['Expenses'], expenses.columns])
        expenses[('Expenses', 'TOTAL')] = expenses.sum(axis=1)
    
    if not revenue.empty:
        revenue = revenue.reindex(sorted(revenue.columns, key=lambda x: int(x)), axis=1)
        revenue.columns = pd.MultiIndex.from_product([['Revenue'], revenue.columns])
        revenue[('Revenue', 'TOTAL')] = revenue.sum(axis=1)
    else:
        revenue = pd.DataFrame(index=expenses.index)
        revenue[('Revenue', 'TOTAL')] = 0

    features = pd.DataFrame(index=expenses.index.union(revenue.index))
    datetime_index = pd.DatetimeIndex(features.index)

    features[("Features", "DoW")] = datetime_index.dayofweek
    features[("Features", "DoM")] = datetime_index.day
    features[("Features", "WoM")] = datetime_index.map(WoM)
    features[("Features", "DAY")] = datetime_index.dayofyear
    features[("Features", "WEEK")] = datetime_index.isocalendar().week
    features[("Features", "QUARTER")] = datetime_index.quarter
    features[("Features", "MONTH")] = datetime_index.month
    features[("Features", "YEAR")] = datetime_index.year

    DATA = pd.concat([expenses, revenue, features], axis=1).fillna(0)
    
    DATA.index.name = "DATE"
    DATA['TOTAL'] = DATA['Revenue', 'TOTAL'] - DATA['Expenses', 'TOTAL']

    return enrichedData(old_data, DATA)
