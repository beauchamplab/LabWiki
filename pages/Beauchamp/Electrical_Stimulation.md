---
title: Electrical Stimulation
parent: Beauchamp
---
# Electrical Stimulation

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

**Electrical Stimulation**  
1. Select "Microstim Staircase" from available KNOT plugins.  
2. On toolbar, open Channel Settings, Stimulus Settings, Staircase Settings, and Behavior Settings windows.  
3. Enter the names of all Channels.  
4. Check to see that the following fields in Stimulus Settings have default values specified below:

:   a. Stimulation: Electrical
:   b. Pre-Interval (ms): 250 (period before Interval One)
:   c. Interval (ms): 300 (length of each interval)
:   d. Inter-interval (ms): 1000 (period between Interval One and Interval Two)
:   e. Post-interval (ms): 50 (period after Interval Two)
:   f. Select Electrical  

    :   i. Indicate "Max. Current (uA)" and "Min. Current (uA)."
    :   ii. Indicate number of "Currents."
    :   iii. Frequency (Hz): 200
    :   iv. Pulse Width (uS): 200
    :   v. Indicate "uA per V output" (If range max is below 1000 uA, use 100 uA per V. If range max is above 1000 uA, use 1000 uA per V.)
    :   vi. DA Channel Out: 0
    :   vii. Marker Pulses Bit: 1
    :   viii. Gate Bit: 0
    :   ix. Check "TTL Marker Pulses."
    :   x. Check "TTL Gate."

Values in other fields will not matter for close-eyed detection task.  
5. Check to see that the following fields in Staircase Settings have default values specified below:

:   a. Trial Limit: 10000 (This is the maximum number of tries the computer will make to determine threshold.)
:   b. Test Jitter (%): 15% (This is the amount by which the computer will jitter the number it selects from the Gaussian around its threshold estimate to deliver. Ultimately, it will choose to deliver the current level from the restricted range we provide that is closest to this jittered value.)
:   c. Select "Electrical."
:   d. Guess Threshold: 1500
:   e. Smallest Intensity Step: 100 (If this is too small, the computer may get stuck in a local minimum. If it is too large, the computer will never deliver currents near threshold.)
:   f. STD of Threshold: 1500

6. Check to see that the following fields in Behavior Settings have default values specified below:

:   a. Blocks: 20
:   b. Intertrial (ms): 2000
:   c. Response Time (ms): 1000 (This can be quicker, if the patient is fast.)
:   d. Too Fast (ms): 100 (This is the window after Post-Interval during which the subject cannot respond.)
:   e. Tries: 1

Values in other fields will not matter for close-eyed detection task.  
7. On toolbar, select File: Record Data to File to record data. Press Run. 20 blocks should take about 20 minutes.   
8. On toolbar, open Windows: Behavior. Keep track of "Number of Trials" in particular. We want at least 10 repetitions at current levels producing 50% correct and 100% correct with several points along the rising edge of the psychometric function.   
9. If the computer is not delivering currents optimally to reconstruct a good behavioral function, press Stop and then press "Choose Constant Currents" in the Stimulus Settings window. Check the current levels desired and the number of trials for each (bearing in mind how many repetitions have already been delivered for each level selected). Press OK. Check "Constant Currents." Now, press Run again.

Back to [Setup Apparatus](Setup_Apparatus.md "Beauchamp:Setup Apparatus").  
On to [Selectivity](Selectivity.md "Beauchamp:Selectivity").
