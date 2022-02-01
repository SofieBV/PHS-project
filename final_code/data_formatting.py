import pandas as pd

def import_all():
    """
    import all data that we have and put it into dataframe format with right column names
    """

    cancer_data_31 = pd.read_csv('data/31DayData.csv')
    cancer_data_62 = pd.read_csv('data/62DayData.csv')
    diagnostics_data_HB = pd.read_csv('data/diagnostics_by_board_september_2021.csv', sep=',', engine='python').sort_values('MonthEnding').reset_index(drop=True)
    diagnostics_data_scot = pd.read_csv('data/diagnostics_scotland_september_2021.csv', engine='python').sort_values('MonthEnding').reset_index(drop=True).rename(columns={'Country':'HBT'})
    cancellation_data = pd.read_csv('data/cancellations_by_board_november_2021.csv', engine='python').sort_values('Month').reset_index(drop=True)
    AE_data = pd.read_csv('data/monthly_ae_waitingtimes_202111.csv', engine='python').sort_values('Month').reset_index(drop=True)

    return cancer_data_31, cancer_data_62