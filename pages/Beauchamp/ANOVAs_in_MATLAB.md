---
title: ANOVAs in MATLAB
parent: Beauchamp
---
# ANOVAs in MATLAB

While all of your data may be in Excel, unfortunately, the Excel for Mac doesn't do ANOVAs.

So, let's use MATLAB! In this example, I'm doing a 2x2 ANOVA on the BOLD amplitudes of response in the right STS (dependent measure).

The two factors are perceiver group (strong McGurk perceivers are '1' and non-perceivers are '2') and stimulus condition (McGurk is '1', non-McGurk incongruent is '2', and congruent is '3').

I'd like to know if there is a significant difference in the right STS response between the subjects who did and did not perceive the McGurk effect,
between the responses to the 3 different stimuli,
and if there is an interaction between perceiver group and stimulus type.

The data for the dependent measure and each factor are put into columns in Excel.

```
R_STS	PerceiverGroup	StimulusType				
0.1662	1	           1				
0.0467	1	           1				
0.1364	1	           1				
-0.0025	1	           1				
0.0185	1	           1				
0.1162	1	           1				
0.1935	1	           1				
0.2685	2	           1				
0.0704	2	           1				
0.3541	2	           1				
0.1392	2	           1				
0.2367	2	           1			
0.0507	2	           1			
-0.0558	2	           1			
0.0738	2	           1			
0.0473	2	           1			
0.0119	2	           1			
0.1375	1	           2			
0.1354	1	           2			
0.1931	1	           2			
-0.26	1	           2			
0.0425	1	           2			
0.2904	1	           2			
0.3069	1	           2			
0.4702	2	           2			
-0.0295	2	           2			
0.391	2	           2			
0.2323	2	           2			
0.6401	2	           2			
0.0562	2	           2			
0.0488	2	           2			
0.0567	2	           2			
0.0635	2	           2			
-0.0592	2	           2			
0.1264	1	           3			
0.1002	1	           3			
0.1368	1	           3			
-0.0933	1	           3			
0.0391	1	           3			
0.2585	1	           3			
0.1405	1	           3			
-0.002	2	           3			
0.0307	2	           3			
0.1367	2	           3			
0.2007	2	           3			
0.438	2	           3			
0.0782	2	           3			
0.0595	2	           3			
0.0279	2	           3			
-0.0203	2	           3			
-0.0746	2	           3
```

Then, I copied the data from each into a array in MATLAB with the same name.
(Copy only numerical data in "Excel", then type v=[ (paste) ] (enter).

Then, run the function 'anovan.m' in MATLAB:

```
    anovan(R_STS,{PerceiverGroup StimulusType},'model',2,'varnames',strvcat('Group','Stim'))					
```

The output is a chart-- copy it back into your Excel spreadsheet to have the numbers handy.

```
    Source Sum Sq. d.f. Mean Sq. F Prob>F					
    --------------------------------------------------------					
    Group 0.00787 1 0.00787 0.3 0.5848					
    Stim 0.03208 2 0.01604 0.62 0.544					
    Group*Stim 0.01316 2 0.00658 0.25 0.7775					
    Error 1.1696 45 0.02599					
    Total 1.2314 50
```

In this example, there was not a significant main effect of perceiver group or stimulus type (both p > 0.5) on the right STS response.
There was also no interaction between the two factors (p > 0.7).

Degrees of freedom:

```
For the numerator, it's the number of categories in that factor minus one (a-1). Or, for the interaction, multiply (a-1)*(b-1). 
  In this case, the numerator df is 1 (from 2-1) for the Perceiver Group factor and 2 (from 3-1) for the Stimulus Condition Factor. 
  For the interaction, the numerator df is 2 (from 1*2).
For the denominator, it's the total number of data points (17 * 3 = 51) minus the total number of categories (N - a*b). 
  In this example, the denominator df are 45 (51 - 2*3).
```
