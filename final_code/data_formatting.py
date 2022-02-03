import pandas as pd
import numpy as np

def import_datasets(names):
    """
    import all data that we have and put it into dataframe format with right column names
    """

    dataframes = []
    time_names = ['Month', 'Quarter', 'QuarterEnding', 'Date', 'Year']
    region_names = ['HB', 'HBT', 'Country']

    for name in names:
        dataframe = pd.read_csv('data/{}.csv'.format(name), engine='python')
        dataframe = dataframe.dropna(axis=1)
        
        indices = []
        for col in dataframe.columns:
            if col=='MonthEnding':
                dataframe=monthending_to_month(dataframe)
                indices.append('Month')
            elif col in time_names:
                time = col
                dataframe = dataframe.astype({col: 'object'})
                indices.append(col)
            elif col in region_names:
                region = col
                indices.append(col)
            elif dataframe[col].dtype == 'object':
                indices.append(col)
                
        dataframe = dataframe.sort_values(by = [time, region]).reset_index(drop=True).set_index(indices)        

        dataframes.append(dataframe)

    return dataframes

def monthending_to_month(dataframe):
    monthendings = list(map(str,dataframe['MonthEnding']))
    month = monthendings.copy()
    for i in range(len(monthendings)):
        month[i] = monthendings[i][:-2]
    dataframe['MonthEnding'] = month
    dataframe = dataframe.rename(columns={'MonthEnding':'Month'})
    
    return dataframe

def day_to_month(dataframe):
    indices = dataframe.index.names
    dataframe = dataframe.reset_index()
    dates = list(map(str,dataframe['Date']))
    month = dates.copy()
    for i in range(len(dates)):
        month[i] = dates[i][:-2]
    dataframe['Date'] = month
    dataframe = dataframe.set_index(indices).rename_axis(index={'Date':'Month'})
    dataframe = dataframe.groupby(dataframe.index.names).sum()

    return dataframe

def month_to_quarter(dataframe):
    indices = dataframe.index.names
    dataframe = dataframe.reset_index()
    months = list(map(str,dataframe['Month']))
    quarter = months.copy()
    for i in range(len(months)):
        if int(months[i][-1]) <= 3:
            quarter[i] = months[i][:-2]+'Q1'
        elif int(months[i][-1]) <= 6:
            quarter[i] = months[i][:-2]+'Q2' 
        elif int(months[i][-1]) <= 9:
            quarter[i] = months[i][:-2]+'Q3'
        else:
            quarter[i] = months[i][:-2]+'Q4'  
    dataframe['Month'] = quarter
    dataframe = dataframe.set_index(indices).rename_axis(index={'Month':'Quarter'})
    dataframe = dataframe.groupby(dataframe.index.names).sum()
    return dataframe

def day_to_quarter(dataframe):
    dataframe = day_to_month(dataframe)
    dataframe = month_to_quarter(dataframe)
    return dataframe

def HB_to_areas(dataframe):

    dataframe = dataframe.rename(index={'S08000020':'NCA','S08000022':'NCA', 'S08000025':'NCA', 'S08000026':'NCA', 'S08000030':'NCA', \
                                            'S08000028':'NCA', 'S08000016':'SCAN','S08000017':'SCAN','S08000029':'SCAN','S08000024':'SCAN', \
                                                'S08000015':'WOSCAN','S08000019':'WOSCAN','S08000031':'WOSCAN','S08000032':'WOSCAN'})
    
    dataframe = dataframe.groupby(dataframe.index.names).sum()

    return dataframe

def time_interval(dataframe, interval):
    time_names = ['Month', 'MonthEnding', 'Quarter', 'QuarterEnding', 'Date', 'Year']

    for ind in dataframe.index.names:
        if ind in time_names:
            newData = dataframe.loc[interval[0]:interval[1],:]

    return newData

def add_categories(dataframe, groupings):
    """
    add certain categories of the dataframe
    """
    dic={}
    for key,value in groupings.items():
        for x in value:
            dic[x] = key

    dataframe = dataframe.rename(index=dic)
    dataframe = dataframe.groupby(dataframe.index.names).sum()

    return dataframe

def extract_data(dataframe, indices, levels, names):
    output = []
    for name in names:
        data = dataframe.xs(indices,level=levels)[name].reset_index().to_numpy().T
        data = data.astype('object')
        data[0,:] = data[0,:].astype(np.str)
        output.append(data)
    if len(output)==1:
        return output[0]
    else:
        return output
