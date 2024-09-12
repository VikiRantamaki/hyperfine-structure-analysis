import pandas as pd
import os
import numpy as np
from scipy.constants import physical_constants
from vals import path, m, vm


c = physical_constants['speed of light in vacuum'][0]
MHz_to_invcm = 10**6/c*0.01

#Create a DataFrame 
def df(path, m, vm):
    '''
    Creates a Pandas DataFrame 
    Merge multiple CSV files with corresponding metadata files into a single Pandas DataFrame sorted by 'timestamp' column. 
    Cleans and processes the data.

    Parameters
    ----------
    path : str
        The directory path where the `.csv` and corresponding `.txt` files are located.
    m : float 
        Mass of the given isotope in units of eV/c^2
    vm : float 
        iscool voltage multiplier
    
    Returns
    ----------
    pd.DataFrame
    timestamp_mean: float
    '''

    def func(path):
        '''
        Returns a merged DataFrame containing data from all `.csv` files in the directory, sorted by the 'timestamp' column.
        
        Raises
        ----------
        FileNotFoundError: If a `.csv` or corresponding `.txt` file is not found in the directory.
        '''

        dir = os.fsencode(path)
        df_list = list()

        #Search for files ending with .csv and save them into files list 
        for file in os.listdir(dir):
            filename = os.fsdecode(file)
            if filename.endswith(".csv"):
                #Get column names from corresponding txt file 
                txt = filename[:-len('.csv')]
                txt = "metadata_" + txt + '.txt'
            
                colnames = np.loadtxt(path + '/' + txt, delimiter=',', skiprows=2, dtype=str)

                filters = {ord('['): None, ord(']'): None, ord('"'): None, ord(' '): None, ord("'"): None}
                colnames = [s.translate(filters) for s in colnames]
                
                #Create DataFrame
                df = pd.read_csv(path + "/" + filename, delimiter=';', names=colnames)
                df_list.append(df)

            else:   
                continue
        
        pd.set_option('display.max_columns',None)
        
        #Merge DataFrames in df_list into one and sort by timestamp column   
        df = pd.concat(df_list)
        df = df.sort_values('timestamp')     
        
        return df

    #Create DataFrame
    df = func(path)
    
    pd.set_option("display.precision", 35)

    #Fill NaN values with the last (or next) valid value for each column except events_per_bunch
    for column in df:
        if column == 'events_per_bunch':
            continue
        else: 
            df[column] = df[column].ffill()
            df[column] = df[column].bfill()

    #Delete all rows where events_per_bunch = NaN
    df = df.dropna(subset=['events_per_bunch'])  

    #Calculate the mean timestamp
    timestamp_mean = df['timestamp'].mean()

    #Change index to timestamp
    df.set_index('timestamp', inplace=True)

    #Multiply iscool voltage by vm
    df['voltage']=df['voltage'].apply(lambda x: x*vm)

    #Laser diode correction (Rb transition = 384228115.20352034 THz)
    Rb_trans = 384228115.210*MHz_to_invcm 
    df["diode_cor"] = Rb_trans - df["wavenumber_2"]
    df["wavenumber_3"] = df["wavenumber_3"] + df["diode_cor"]

    #Convert delta_t values from 0.5 ms to 1 mus by dividing by 2000
    df['delta_t']=df['delta_t'].apply(lambda x: x/2000)

    #Calculate the doppler shift 
    def beta(V,m):
        return np.sqrt(1-m**2/(V+m)**2)

    df['wavenumber_1'] = df['wavenumber_1']*(1-beta(df['voltage'],m))/(np.sqrt(1-beta(df['voltage'],m)**2))
    df['wavenumber_3'] = df['wavenumber_3']*(1-beta(df['voltage'],m))/(np.sqrt(1-beta(df['voltage'],m)**2))
    df['wavenumber_4'] = df['wavenumber_4']*(1-beta(df['voltage'],m))/(np.sqrt(1-beta(df['voltage'],m)**2))

    #Display the drift correction
    #plt.plot(df.index, df["diode_cor"], 'r--')
    #plt.xlabel('timestamp (s)')
    #plt.ylabel('Diode correction ($cm^{-1}$)')
    #plt.show()    

    return df, timestamp_mean
