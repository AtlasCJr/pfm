import pandas as pd

def getTimeCycle(data: pd.DataFrame, cycle: str) -> pd.DataFrame:
    """
    Groups the data by the specified time cycle (Day, Week, Month, Year).

    Parameters:
    data (pd.DataFrame): The input DataFrame with a 'CREATED_AT' column.
    cycle (str): The time cycle to group by. Allowed values are "DAY", "WEEK", "MONTH", "YEAR".

    Returns:
    pd.DataFrame: The DataFrame grouped by the specified time cycle.
    """
    if cycle not in ["DAY", "WEEK", "MONTH", "YEAR"]: return

    data['CREATED_AT'] = pd.to_datetime(data['CREATED_AT'])
    data = data.drop(columns=['UPDATED_AT', 'TRANSACTION_ID', 'USER_ID', 'ITEM'])
    data = data.set_index('CREATED_AT')

    frequency = {'DAY': 'D', 'WEEK': 'W', 'MONTH': 'M', 'YEAR': 'YE'}[cycle]

    expense_types = data[data['CATEGORY'] == 0]['TYPE'].unique()
    revenue_types = data[data['CATEGORY'] == 1]['TYPE'].unique()


    expenses_resampled = [
        data[(data['CATEGORY'] == 0) & (data['TYPE'] == i)]
        .drop(columns=['CATEGORY', 'TYPE'])
        .resample(frequency)
        .sum()
        .rename(columns={'VALUE': f'{i}'})
        for i in expense_types
    ]

    revenue_resampled = [
        data[(data['CATEGORY'] == 1) & (data['TYPE'] == i)]
        .drop(columns=['CATEGORY', 'TYPE'])
        .resample(frequency)
        .sum()
        .rename(columns={'VALUE': f'{i}'})
        for i in revenue_types
    ]

    expenses_concat = pd.concat(expenses_resampled, axis=1)
    revenue_concat = pd.concat(revenue_resampled, axis=1)

    expenses_concat.columns = pd.MultiIndex.from_product([['Expenses'], expenses_concat.columns])
    revenue_concat.columns = pd.MultiIndex.from_product([['Revenue'], revenue_concat.columns])

    resampled_data = pd.concat([expenses_concat, revenue_concat], axis=1).fillna(0)

    resampled_data['Expenses', 'TOTAL'] = resampled_data['Expenses'].sum(axis=1)
    resampled_data['Revenue', 'TOTAL'] = resampled_data['Revenue'].sum(axis=1)
    resampled_data['TOTAL'] = resampled_data['Revenue', 'TOTAL'] - resampled_data['Expenses', 'TOTAL']


    if cycle == 'DAY':
        resampled_data.index = resampled_data.index.strftime('%Y-%m-%d')
    elif cycle == 'WEEK':
        resampled_data.index = resampled_data.index.strftime('%Y-%W')
    elif cycle == 'MONTH':
        resampled_data.index = resampled_data.index.strftime('%Y-%m')
    elif cycle == 'YEAR':
        resampled_data.index = resampled_data.index.strftime('%Y')

    resampled_data.index.name = cycle

    return resampled_data