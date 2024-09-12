# Assign values for the analysis of aluminum isotopes

# Location of the data folder "ml/scan"
ml = "27"
scan = "scan_4477"
path = "data/" + ml + "/" + scan

m = 25.133144105267924*10**9    # mass of the given isotope in units of eV/c^2
#m = 25.133142783695394888*10**9
vm = 5963.39    # iscool voltage multiplier
binsize  = 25   # in MHz #*0.0000334
wavenumber = 'wavenumber_3'

scan_binsize ={
    'scan_4433' : 25, 
    'scan_4438' : 25,
    'scan_4442' : 15, 
    'scan_4445' : 20, 
    'scan_4446' : 20, 
    'scan_4448' : 20, 
    'scan_4452' : 20, 
    'scan_4458' : 20, 
    'scan_4460' : 25, 
    'scan_4466' : 20, 
    'scan_4467' : 20, 
    'scan_4477' : 25, 
    'scan_4478' : 25, 
    'scan_4503' : 25, 
    'scan_4508' : 25, 
    'scan_4513' : 20
    }

# Spins for the ground state of aluminum isotopes
# Key: Mass number, Value: Nuclear spin
spins_gs = {
    26: 5,
    27: 5/2,
    28: 3,
    29: 5/2,
    30: 3,
    31: 5/2,
    32: 1, 
    33: 5/2, 
    34: 4
    }

# The hyperfine structure constants of aluminum isotopes 
# Key: Mass number, Values: List of hyperfine parameters  
hyperfine_factors_gs_12 = {
    26: [193.88, 166.28,0,0,0,0],
    27: [503.58,431.89,0,0,0,0], 
    28: [373.61, 320.42, 0, 0, 0, 0],
    29: [506.83, 434.68, 0, 0, 0, 0],
    30: [346.87, 297.49, 0, 0, 0, 0],
    31: [529.65, 454.25, 0, 0, 0, 0], 
    32: [674.85, 578.78, 0, 0, 0, 0], 
    33: [565.33, 484.84, 0, 0, 0, 0], 
    34: [186.34, 159.82, 0, 0, 0, 0]
    }

# Lineshapes for model creation
lineshapes = {
    'voigt' : [100,100],
    'gaussian' : 100,
    'lorentzian' : 100,
    'pseudovoigt' : 100,
    #'crystalball' : 100,
    'asymmlorentzian' : 100
    }
