import pandas as pd

def import_datasets(names):
    """
    import all data that we have and put it into dataframe format with right column names
    """

    dataframes = []
    time_names = ['Month', 'MonthEnding', 'Quarter', 'QuarterEnding', 'Date', 'Year']
    region_names = ['HB', 'HBT', 'Country']

    for name in names:
        dataframe = pd.read_csv('data/{}.csv'.format(name), engine='python')
        dataframe = dataframe.dropna(axis=1)
        
        indices = []
        for col in dataframe.columns:
            if col in time_names:
                time = col
                dataframe = dataframe.astype({col: 'object'})
            if col in region_names:
                region = col
            if dataframe[col].dtype == 'object':
                indices.append(col)
                
        dataframe = dataframe.sort_values(by = [time, region]).reset_index(drop=True).set_index(indices)        

        dataframes.append(dataframe)

    return dataframes


def month_to_quarter(dataframe):
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