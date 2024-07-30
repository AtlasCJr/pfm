import pandas as pd

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

    data['CREATED_AT'] = pd.to_datetime(data['CREATED_AT'])
    data = data.drop(columns=['UPDATED_AT', 'TRANSACTION_ID', 'ITEM', 'USERNAME'])
    data = data.set_index('CREATED_AT')

    frequency = {'DAY': 'D', 'WEEK': 'W', 'MONTH': 'M', 'YEAR': 'Y'}[cycle]

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

    data = data[(data.index >= start_date) & (data.index <= end_date)]

    expense_types = data[data['CATEGORY'] == 0]['TYPE'].unique()
    revenue_types = data[data['CATEGORY'] == 1]['TYPE'].unique()

    expenses_resampled = pd.concat([
        data[(data['CATEGORY'] == 0) & (data['TYPE'] == i)]
        .drop(columns=['CATEGORY', 'TYPE'])
        .resample(frequency)
        .sum()
        .rename(columns={'VALUE': f'{i}'})
        for i in expense_types
    ], axis=1)

    revenue_resampled = pd.concat([
        data[(data['CATEGORY'] == 1) & (data['TYPE'] == i)]
        .drop(columns=['CATEGORY', 'TYPE'])
        .resample(frequency)
        .sum()
        .rename(columns={'VALUE': f'{i}'})
        for i in revenue_types
    ], axis=1)

    if not expenses_resampled.empty:
        expenses_resampled.columns = pd.MultiIndex.from_product([['Expenses'], expenses_resampled.columns])
    if not revenue_resampled.empty:
        revenue_resampled.columns = pd.MultiIndex.from_product([['Revenue'], revenue_resampled.columns])

    resampled_data = pd.concat([expenses_resampled, revenue_resampled], axis=1).fillna(0)

    if not resampled_data.empty:
        resampled_data['Expenses', 'TOTAL'] = resampled_data['Expenses'].sum(axis=1)
        resampled_data['Revenue', 'TOTAL'] = resampled_data['Revenue'].sum(axis=1)
        resampled_data['TOTAL'] = resampled_data['Revenue', 'TOTAL'] - resampled_data['Expenses', 'TOTAL']

    if cycle == 'DAY':
        resampled_data.index = resampled_data.index.strftime('%Y-%m-%d')
    elif cycle == 'WEEK':
        resampled_data = resampled_data.groupby(resampled_data.index.to_period('W')).first()
        resampled_data.index = resampled_data.index.strftime('%Y-%m-%d')
    elif cycle == 'MONTH':
        resampled_data.index = resampled_data.index.strftime('%Y-%m')
    elif cycle == 'YEAR':
        resampled_data.index = resampled_data.index.strftime('%Y')

    resampled_data.index.name = cycle

    return resampled_data
