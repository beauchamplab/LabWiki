# dprime

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

|  |  |
| --- | --- |
| [Brain picture](../../attachments/AuditoryTactile/BrainPic.0023.png) | Beauchamp Lab Notebook |

- [Home](index.md "Beauchamp")
- [Lab Members](Lab_Members.md "Beauchamp:Lab Members")
- [Lab Alums](Lab_Alums.md)
- [Projects](Projects.md)
- [Publications](Publications.md "Beauchamp:Publications")
- [*Lab Notebook*](Lab_Notebook.md "Beauchamp:Lab Notebook")
- [Subjects](Subjects.md "Beauchamp:Subjects")

- [Software Installation](Software_Installation.md)
- [Ordering](Ordering.md)
- [MRI Data Analysis](MRI_Data_Analysis.md "Beauchamp:MRI Data Analysis")
- [Electrophysiology](Electrophysiology.md "Beauchamp:Electrophysiology")
- [TMS](TMS.md "Beauchamp:TMS")

In a two-alternative forced choice task (2AFC) where the stimulus is either True or False, there are 2 possible outcomes for each stimulus type, making 4 total possibilities:

```
Stimulus =  True,  Response = True  ---> Hit
Stimulus =  True,  Response = False ---> Miss
Stimulus =  False, Response = True  ---> False Alarm
Stimulus =  False, Response = False ---> Correct Rejection
```

Hit Rate (HR) and False Alarm Rate (FAR) will be:

```
HR = Hits / (Hits + Misses)
FAR = False Alarms / (False Alarms + Correct Rejections)
```

d' (d-prime) is a measure in signal detection theory that measures the distance between signal and noise in standard deviation units. It is calculated as:

```
d' = Z(HR) - Z(FAR)
```

The Z scores are calculated using Normal CDF, for example in Matlab:

```
Z_HR = norminv(HR)
```

Z(0) and Z(1) is infinity. One way around it is to add 1 to each of the 4 outcomes. For example the HR for 40 True responses out of 40 trials with a True stimulus, instead of being 40/40 would be 41/42. NOTE: To avoid bias, this procedure should be done for all conditions regardless of whether the rates are at extreme values (0 or 1) or not.

UPDATE: To make this procedure consistent across experiments with different numbers of trials for each condition, one can first normalize the number of trials in each condition to 100 and then add 1. In the previous example, 40/40 HR would first become 100/100 and then becomes 101/102. This way the same z-score and hence d-prime will be obtained for experiments with same ratios of hits and misses but different number of trials.

Another useful measure, is Response Bias (criterion, c) calculated as:

```
c = -(Z(HR) + Z(FAR))/2
```

Smaller absolute values of c are desired because a large absolute value of c shows the subjects' bias towards one type of response regardless of the stimulus. For example if the subject is responding "True" all the time, then:

```
HR = 101/102
FAR = 101/102
c = -2.3
```

or if the subject is responding "False" all the time, then:

```
HR = 1/102
FAR = 1/102
c = 2.3
```

A perfect subject would respond appropriately to the different types of trials:

```
HR = 101/102
FAR = 1/102
c = 0
```

Or a more realistic scenario:

```
HR = 71/102
FAR = 11/102
c = 0.36
```

For more info see:
Stanislaw H and Todorov N (1999) "Calculation of signal detection theory measures" *Behavior Research Methods, Instruments, & Computers* 31 (1), 137-149
