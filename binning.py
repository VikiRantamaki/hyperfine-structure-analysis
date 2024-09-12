from sqlite3 import Timestamp
import numpy as np 
import pandas as pd 
import create_dataframe
from vals import path, m, vm, binsize
from uncertainties import unumpy
import matplotlib.pyplot as plt

def data_binning(path, m, vm, binsize, wavenumber):
    '''
    Perform data binning on a given dataset to produce a histogram of counts per wavenumber 
    with error handling using uncertainty propagation.

    Parameters
    ----------
    path : str
        The file path to the dataset containing wavenumber and event counts
    m : float 
        Mass of the given isotope in units of eV/c^2
    vm : float 
        Iscool voltage multiplier
    binsize : int
        Binsize in MHz
    wavenumber : str
        The column name for the wavenumber data in the dataset

    Returns
    -------
    x : numpy.ndarray
        Array of binned wavenumber centers for the histogram
    y : numpy.ndarray
        Array of normalized counts per bin (with error handling)
    yerr : numpy.ndarray
        Array of uncertainties in the binned counts
    timestamp_mean : float
        The mean timestamp from the data
    '''

    np.set_printoptions(precision=30)

    df, timestamp_mean = create_dataframe.df(path, m, vm)

    wn = df[wavenumber].to_numpy()
    counts = df['events_per_bunch'].to_numpy()
    valid_wn_low = np.where(wn >= 500)
    lowerbin = wn[valid_wn_low].min()
    upperbin = wn.max()

    bins = np.arange(lowerbin, upperbin + binsize, binsize)

    y, spectrum_edges  = np.histogram(wn, bins, weights=counts)
    y = unumpy.uarray(y, np.sqrt(y))
    y2, _ = np.histogram(wn, bins)
    y2 = unumpy.uarray(y2, np.sqrt(y2))
    y[y==0] = np.nan
    y2[y2==0] = np.nan
    y = y / y2
    spectrum_centres = spectrum_edges[:-1] + np.diff(spectrum_edges)/2

    #remove NaN values
    spectrum_centres, y = spectrum_centres[~unumpy.isnan(y)], y[~unumpy.isnan(y)]

    spectrum = y
    x = spectrum_centres
    y = unumpy.nominal_values(spectrum)
    yerr = unumpy.std_devs(spectrum)

    return x,y,yerr,timestamp_mean
