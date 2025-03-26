# Data Analysis Scripts

This repository contains Python scripts for data processing, binning, and model creation in hyperfine structure analysis. The scripts utilize **Pandas**, **NumPy**, and **SciPy** for data handling and statistical analysis. 

To run this code, you also need the **SATLAS - Statistical Analysis Toolbox for Laser Spectroscopy** package, which can be found at https://woutergins.github.io/satlas/

For more details about the experiment this analysis was created for, see **[ExperimentInfo.md](ExperimentInfo.md)**.

---
## Scripts
---
### **vals.py**  
Assigns values used across all scripts.

### **create_dataframe.py**  
- Creates a Pandas DataFrame from all `.csv` files in a given directory.  
- Cleans and processes the data.

### **binning.py**  
- Calls **create_dataframe.py** to access processed data.  
- Performs data binning on a given dataset to generate a histogram of counts per wavenumber.  
- Includes error handling using uncertainty propagation. 


### **model_creation.py**  

- Defines the `satlas_analysis` class for model creation and plotting.
- Calls **binning.py** for binned data 

#### **Methods**  
- **Plot_only** – Plots the model alongside the data.  
- **Chisquare_fit** – Plots the chi-square model.  
- **Residual_plot** – Plots the chi-square model, calculates residuals between the data and the model, and plots the residuals.  
- **Get_resultframe** – Performs chi-square fitting and returns a Pandas DataFrame of the result values.  


### **lineshapes.py**  
Calls **model_creation.py** to generate models for different lineshapes:  
- **Voigt**  
- **Gaussian**  
- **Lorentzian**  
- **Pseudo-Voigt**  
- **Crystal Ball**  
- **Asymmetric Lorentzian**

### **binsize_scan.py**  
- Calls **model_creation.py** to run chi-square fitting for different bin sizes.
#### **Functions**  
- **run_binsize_analysis** – Generates a `.csv` file of chi-square fitting variables for different bin sizes.  
- **binsize_plot** – Creates a 2×2 subplot with x-axis as bin size and y-axis as plot list values, including error bars.  

---

## Script Dependency Flow  

vals.py  →  {create_dataframe.py, binning.py, model_creation.py, lineshapes.py, binsize_scan.py}

create_dataframe.py  →  binning.py  →  model_creation.py  →  {lineshapes.py, binsize_scan.py}

---

## Usage
Each script can be run individually for different stages of analysis. 
