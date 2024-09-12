from cmath import nan
from lib2to3.pygram import pattern_grammar
from model_creation import satlas_analysis
from lampi import ml, m, vm, binsize, scan_binsize, lineshapes
import pandas as pd
import matplotlib.pyplot as plt


class hai():
    def __init__(self, m, vm, ml, lineshapes, scan_list, plot_list = ['FWHM', 'Centroid', 'Al', 'Au', 'A-ratio'], filename = ml, Constrained_A = False):
        #path: file path, m: mass in eV/c**2, vm: iscool voltage multiplier, ml: mass number
        self.m = m
        self.vm = vm
        self.ml = ml
        self.scan_list = scan_list
        self.plot_list = plot_list
        self.filename = filename
        self.lineshapes = lineshapes
        self.constrained_A = Constrained_A

    def get_result_frame(self, shape):                                                                         
        df_list = list()

        #Create hfsmodel for different lineshapes
        
        for scan in self.scan_list:
            path = "data/" + ml + "/" + scan
            result_frame = satlas_analysis(path, self.m, self.vm, self.ml, self.scan_list[scan], scan, shape=shape, pseudovoigtparams={'Eta': 0.5, 'A': 0})
            result_frame, t_mean = result_frame.lit_values()
            #result_frame, t_mean = result_frame.Get_resultframe()
            
            result_frame.insert(0, 'binsize', self.scan_list[scan])
            result_frame.insert(0, 'tMean', t_mean)
            result_frame.insert(0, 'Scan', scan)

            #Add A-ratio
            result_frame['A-ratio'] = result_frame['Au', 'Value']/result_frame['Al', 'Value']

            df_list.append(result_frame)

        df = pd.concat(df_list)
        df = df.sort_values('tMean')
        df.fillna(0)
        return df

    def get_result_frame_pseudovoigt(self):                                                                         
        df_list = list()

        #Create hfsmodel for different lineshapes
        
        for eta in [0, 0.25, 0.5, 1]:
                
            for scan in self.scan_list:
                print('Eta : ', eta)
                print('scan : ', scan)
                path = "data/" + ml + "/" + scan
                result_frame = satlas_analysis(path, self.m, self.vm, self.ml, self.scan_list[scan], scan, shape='pseudovoigt', pseudovoigtparams={'Eta': eta, 'A': 0})
                print('model done')
                if self.constrained_A:
                    print('A constrained = True')
                    result_frame, t_mean = result_frame.lit_values()
                else:
                    print('A not constrained')
                    result_frame, t_mean = result_frame.Get_resultframe()
                
                dict = {'binsize' : self.scan_list[scan], 'tMean' : t_mean, 'Scan': scan, 'setted Eta' : eta}
                print('dict = ', dict)
                for name in dict:
                    result_frame.insert(0, name, dict[name])
                
                #Add A-ratio
                result_frame['A-ratio'] = result_frame['Au', 'Value']/result_frame['Al', 'Value']

                df_list.append(result_frame)

        df = pd.concat(df_list)
        df = df.sort_values('tMean')
        df.fillna(0)
        
        return df


    #rename unnamed columns 
    def rename_unnamed(self, df):  
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

    def write_result_frame(self):
        for shape in self.lineshapes: 
            df = self.get_result_frame_pseudovoigt()
            if shape == 'voigt':
                df = df.rename(columns={'TotalFWHM' : 'FWHM'})
            if self.constrained_A:
                df.to_csv( self.filename +'_' + shape + '_ConstA.csv', index=False)
            else:
                df.to_csv( self.filename +'_' + shape + '.csv', index=False)
            #Voigtin kanssa voi tulla ongelmia, koska kirjoittaa TotalFWHM ja plotissa silmukka FWHMn yli.
        

    def plot(self):

        for name in self.plot_list:
            plt.figure()
            print('*************************************')
            print(' ')
            print(name)
            print(' ')

            
            for shape in self.lineshapes:
                    df = pd.read_csv(self.filename +'_' + shape + '_ConstA.csv', header  =[0,1], delimiter = ',')
                    df = self.rename_unnamed(df)
            
                    x = df['tMean', '']
                
                    if name == 'A-ratio':
                        y = df[name, '']
                        plt.scatter(x, y, label = shape)
                        plt.title(name + ', Constrained A')
                        plt.xlabel('t_Mean') 
                        plt.legend()       
                    else:
                        y = df[name, 'Value']
                        yerr = df[name, 'Uncertainty']
                        plt.errorbar(x, y, yerr, fmt='o', label = shape)
                        plt.title(name + ', Constrained A')
                        plt.xlabel('t_Mean') 
                        plt.legend()
            print('*************************************')

            plt.show()

    def plot_pseudovoigt(self):

        df = pd.read_csv(self.filename +'_pseudovoigt.csv', header  =[0,1], delimiter = ',')
        df = self.rename_unnamed(df)

        for name in self.plot_list:
            plt.figure()
            print('*************************************')
            print(' ')
            print(name)
            print(' ')

            for eta in [0, 0.25, 0.5, 1]:
                df_new = df[df['setted Eta'] == eta]
            
                x = df_new['tMean', '']
                
                if name == 'A-ratio':
                    y = df_new[name, '']
                    plt.scatter(x, y, label = "Eta: "+str(eta))
                    plt.title(name)
                    plt.xlabel('t_Mean') 
                    plt.legend()       
                else:
                    y = df_new[name, 'Value']
                    yerr = df_new[name, 'Uncertainty']
                    plt.errorbar(x, y, yerr, fmt='o', label = "Eta: "+str(eta))
                    plt.title(name)
                    plt.xlabel('t_Mean') 
                    plt.legend()
            print('*************************************')  
                
            plt.show()


hai = hai(m, vm, ml, lineshapes, scan_list=scan_binsize, Constrained_A = False) 
#hai.write_result_frame()
#hai.plot()
hai.plot_pseudovoigt()

