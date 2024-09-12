from turtle import shape
from scipy.constants import physical_constants
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import satlas as sat
from binning import data_binning
from vals import ml, scan, m, path, vm, binsize, spins_gs, hyperfine_factors_gs_12, lineshapes

class satlas_analysis:
    '''Model creation and plotting
    Functions
    --------
    Plot_only 
        Plot model together with data
    Chisquare_fit
        Plot chisquare model
    Residual_plot 
        Plot chisquare model, calculate residuals between the data and the model and plot residuals
    Get_resultframe
        Does the chisquare fitting and returns a pandas dataframe of the result values
        '''

    def __init__(self, path, m, vm, ml, binsize, scan='Unknown scan', wavenumber='wavenumber_3', shape='voigt', pseudovoigtparams={'Eta': 0.5, 'A': 0}): 
        #path: file path, m: mass in eV/c**2, vm: iscool voltage multiplier, ml: mass number
        self.path = path
        self.m = m
        self.vm = vm
        self.ml = ml
        self.binsize = binsize *0.0000334 # converts from MHz to 1/cm
        self.scan = scan
        self.wavenumber = wavenumber
        self.shape = shape
        self.pseudovoigtparams = pseudovoigtparams
        self.transition = 25347.756
        self.freq_multi = 2

        self.x, self.y, self.yerr, self.t_mean = data_binning(self.path, self.m, self.vm, self.binsize, self.wavenumber) 

        #SATLAS PARAMETERS
        MASS = int(self.ml)
        self.I = spins_gs[MASS]
        self.J = [1/2, 1/2]
        self.ABC = hyperfine_factors_gs_12[MASS] 
        self.fwhm = lineshapes[self.shape] 
        self.bkg = [self.y.min()]
        self.scale = self.y.max()-self.y.min()
        self.centroid = 0

        print('**********************************************')
        print('')
        print('Lineshape : ', self.shape)
        print('')
        print('')
        print('FWHM : ', lineshapes[self.shape])
        print('')
        print('**********************************************')


    def Create_model(self):
        x = (self.x* self.freq_multi - self.transition) * 29979.2458
        y = self.y
        yerr = self.yerr
        
        return x, y, yerr, sat.HFSModel(I = self.I, J = self.J, ABC = self.ABC, centroid = self.centroid, fwhm = self.fwhm, background_params = self.bkg, shape=self.shape, use_racah = False, scale = self.scale, pseudovoigtparams = self.pseudovoigtparams, asymmetryparams={'a': 0})

    def Plot_only(self):
        x, y, yerr, model = self.Create_model()

        se = np.arange(x.min(), x.max(), 0.1)

        plt.errorbar(x, y, yerr = yerr, fmt = '.', zorder = 1, label = 'Data')
        plt.plot(se, model(se), 'r-', zorder = 2, label = 'Initial Fit')
        plt.fill_between(se, min(model(se)), model(se), facecolor = 'coral', alpha=0.5)
        plt.ylabel('Counts')
        plt.xlabel('Frequency (MHz)')
        plt.title('Hyperfine Spectra of ' + ml + '-Al' + ' (' + self.scan + ')')
        plt.legend()
        plt.show()

    
    def Residual_plot(self):
        x, y, yerr, model = self.Create_model()

        se = np.arange(x.min(), x.max(), 0.1)
        sat.chisquare_fit(model, x, y, yerr = yerr)
        model.display_chisquare_fit(show_correl = False)
        model.plot(x, y, yerr=yerr, ax=plt.subplot(2,1,1), show=False)
        plt.fill_between(se, min(model(se)), model(se), facecolor = 'coral', alpha=0.5)
        plt.legend()
        plt.title('Hyperfine Spectra of ' + ml + '-Al' + ' ( ' + self.scan + ' ), \n Lineshape: ' + self.shape + ' ' + str(self.pseudovoigtparams))
        plt.ylabel('Count rate')
        plt.xlabel('')
        
        res = y - model(x)
        plt.subplot(2,1,2)
        plt.scatter(x,res) #, label = 'residual between model and data')
        plt.axhline(y=0, color='r', linestyle='-')
        plt.grid()
        plt.ylabel('Residual')
        plt.xlabel('Frequency (MHz)')
        plt.legend()
        
        plt.show()

    def Get_resultframe(self):
        x, y, yerr, model = self.Create_model()

        sat.chisquare_fit(model, x, y, yerr = yerr)
        model.display_chisquare_fit(show_correl = False)
        result_frame = model.get_result_frame(scaled = False)
        return result_frame, self.t_mean
    
    def Chisquare_fit(self):
        x, y, yerr, model = self.Create_model()

        se = np.arange(x.min(), x.max(), 0.1)
        sat.chisquare_fit(model, x, y, yerr = yerr)
        model.display_chisquare_fit(show_correl = False)
        model.plot(x, y, yerr=yerr, show=False)
        plt.fill_between(se, min(model(se)), model(se), facecolor = 'coral', alpha=0.5)
        plt.legend()
        plt.title('Hyperfine Spectra of ' + ml + '-Al' + ' ( ' + self.scan + ' )')
        plt.ylabel('Count rate')
        plt.xlabel('')
        plt.show()

    def lit_values(self):
        x, y, yerr, model = self.Create_model()

        A_ratio = self.ABC[1] / self.ABC[0]
        model.fix_ratio(A_ratio, target='upper', parameter='A')

        se = np.arange(x.min(), x.max(), 0.1)
        sat.chisquare_fit(model, x, y, yerr = yerr)
        model.display_chisquare_fit(show_correl = False)
        result_frame = model.get_result_frame(scaled = False)
        
        """model.plot(x, y, yerr=yerr, ax=plt.subplot(2,1,1), show=False)
        plt.fill_between(se, min(model(se)), model(se), facecolor = 'coral', alpha=0.5)
        plt.legend()
        plt.title('Hyperfine Spectra of ' + ml + '-Al' + ' ( ' + self.scan + ' )')
        plt.ylabel('Count rate')
        plt.xlabel('')

        res = y - model(x)
        plt.subplot(2,1,2)
        plt.scatter(x,res) #, label = 'residual between model and data')
        plt.axhline(y=0, color='r', linestyle='-')
        plt.grid()
        plt.ylabel('Residual')
        plt.xlabel('Frequency (MHz)')
        plt.legend()
        plt.show()"""
        return result_frame, self.t_mean





