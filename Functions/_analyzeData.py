import pandas as pd
from matplotlib import pyplot as plt

def getTimeCycle(data:pd.DataFrame, cycle:str) -> pd.DataFrame:
    """
    Groups the data by the specified time cycle (Day, Week, Month, Year).
    """
    if cycle not in ["DAY", "WEEK", "MONTH", "YEAR"]:
        return
    
    data['CREATED_AT'] = pd.to_datetime(data['CREATED_AT'])
    data = data.drop(columns=['UPDATED_AT', 'TRANSACTION_ID', 'USER_ID'])

    data = data.set_index('CREATED_AT')
    
    if cycle == "DAY":
        resampled_data = data.resample('D').sum()
    elif cycle == "WEEK":
        resampled_data = data.resample('W').sum()
    elif cycle == "MONTH":
        resampled_data = data.resample('M').sum()
    elif cycle == "YEAR":
        resampled_data = data.resample('Y').sum()

    return resampled_data