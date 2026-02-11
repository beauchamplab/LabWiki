---
layout: default
title: "anovan"
parent: Beauchamp
---
# anovan


|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

## Matlab ANOVAN

For performing sophisticated statistical analyses, Matlab's anovan is a useful function. Other options are dedicated stats packages like R, SPSS, etc.

These notes are adapted from /data1/UT/STP/STPNotes.rtf

The values can be read into Matlab from a text file or from Excel with the command

```
 correct = xlsread('tomatlab.xls')
```

We feed ANOVAN a 1-D vector which contains all of the data.
To make sense of the vector, Matlab also needs other vectors which list the factor-level for each datum.
There is a separate 1-D file for each factor.

For instance, if the data is input by subject with three data points (corresponding to stimulus types) for each subject, our data vector would be

```
 s1d1 s1d2 s1d3 s2d1 s2d2 s2d3 etc.
```

Then, our subject factor vector would be

```
 1 1 1 2 2 2 etc.
```

and out stimulus factor would be

```
 1 2 3 1 2 3 etc.
```

Note that these can also be text labels (e.g. "Face","House").
We use numbers for ease of automation.

These factor vectors can be automatically generated in Matlab with
stimnum = 5
subjnum = 37

gsubj = reshape(meshgrid(1:1:subjnum,ones(1,stimnum)),stimnum\*subjnum,1)
gstim = repmat(meshgrid(1:1:stimnum,1),1,subjnum)'

In a more complex example, we have two different groups with different diagnosis.

```
 numgrp1 = 20
 numgrp2 = 17
 total1 = numgrp1 * stimnum;
 total2 = numgrp2 * stimnum;
 ggroup = [ 1*ones(total1,1)' 2*ones(total2,1)' ]'
```

Next, we can try to load in data to run the ANOVA on:
cd /Volumes/data1/NIH/autism/point\_light/AKGroup/TimeSeries

```
 load NCSTSv6.2D
```

This contains the average timeseries from the STS in 17 NC subjects (group 2).
load ASDSTSv6.2D
This contains the average timeseries from the STS in 20 ASD subjects (group 1).
We average the appropriate time points to get a single number for each stimulus:

```
 clear alldata
 ctr = 1
 for i=1:numgrp1
 alldata(ctr:ctr+4) = [mean(ASDSTSv6(3:9,i)) mean(ASDSTSv6(16:22,i)) mean(ASDSTSv6(29:35,i)) mean(ASDSTSv6(42:48,i)) mean(ASDSTSv6(55:61,i))]'
 ctr = ctr + 5;
 end
 for i=1:numgrp2
 alldata(ctr:ctr+4) = [mean(NCSTSv6(3:9,i)) mean(NCSTSv6(16:22,i)) mean(NCSTSv6(29:35,i)) mean(NCSTSv6(42:48,i)) mean(NCSTSv6(55:61,i))]'
 ctr = ctr + 5;
 end
```

```
 resdata = alldata'

 ggroup = [ 1*ones(total1,1)' 2*ones(total2,1)' ]'
 gstim = repmat(meshgrid(1:1:stimnum,1),1,subjnum)'
 gsubj = reshape(meshgrid(1:1:subjnum,ones(1,stimnum)),stimnum*subjnum,1)
```

```
 [p,table,stats] = anovan(resdata,{gsubj ggroup gstim},'model','interaction','random',1,'varnames',{'Subject','Diagnosis' 'StimType'});
```

```
 [p,table,stats] = anovan(resdata,{ggroup gstim},'model','interaction','random',1,'varnames',{'Diagnosis' 'StimType'});
```

```
[p,table,stats] = anovan(resdata,{ggroup gstim},'model','interaction','varnames',{'Diagnosis' 'StimType'});
```

Include another stimulus type:
stimnum = 6
subjnum = 37

```
 numgrp1 = 20
 numgrp2 = 17
 total1 = numgrp1 * stimnum;
 total2 = numgrp2 * stimnum;
```

```
 clear alldata
 ctr = 1
 for i=1:numgrp1
 alldata(ctr:ctr+5) = [mean(ASDSTSv6(3:9,i)) mean(ASDSTSv6(16:22,i)) mean(ASDSTSv6(29:35,i)) mean(ASDSTSv6(42:48,i)) mean(ASDSTSv6(55:61,i)) mean(ASDSTSv6(68:74,i))]'
 ctr = ctr + 6;
 end
 for i=1:numgrp2
 alldata(ctr:ctr+5) = [mean(NCSTSv6(3:9,i)) mean(NCSTSv6(16:22,i)) mean(NCSTSv6(29:35,i)) mean(NCSTSv6(42:48,i)) mean(NCSTSv6(55:61,i)) mean(NCSTSv6(68:74,i))]'
 ctr = ctr + 6;
 end
```

```
 resdata = alldata';

 ggroup = [ 1*ones(total1,1)' 2*ones(total2,1)' ]'
 gstim = repmat(meshgrid(1:1:stimnum,1),1,subjnum)'
 gsubj = reshape(meshgrid(1:1:subjnum,ones(1,stimnum)),stimnum*subjnum,1)
```

[p,table,stats] = anovan(resdata,{ggroup gstim},'model','interaction','varnames',{'Diagnosis' 'StimType'});

We can then use ttest2 to get probabilities for any given combination:
If stimuli 1 are movies and 2 are pictures, then we can perform a t-test of movies vs. pictures:

```
 [h,p,ci,stats] = ttest2(alldata(gstim==1),alldata(gstim==2))
```

h =

```
    1
```

p =

```
  1.4378e-13
```

ci =

```
   0.1230    0.1922
```

stats =

```
   tstat: 9.0872
      df: 72
      sd: 0.0746
```

or, more complex:

```
 [h,p,ci,stats] = ttest2(alldata(gstim==1 & ggroup ==2),alldata(gstim==2 & ggroup == 2))
 [h,p,ci,stats] = ttest2(alldata(gstim==4 & ggroup ==2),alldata(gstim==5 & ggroup == 2))
[h,p,ci,stats] = ttest2(alldata(gstim==4 & ggroup ==1),alldata(gstim==5 & ggroup == 1))
```

[h,p,ci,stats] = ttest2(alldata(gstim==4 & ggroup ==1),alldata(gstim==5 & ggroup == 1))

```
 [h,p,ci,stats] = ttest2(alldata(gstim==1 & ggroup ==2),alldata(gstim==3 & ggroup == 2))
```
