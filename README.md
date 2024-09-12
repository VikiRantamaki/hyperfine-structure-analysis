# hyperfine-structure-analysis
**Analysis of experimental data from an experiment on radioactive aluminum isotopes at CERN**

The experiment aimed to measure changes in the mean-squared nuclear charge radii of the short-lived isotopes 
<sup>33</sup>Al and <sup>34</sup>Al. These isotopes have extreme neutron-to-proton ratios and very short half-lives. The changes in the mean-squared nuclear charge radii can be calculated  with the isotope shift that is extracted from the hyperfine structures of a reference isotope and the isotope of study. 

The hyperfine structures of these isotopes were studied using the CRIS technique. In this technique, the ion beam from ISOLDE is neutralized in a hot charge exchange cell filled with potassium vapor. Neutral atoms then travel to the interaction region, while remaining ions are deflected from the beam. In the interaction region, where the atom beam is overlapped collinearly with a series of laser beams, the  atoms are firstly resonantly excited and then ionized. The frequency of the first excitation laser is constantly scanned during the experiment and the second non-resonant laser will then ionize those excited atoms which are then deflected on to the ion detector. The hyperfine structure can be reconstructed by plotting the ion count rate against excitation laser frequency.

My goal was to analyse the data for the reference isotope <sup>27</sup>Al with the SATLAS (Statistical Analysis Toolbox for Laser Spectroscopy) Python package which was made especially for analysing experimental data from laser spectroscopy experiments. 
For hyperfine spectra, I plotted the frequency and ion count rate with the model created with the SATLAS package and also the residual between model and data. Next step was to analyse how hyperfine A-parameter, centroid and full width at half maximum (FWHM) change over time with and without constraining the ratio of  A-parameters of the upper and lower electronic states using literature values. In the figure below, FWHM is plotted against time with and without constraining the ratio of A-parameters using literature values.

![27_FWHM](https://github.com/user-attachments/assets/ba5d649d-5c37-4ab4-8822-b3bb7e2f9868)

The hyperfine A-parameter is defined as the ratio between magnetic dipole moment &mu;, magnetic field _B<sub>0</sub>_ created by electrons in vicinity of the nucleus, and nuclear spin _I_ and angular momentum of the electronic state _J_, as _A_= &mu; _B<sub>0</sub>_ / _IJ_. Since the A-parameter depends on _B<sub>0</sub>_ and _J_, which are characteristic for each electronic state, the A-parameter varies between electronic states in an atom. The A-parameter quantifies how much an electronic state splits into hyperfine substates due to the presence of a nuclear magnetic dipole moment. The A-ratio is the ratio between the upper and lower states probed in the experiment. 

The last step in my project was to compare how different lineshape choices for the model affects the A-parameters, centroid and FWHM. I created the model and calculated the parameters with 5 different lineshapes: Voigt, which is a convolution of a Gaussian and Lorentzian function, Gaussian, Lorentzian, pseudo-Voigt and assymetric Lorentzian. From here the analysis could be continued by choosing the best lineshape corrections and also considering some systematic corrections as a function of time. After that we can start analysing data from <sup>33-34</sup>Al scans and calculating the isotope shift. 

Controlling the systematic effects in this experiment is really important as extracting the aluminium nuclear charge radii from the isotope shifts requiers very high precision. Understanding the centroid shifts and how lineshape choices is requirement to extract accurate charge radii for these weakly bound nuclei. Such information of the nuclear charge radius is important to understand the details of the strong nuclear interaction.  

Here is the resulting hyperfine spectra of <sup>27</sup>Al and the residual plot between model and data.
![4503_hfspectra](https://github.com/user-attachments/assets/3efd294c-8d4f-4cac-a7fd-fd50cbb6f7b7)
