from model_creation import satlas_analysis
from lampi import ml, scan, m, path, vm
import pandas as pd
import matplotlib.pyplot as plt

filename = 'binsize_' + scan + '.csv'
plot_list = ['TotalFWHM', 'Centroid', 'Al', 'Au']
binsize = 5
endpoint = 40

def run_binsize_analysis(path, m, vm, ml, filename, binsize, endpoint): 
    '''
    Creates a csv file of chisquare fitting variables for different binsizes

    Parameters
    ----------
    path : str
        The directory path where the `.csv` and corresponding `.txt` files are located.
    m : float 
        Mass of the given isotope in units of eV/c^2
    vm : float 
        Iscool voltage multiplier
    ml : str
        Mass number
    filename : str
        Filename for saving the result frames 
    binsize : int
        Initial binsize
    endpoint : int
        Final binsize
    '''
    #df_list = list()

    result_frame = satlas_analysis(path, m, vm, ml, binsize)

    result_frame = result_frame.Get_resultframe()

    result_frame.insert(0, 'binsize', binsize)
    #df_list.append(result_frame)
    result_frame.to_csv(filename, index= False)
    binsize +=5

    while binsize<=endpoint:
        result_frame = satlas_analysis(path, m, vm, ml, binsize)
        
        result_frame = result_frame.Get_resultframe()
        
        result_frame.insert(0, 'binsize', binsize)
        result_frame.to_csv(filename, header = False, index = False, mode ='a')
        #df_list.append(result_frame)
        binsize +=5


def binsize_plot(filename, plot_list):
    '''
    Creates 2x2 subplot with x: binsize, y: plot_list value together with the related errorbars 

    Parameters
    ----------
    filename : str
        csv filename or path
    plot_list : list of str 
        List of exactly 4 column names to plot  
    '''
    
    df = pd.read_csv(filename, header=[0,1]) #csv to pandas
    pd.set_option('display.max_columns',None)  
    
    #rename unnamed columns 
    def rename_unnamed(df):  
        for i, columns in enumerate(df.columns.levels):
            columns_new = columns.tolist()
            for j, row in enumerate(columns_new):
                if "Unnamed: " in row:
                    columns_new[j] = ""
            if pd.__version__ < "0.21.0":  
                df.columns.set_levels(columns_new, level=i, inplace=True)
            else:
                df = df.rename(columns=dict(zip(columns.tolist(), columns_new)),
                            level=i)
        return df
    
    df = rename_unnamed(df)

    fig, axes = plt.subplots(2,2)
    axes = axes.ravel()
    fig.suptitle(scan)
        
    for i, name in enumerate(plot_list):
        x = df['binsize', '']
        y = df[name, 'Value']
        yerr = df[name, 'Uncertainty']
        axes[i].errorbar(x, y, yerr, fmt='o', label=name)
        axes[i].legend()
        

    fig.text(0.5, 0.02, 'Binsize', ha='center')
    plt.show()
