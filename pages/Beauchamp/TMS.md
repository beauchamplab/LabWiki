---
title: TMS
parent: Beauchamp
---
# TMS

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

## Computer control of TMS machines

This page describes research conducted for Nafi Yasar's Rice Bioengineering Ph.D. thesis in the Beauchamp Lab. Many additional details not found on this page can be found in the thesis. [Click here for Nafi's thesis.](../../attachments/TMS/Thesis_v3.pdf "Thesis v3.pdf")

[Click here for the document describing Nafi's TMS system](../../attachments/TMS/BeauchampTMSSystemOverview.doc "BeauchampTMSSystemOverview.doc")

**CONTROLLING MAGSTIM RAPID2 IN E-PRIME**

There are two ways for this depending whether you only need to send a trigger pulse or whether you also need to set machine parameters, enable/Disable etc.

**Sending a trigger pulse only:**
For this you need to have a parallel port. Virtually no laptop these days comes with a parallel port. If you must use a laptop, then there are some limited option with parallel port Express Cards. Otherwise desktop computers may have a factory installed parallel port and if not a PCI parallel port card can be easily added.
You then need to build a cable to connect the parallel port to the TMS machine. Easiest way would be to hack a BNC cable and connect a Male DB25 connector and connect the signal wire of the BNC cable to pin 2 and the shield wire to pin 18 (or any of the pin 18 - 25). Then connect the DB25 side to the parallel port and the BNC side to the Input Trigger jack on the Magstim.

In E-Prime you need to use WritePort command (Syntax: WritePort PORT\_ADDRESS, Value)
WritePort can write to pins 2-9 of the parallel port. Pin order is like this: 9-8-7-6-5-4-3-2

So 00000001 means send 5 volts down first pin (Pin 2) and so forth. WritePort takes the decimal value of the byte so either calculate it (for example the value to set the first pin [pin2] on would be 2^0 = 1) or use a table as in <http://www.pstnet.com/support/kb.asp?TopicID=1320>

or just use the binary value with the &B prefix e.g. &B00000001

WritePort also needs the parallel port address. One way To find the parallel port address is to go to:

Control Panel --> Device Manager --> Ports --> LPT1 --> Resources

and get the beginning value of the first I/O range (for example 378 or D010) which is in Hex so need to refer to it with &H prefix: &H378 or &HD010

Lastly the pin needs to be reset after the desired pulse duration has elapsed. One way to do this would be to use Sleep function which take values in milliseconds.

So to send a 10ms TTL pulse down Pin2 you could use this in-line script:

```
Const PORT_ADDRESS = &HD010
Const PulseDur = 10 'ms
WritePort PORT_ADDRESS, &B00000001  ' turn on pulse. 
Sleep PulseDur
WritePort PORT_ADDRESS, &B00000000  ' turn ff pulse
```

**Full computer control of Magstim Rapid2:**
For this you need to have a serial port and possibly an unlock code (that may need to be purchased from Magstim. Please contact them directly for further info).
Once the unlock code (if needed) is received you will need a cable to connect the serial port to Rapid2 machine. The cable would be female DB9 on one side and male DB26 on the other side. Only 3 wires are needed as described in <http://www.psych.usyd.edu.au/tmslab/downloads/SerialCable_and_Rapid2Toolbox_v1.pdf>

In summary:

DB9 --> DB26

pin 2 --> pin 13

pin 3 --> pin 12

pin 5 --> pin 11 (ground)

To send signals via serial port, you need to send ASCII strings of commands as defined in Magstim's manual. This involves calculating a checksum byte too which is calculated by adding all the bytes in the command, then inverting the first 8 bits bit by bit. For example a command "@050" which is to set the TMS power to 50% needs a checksum byte which can be calculated as amentioned above to be "\*".

The signal can then be send using WriteString:

```
Serial.WriteString "@050*"
```

But in some cases the checksum byte is not type-able (like a file separator for example which is 0X1C in Hex). For that, or for all cases, you can use WriteBytes:

```
Dim arrData1(4) As Integer
arrData1(0) = &H40 'or you can use the binary value if preferred. for example &B01000000
arrData1(1) = &H30   
arrData1(2) = &H35
arrData1(2) = &H30
arrData1(2) = &H2A 'this is the checksum byte which is "*" in ASCII
Serial.WriteBytes arrData1
```

You can read responses from Rapid2 in a similar way using ReadBytes or Read String. For example to read system status I have written this function:

```
Sub GetSystemStatus
   Dim SerialStr As String
   Dim N As String
   Dim SystemStatus As String

   Serial.WriteString "x@G"
   Do While Serial.InputCount =0
   Loop

   Dim arrData(5) As Integer
   Dim nRead As Long
   nRead = Serial.ReadBytes(arrData,6)
   SystemStatus = BIN(arrData(1))
   Debug.Print IIf(Mid(SystemStatus,8,1)="1","Standby, ","") &_
               IIf(Mid(SystemStatus,7,1)="1","Armed, ","") &_
               IIf(Mid(SystemStatus,6,1)="1","Ready, ","") &_
               IIf(Mid(SystemStatus,5,1)="1","Coil Present, ","") &_
               IIf(Mid(SystemStatus,4,1)="1","Replace Coil, ","") &_
               IIf(Mid(SystemStatus,3,1)="1","Error Present, ","") &_
               IIf(Mid(SystemStatus,2,1)="1","Fatal Error, ","") &_
               IIf(Mid(SystemStatus,1,1)="1","Remote Control Enabled","")
End Sub	
```

For fixed commands, the checksum can be calculate once and used whenever needed. Some commands however (such as set power) will need a checksum value of which depends on the chosen parameter (for example the chosen power level). To calculate the checksum byte, I have written this function:

```
Function CRC(InputString As String) As Integer
   Dim CharCount As Integer
   Dim CRC_init As Integer
   CRC_init = 0
   For CharCount = 1 To Len(InputString)
      CRC_init = CRC_init + ASC(Mid(InputString,CharCount,1))
   Next CharCount

   Dim CRC_Bin As String
   CRC_Bin = BIN(CRC_init)
   CRC_Bin = RIGHT(CRC_Bin,8)

   Dim CRC_Bin_Inv As String
   CRC_Bin_Inv = ""
   For CharCount = 1 To 8
      CRC_Bin_Inv = CRC_Bin_Inv & IIf(Mid(CRC_Bin,CharCount,1)="0","1","0")
   Next CharCount

   Dim CRC_Bin_Inv_Dec As Integer
   CRC_Bin_Inv_Dec = 0
   For CharCount = 1 To 8
      CRC_Bin_Inv_Dec = CRC_Bin_Inv_Dec + Mid(CRC_Bin_Inv,CharCount,1) * 2^(8-CharCount)
   Next CharCount
 
   CRC = CRC_Bin_Inv_Dec
End Function
```

And to set the power to the desired level, I have written this function:

```
Function SetPower(PowerValue As Integer)
   If PowerValue >=10 And PowerValue <=99 Then
      Serial.WriteString "@0" & CStr(PowerValue) & CHR(CRC("@0" & CStr(PowerValue)))
   ElseIf PowerValue = 100 Then
      Serial.WriteString "@100" & CHR(CRC("@100"))
   Else
      ' power should be between 10 and 100 
   End If
End Function
```

**USB CONTROL OF MAGSTIM RAPID AND NAFI'S MACHINE USING PRESENTATION SOFTWARE**

Both machines (MagStim and Nafi's) use a National Instrument USB Data acquisition card (referred to here as NIDAQ). However the Presentation Library for these two machines are different. Here is the one for Magstim: [[1]](../../attachments/TMS/USB_TMS_library.pcl) and here is the one for Nafi's: [[2]](../../attachments/TMS/Nafi's_TMS_library.pcl)

The NIDAQ needs to be defined in Presentation (under Settings --> Port) as 3 output ports. For each port, "USB-6501" should be selected. For the first port choose "Data source: port0", for the second one choose "Data source: port1", and for the third one choose "Data source: port2". For Nafi's nothing else needs to be changed. For MagStim the "Inversion mask" of the seond port needs to be changed to 255 (because they have used inverse logic for their trigger circuit).

These 3 lines need to be put in the header part of Presentation scenario file (before the SDL begin):

```
pulse_width = indefinite_port_code;
write_codes = true;
response_port_output =  false;
```

The appropriate library also need to be included at the beginning of the PCL section:

```
include "USBTMS_library.pcl";
```

or

```
include "nafi's_TMS_library.pcl";
```

These are the self explanatory commands used in the PCL section to control each system:

MagStim:

```
set_TMS_strength(integer between 0 and 100)
enable_TMS()
disable_TMS()
trigger_TMS()
```

Nafi's:

```
set_TMS_strength(integer between 0 and 100)
arm_TMS()
disarm_TMS()
trigger_TMS()
connect_coil()
disconnect_coil()
```

An alternative to trigger\_TMS() that can be used in the SDL section (inside trial definition) is this:

```
nothing{};	time = $TMS_time;   port_code = 1;   port = 2;
nothing{};	time = '$TMS_time + 1';   port_code = 0;   port = 2;
```

The port\_code commands could also be used with any other event (instead of nothing{ }).

When timing of TMS pulse can be defined in terms of the time after the beginning of trial, the above mentioned method is used. On the other hand, when the timing of TMS pulse is defined in terms of a video frame of a video file, then the trigger\_TMS() in PCL is used.

Here is an example of delivering a TMS pulse at a specific time during trial:

```
trial {
   trial_duration = $trial_dur;
   picture some_picture;	time = 0;
   sound some_sound; time = $touch_time;
   nothing{};	time = $TMS_time;   port_code = 1;   port = 2;
   nothing{};	time = '$TMS_time + 1';   port_code = 0;   port = 2;
}sample_TMS_trial;
```

Here is an example of delivering a TMS pulse at a specific video frame:

```
int movienum = 0;
int curfr = 0;
bool startedplaying = false;
video_report whatson;
int TMS_frame = 35;
int end_frame = 50;

test_video.set_end_frame(end_frame); 
test_video.prepare(); 
video_player.play( test_video, "test_video" );

loop until curfr > end_frame
begin 
   if ( !startedplaying && video_player.report_count() > movienum) then 
      startedplaying = true;
      movienum = movienum + 1;
      whatson = video_player.last_report();
   end;
   if ( startedplaying ) then 
      if (whatson.frame_data_count() > curfr) then 
         curfr = whatson.frame_data_count();
         if curfr == TMS_frame then
            trigger_TMS(); 
         end;
      end;  
   end;
end;
```

## Simultaneous TMS and EMG

Rogue Research is supposed to soon offer an EMG setup that is compatible with BrainSight.
Cambridge Electronic Design produces some amplifiers that are designed to eliminate the TMS artifact, as well as software called Signal for recording the EMGs.
Here are some PDFs from them that have information on controlling MagStims through the serial port.
[Media:MagstimcontrolSignalv4.pdf](../../attachments/TMS/MagstimcontrolSignalv4.pdf "MagstimcontrolSignalv4.pdf")
[Media:SignalEvokedResponse.pdf](../../attachments/TMS/SignalEvokedResponse.pdf "SignalEvokedResponse.pdf")
[Media:Beauchamp1902.pdf](../../attachments/TMS/Beauchamp1902.pdf "Beauchamp1902.pdf")

## USB control of TMS

<Software_Installation.md#Presentation>

## Parallel port control of Magstim Rapid TMS (OLD)

This is our TMS (Transcranial Magnetic Stimulation) machine from Magstim company, UK. The front panel controls are:

:   1.Standby
:   2.Run (arm, bring out of standby)
:   3.Stimulus intensity control
:   4.Trigger

Alternatively to trigger the device, a TTL pulse can be sent to the "Trigger In" port in the back of the device with a BNC connector.

The machine can also be controlled externally via the 36pin Centronics connector in the back panel.
A Parallel printer cable can be used/made with a DB25 male connector on one end to connect to PC Parallel Port and a Centronics 36pin male connector on the other end to connect to Magstim Rapid.

NOTE: ECP/EPP needs to be selected for the Parallel Port in BIOS.

A 5V input should be connected to Pin 1 of the Centronics connector to gain external control (either from an external source or by downstepping the available 12V at pin 15 of the Centronics connector.

A 7 bit binary code through pins 2-8 can set the stimulus intensity (only values between 10% and 100% should be used, for example 0110010 for 50%)

Pin 9 is used for triggering by applying a 0.

Magstim instruction manual advises NOT to use the BNC trigger input when using this trigger instead.

Pins 14 and 31 of the Centronics connector can be used to arm and standby the device respectively. Magstim instruction manual advises NOT to use these features because of possible safety issues. However we noticed that when the TMS coil is in the magnet, many a time the inducted signal by the scanner puts the TMS device on standby. Therefore it needs to be armed again to deliver TMS pulses during the gap between scans. So it seems using pin 14 to arm the device is inevitable.

A number of digital and analog output signals are also available at the port including coil temperature and capacitor voltage. See Magstim instruction manual.

## Transferring MRI Data To The Brainsight System

The BrainSight controls for adjusting and viewing MRI data are not very flexible. Therefore, preprocessing must be done in AFNI.

Anatomical MRIs:
Brainsight can directly load NIFTI files. The highest quality T1s are the average anatomicals collected for creating cortical surface models (ibid.). Use the 3dcopy command to create a NIFTI version.

```
 3dcopy EKanatavg+orig EKanatavg_forTMS.nii
```

In some cases, the image may be too dark or too bright (even after using BrainSight's built-in contrast tools).
If this is the case, adjust the image intensity with 3dcalc.

Functional MRIs:
First, decide what combination of sub-briks and what thresholds you would like to visualize.
Then create a BRIK:

```
 3dcalc -prefix ThumbVsIndexForBrainSight -a0 EIalldec+orig -b35 EIalldec+orig -expr "step(a-4.94)*step(abs(b)-2)*b"
```

Next, it must resampled to be the same resolution as the anatomical

```
 3dresample -inset ThumbVsIndexForBrainSight+orig -master EIanatavg_forTMS.nii -prefix ThumbVsIndexForBrainSight_nifti.nii
```

BrainSight requires a substantial amount of post-processing for the T1 anatomicals, such as the curvilinear brain surface reconstruction, markers, etc.
If the fMRI data is from a different day, then we want to resample (and realign) the fMRI data to the other-day T1 used for BrainSight post-processing.
This requires two steps. First, align the old and new anatomies. Second, apply the same transformation that aligns the old and new anatomies to the (new) fMRI data. Following these two steps, the new fMRI data will be in alignment with the old T1.
An important detail is that it is better to perform thresholding AFTER alignment (or any other kind of resampling) so this is actually a three step process.

If the old and new anatomies have different number of slices, the alignment can be performed with 3dAllineate.

```
 3dAllineate -1Dparam_save DBtoBG  -1Dmatrix_save DBtoBG -twopass -warp shr \
 -base /Volumes/data9/surfaces/beauchamp_michael/afni/T1/BG_avg+orig \
 -prefix DBanatavg_regtoBG DBanatavg+orig
```

Step 2:

```
 3dAllineate -float -input DBt2v1dec+orig'[23]'   -1Dmatrix_apply DBtoBG.aff12.1D \
 -master /Volumes/data9/surfaces/beauchamp_michael/afni/T1/BG_avg+orig \
 -prefix DBt2v1sb23_AlndToBG
```

Step 3:

```
 3dcalc -prefix DBregtoBG_MSB_SSct.nii -a DBt2v1sb23_AlndToBG+orig -expr "step(a-4.2)*a"
```

If the old and new anatomies have the same number of slices, it may be easiest to do this with 3dvolreg (these steps have not been tested):

```
3dvolreg -twopass -twodup \
 -base /Volumes/data9/surfaces/beauchamp_michael/afni/T1/BG_avg+orig \
 -prefix DBanatavg_regtoBG DBanatavg+orig
```

Step 2:

```
3drotate -rotparent /Volumes/data9/surfaces/beauchamp_michael/afni/T1/DBanatavg_regtoBG+orig \
 -gridparent /Volumes/data9/surfaces/beauchamp_michael/afni/T1/BG_avg+orig \
 -prefix DB_MSB_SSctx_AlndToBG DB_MSB_SSctx+orig
```

Step 3: Redo thresholding.

## Simultaneous TMS and fMRI

The TMS coil is too small to fit in the standard SENSE head coil.
The two options are to use the 2-element surface coil (TMJ coil) for local coverage or the
whole-head birdcage transmit/receive (TR) coil.
If using the TR coil, the placement of the TMS coil relative to the TR coil is critical. If it is too close to the bars of the TR coil, the scanner will give an error message such as:
"TR head coil requires 2149 watts. Limit is 2000 watts."
This might be due to inductive coupling between the headcoil and the TMS coil, so the scanner cannot drive the coil to generate RF.

experiment notes for 10/07/2009

TMS coil placed on right side of face
first goal was to map out auditory/somatosensory stimulation (indirect effect of TMS)
started with coil far away from face for just auditory response, but this created error message described above.
therefore, moved closer creating both auditory stimulation and face stimulation from TMS (no magnetic stimulation)
so used 10% TMS with block design experiment
6 TR ON/6 TR OFF \* 10 blocks = 120 TRs total
each TR was 2.75 sec, with 5 TMS pulses in each TR at 10 Hz
idea is that should result in a nice block design auditory/SS cortex response
used Philips RT to look at map

run 1: program crashed after 3 - 4 blocks

run 2: couldn't figure out problem, increased total\_scans variable to 1200
watch more closely
crashed after 6 - 7 blocks
TMS pulses seemed to be coming too early within each TR, then program crashed.
in the last TR or two before the crash, the relays opened but there was no pulse.

1/12/2010
Problems
fault lights come on, must restart machine
NIDAQ card crashing
extra scanner pulses
contactor fusing shut--worse at 90%?

double pulse problem
(reduce contactor opening time)

contactor bouncing (distracting but not a serious problem)

display chip fried
light malfunctioning

More testing notes 2/2/2010
Used double pulses and varied the interpulse interval (IPI)
at 200 ms IPI, double pulses at 70% were the same amplitude
for double pulses at 90%, second pulse was decreased in amplitude about 20%
at 150 ms IPI at 70%, the second pulse was decreased in amplitude.

with the Magstim, at 70% 75 ms IPI was the minimum to prevent decrease amplitude
at 90%, 115 ms was the minimum
The Magstim will not trigger if the cap is not fully charged; Nafi's stimulator does not have that circuitry.
On the scope, both waveforms looked similar, roughly triphasic: large sharp positive, medium negative, small third positive peak.
Nafi's pulse was a little noisier and longer (400 us vs. 350 us).

## Timing of TMS and multisensory stimuli in Presentation

Presentation can keep the record of stimulus presentation times. It is important to understand that these times are from the "input" side of stimulus presentation devices. For example for a visual stimulus, the logged time would show the time that the information was sent to the video card and does not take into account any processing time by the video card and the internal delay of the display. Similar argument holds for auditory stimuli and TMS or other devices controlled by the computer. Here is a report of some measurements of the stimuli timing both from the "input" and the "output" sides.

**INPUT SIDE TIMINGS**

**Visual stimuli:**
It is important to understand that the start of a visual stimulus can only occur at integer multiples of the video refresh time after the start of trial. For a video card running at 60Hz that would be 0, 16.7, 33.4, etc. For example the following code:

```
trial {
picture test_picture; time = 90; code = "visual_onset";
} test_trial;
```

will lead to presentation of test\_picture at ~ 100ms after the start of trial as logged in the log file. By the same token the end of a visual stimulus (which is basically the beginning of another visual stimulus, i.e. blank or default) can only occur at said times and the minimum length of a visual stimulus will be equal to one refresh (16.7ms in this case).

Theoretically if you schedule a visual stimulus right at the time of an integer multiple of the refresh time, it should play at the requested time. But because of the preparation and processing times and perhaps other reasons, the visual stimulus needs to be scheduled slightly prior to that, for example by 5ms.

So far I am recommending the following code for showing the visual stimulus for 16.7 ms starting at time = 100ms:

```
trial {
picture test_picture; time = 95; code = "visual_onset";
picture {}; time = 112; code = "visual_end";
} test_trial;
```

Presenting the above trial many times theoretically should lead to presentation of the visual stimulus at time = 100ms lasting for one refresh or 16.7ms. In reality there are other factors that could affect this time including the processor load at the time. Presentation keeps a record of "uncertainty" of the recorded time. One can always go back to the log files and throw out trials for which the uncertainty or timings are not acceptable. The results may vary according to the hardware used. In my experience with a MacBook running Windows XP using Parallel, and no load other than Presentation, >90% of trials had variations < 1ms (much worse results with a Lenovo T61).

**Auditory stimuli:**
The logged time of the auditory stimuli are generally the exact requested time.

```
trial {
sound test_sound; time = 90; code = "audio_onset";
} test_trial;
```

will lead to presentation of test\_audio at 90ms after the start of trial as logged in the log file. Timing variations on the tested MacBook were pretty minimal (>95% of trials had variations <1ms)

This is with "DirectX Software" audio setting in Presentation. Other settings either didn't work at all with this setup or caused frequent crashing of the program.

**TMS:**
We use a National Instruments USB DAQ (NI USB-6501) [[3]](TMS.md#USB_control_of_TMS) to control our Magstim Rapid TMS mainly due to lack of parallel port in newer laptops. TMS is triggered by changing a port for a short time (1ms or less):

```
trial {
nothing {}; time = 90; port_code = 1; port = 2; code = "TMS";
nothing {}; time = 91; port_code = 0; port = 2;
} test_trial;
```

This will lead to triggering of TMS at 90ms after the start of trial as logged in the log file. Timing variations on the tested MacBook were pretty minimal (>95% of trials had variations <1ms)

**Simultaneous Audio, video, and TMS:**
Here is a code to present Audio, video, and TMS simultaneously:

```
trial {
picture test_picture; time = 95; code = "visual_onset";
picture {}; time = 112; code = "visual_end";
sound test_sound; time = 100; code = "audio_onset";
nothing {}; time = 100; port_code = 1; port = 2; code = "TMS";
nothing {}; time = 101; port_code = 0; port = 2;
} test_trial;
```

Presentation log file will show that all three stimuli were delivered at time 100-101ms.

**OUTPUT SIDE TIMINGS**

So far all these timings were related to the "input side". To measure the actual time (the time the illumination of the appropriate pixels change) I attached a photo diode to the LCD monitor at a location where a small white dot would be displayed using Presentation and connected it to the oscilloscope. The audio (from computer audio jack) and TMS (from the NIDAQ) were directly connected to the oscilloscope.

[![](../../attachments/TMS/Photo_diode_setup.jpg)](../../attachments/TMS/Photo_diode_setup.jpg)

[Photodiode circuit picture modified from: [[4]](http://www.rp-photonics.com/spotlight_2009_12_13.html)]

I only had access to a two channel oscilloscope so I had to look at two of the three signals at a time. Here is the "actual" timing of audio (Yellow) and video (Blue):

[![](../../attachments/TMS/Audio_video_timing_1.JPG)](../../attachments/TMS/Audio_video_timing_1.JPG)

This shows that even though the log files showed that the audio and visual stimuli started at the same time, here we see that in reality audio was lagging the video by about 15ms.

Here is the TMS (from USB DAQ) and the video:

[![](../../attachments/TMS/TMS_video_1.JPG)](../../attachments/TMS/TMS_video_1.JPG)

This shows that the video onset is lagging the TMS by about 10ms.

Now let's look at TMS and the Audio:

[![](../../attachments/TMS/TMS_audio_1.JPG)](../../attachments/TMS/TMS_audio_1.JPG)

This shows that the audio is lagging the TMS by about 26ms.

So even though Presentation log file shows that all three stimuli were presented at the same time (time 100ms), in reality the first stimulus is the TMS, then 10 ms later the video starts, and it takes another 16ms for the audio to start. This is obviously not desired specially for a TMS experiment where 10-20 ms could make a big difference. [Note that these time are relative to the actual TMS (from USB DAQ). I have no means of measuring the times with respect to the start of trial]

The following code will cause the 3 stimuli to be delivered at the same time:

```
trial {
sound test_sound; time = 85; code = "audio_onset";
picture test_picture; time = 95; code = "visual_onset";
picture {}; time = 112; code = "visual_end";
nothing {}; time = 110; port_code = 1; port = 2; code = "TMS";
nothing {}; time = 111; port_code = 0; port = 2;
} test_trial;
```

This code adjust the timings of TMS and audio to match that of the video onset. Here are the results:
[![](../../attachments/TMS/Audio_video_TMS_timing2.jpg)](../../attachments/TMS/Audio_video_TMS_timing2.jpg)

To present TMS 50ms after audio-video, add 50ms to the scheduled timings of TMS (160 and 161ms respectively). Similarly, to present TMS 50ms after audio-video, subtract 50ms from the scheduled timings of TMS (60 and 61ms respectively). Here are the actual results. Top row is TMS 50ms after, and bottom row is TMS 50ms before audio-video:
[![](../../attachments/TMS/TMS_before_and_after_AV.jpg)](../../attachments/TMS/TMS_before_and_after_AV.jpg)

It is important to note that these timing will most likely be different with different hardware setups. I tested an external monitor (Philips Brilliance 190SW; cloned with the MacBook display) and the video lags were longer and more variable. With the Macbook display, video lags were pretty consistent at 10ms (plus/minus 2 seconds or so). With the Philips they ranged from 7 to 21 ms with a mean and median of ~14ms (std = 4.4ms). I'm not sure whether this is a problem of the Philips monitor or the cloning process (MacBook's NVIDIA GeForce 8600M GT). UPDATE: It is apparently because of cloning. I tested the same Philips monitor as the primary display with the same MacBook and the lags were once again right around 10ms.

Another source of potential delay could be the TMS machine itself and the audio amplifier. I tested the input-output delays of our Magstim Rapid and PylePro PCA1 amplifier and they were negligible. I used the trigger-out of TMS machine for this test. To rule out the possibility of any delay between this trigger-out signal and the actual TMS pulse at the coil, I attached a loop of wire to the hotspot of TMS coil and connected it to the oscilloscope. There were no delays between the trigger-out signal and the actual TMS-pulse:
[![](../../attachments/TMS/TMS_trigger_out_vs_actual_pulse2.jpg)](../../attachments/TMS/TMS_trigger_out_vs_actual_pulse2.jpg)

**Bottom-Line:**
Depending on the hardware used it is possible to achieve timings that are within a few milliseconds of the planned times. One needs to measure the delays and make appropriate adjustments for each setup/experimental condition. Log-files need to be looked at after the experiments and trials with unacceptable timings should be discarded.

## Comparing strength of different TMS coils and machines

01-12-11

I used a loop of wire hooked up to the oscilloscope using a 100x probe (not sure if necessary, just to be safe) and measured the peak-to-peak voltage of the waveform generated by a TMS pulse for 3 setups:

```
- Magstim rapid machine with regular figure-of-eight coil
- Magstim rapid machine with air-cooled figure-of-eight coil
- Nafi's TMS machine with MRI compatible coil
```

Obviously, the voltages measured are a function of different parameters other than the actual TMS pulse strength (e.g. number of turns, wire thickness, material, etc). But the same loop of wire shown in this image was used for all three coils in the same orientation setup attached to the bottom of the coils at their hot-spots. So the relative measurements are meaningful. The measurements will also vary according to the placement of the loop of wire but I tried to be accurate in placing it the same way for the all three setups and the results below are consistent with the "feeling" one gets of the strength of these three setups.

[![](../../attachments/TMS/Aircooled_coil_measurement.jpg)](../../attachments/TMS/Aircooled_coil_measurement.jpg)

Results:

```
- Magstim with regular figure-of-eight coil is ~14% stronger than Magstim with air-cooled coil
- Magstim with regular figure-of-eight coil is ~35% stronger than Nafi's TMS with MRI compatible coil
- Magstim with air-cooled coil is ~19% stronger than Nafi's TMS with MRI compatible coil
- Programmed strength vs. measured strength relationship is reasonably linear
- Pulse duration is slightly different across the setups (~330-430 microseconds)
```

[![](../../attachments/TMS/TMS_coil_strength_comparison_chart.jpg)](../../attachments/TMS/TMS_coil_strength_comparison_chart.jpg)

- data for this chart can be found on data1/TMS/TMS\_coil\_strength\_comparison\_chart.xlsx

- In the bilateral STS-TMS experiment, we are using the magstim with regular coil and Nafi's with MRI coil and want the intensities to match. So for example if we decide on an intensity equivalent to 65% of Magstim's setup, we need to set Nafi's TMS intensity at 65\*1.35 = ~88% Or if we want to have the maximum possible matching intensity, that would be 100% on Nafi's TMS and 100/1.35 = ~74% on Magstim machine.

Waveforms:

[![](../../attachments/TMS/TMS_pulse_induced_waveform_figure_of_eight_coil_magstim_machine.jpg)](../../attachments/TMS/TMS_pulse_induced_waveform_figure_of_eight_coil_magstim_machine.jpg)
[![](../../attachments/TMS/TMS_pulse_induced_waveform_aircooled_coil_magstim_machine.jpg)](../../attachments/TMS/TMS_pulse_induced_waveform_aircooled_coil_magstim_machine.jpg)
[![](../../attachments/TMS/TMS_pulse_induced_waveform_MRI_compatible_coil_NAFI_machine.jpg)](../../attachments/TMS/TMS_pulse_induced_waveform_MRI_compatible_coil_NAFI_machine.jpg)

From left to right: Magstim with regular coil, Magstim with aircooled coil, Nafi's with MRI compatible coil. Time grid is 100 microseconds. Each images is from an 80% intensity TMS pulse in the corresponding setup.

Note: At the time of these measurements I was not able to use other setups, e.g. Nafi's TMS with regular or air-cooled coil or Magstim with the MRI compatible coil. These experiments were done WITHOUT the use of the relay boxes which may have allowed the mentioned setups to work.
