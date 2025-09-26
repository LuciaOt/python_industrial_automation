# Screening datasets for laser welded steel-copper lap joints
## Description
**V1**:  
The data show a definitve screening design to evaluate the the influence of six factors (laser beam power (W), welding speed (m/min), angular position in welding direction (°), focal positon (mm), gas flow rate (l/min), material thickness of the steel sheet (mm)) in three levels and 18 parameter combinations on the weld depth and the geometrical dimensions of the weld metal in laser welded steel-copper joints in the lap configuration with steel on the top side. Every parameter combination was repeated 5 times and every sheet was cuttet 4 times to overall generate 360 cross sections. Every line in the dataset stands for a cross section which was evaluated regarding the dimensions of the weld metal. Additionally, there was a dichotomous data column added for cracking in the weld metal (yes/no). 
The dataset is not suitable for modelling a precise predicting model of weld depth in the copper sheet, but shows a correlation between cracking (yes/no) and the weld depth in the copper sheet. This can be discribed very well in a binominal logistic regression.
Moreover the average crack lenght and count of cracks was added in Versions V1.1 

**V2**:   
The data show the same screening experiments but with adjusted laser power levels to garantee sufficient weld depth for all parameter combinations (which was lacking in V1). The target is the average weld depth in the bottom copper sheet for every parameter combination. The data can be used to calculate the parameter effect strenght of the different factors on the weld depth and to build a simple linear model of the coherences between the parameters and the resulting weld depth. 
V2.1 ist basically the same dataset but with the resulting copper dilution instead of the weld depth.   

## Url 
https://data.mendeley.com/datasets/2s5m3crbkd/2
## Credits 
Rinne, Jonas (2021), “Screening datasets for laser welded steel-copper lap joints ”, Mendeley Data, V2, doi: 10.17632/2s5m3crbkd.2