# TMSOverview

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

## General Overview

Like with any other experiment you first need to design the experiment and determine what conditions you will be testing and how many repetitions and how many subjects, etc. Additionally for all TMS experiments you will need to have one or more "control" experiments. This is to rule out that the observed effect is due to non-specific effect of the TMS. It is best to have at least one "spatial" and one "temporal" control experiment. With the spatial control, you will move the coil to a different location on the brain. Some people move the coil away from the head or tilt it. I don't think that would be a good control. Sham TMS coils are expensive and do not seem to replicate nonspecific effect of the real TMS coil. For a temporal control, you need to try different timings of TMS with respect to the stimulus. If the observed effect is a genuine neural effect, it has to be extremely dependent on the timing of TMS. You can use the figure-of-eight coil for disrupting neural activity in a relatively small part of the brain (on the order of several cubic millimeters) and the round coil for disrupting larger areas like much of the visual cortex. Double coil TMS is possible with our two machines. See a sample experiment in /Volumes/data1/TMS/Siavash/LAB\_WORK/Experiments/McGurk/Double\_Coil

It is a good practice to keep a record of anything that happens while doing the experiment that might be helpful when analyzing the data. For example an experimental sheet can be used: [[1]](../../attachments/TMSOverview/TMS_EXPERIMENTAL_SHEET.pdf)

## Subject recruitment

So far we only do single pulse TMS for which I have not seen any reports of adverse effects. However to be on the safe side, our experiments are restricted to healthy individuals (no neurological disorder or history) and those who are not pregnant and are not taking any medications that may lower seizure threshold (for a sample list see: [[2]](http://professionals.epilepsy.com/page/table_seniors_drugs.html)). A TMS Screening form has been created to make sure the subject has no contraindications [[3]](../../attachments/TMSOverview/TMS_SCREENING_FORM.pdf)

And as with any other experiment, an informed consent form must be given to the subject prior to the experimentation with sufficient time for them to read it and to ask any questions they might have. The form must be signed and dated by both the subject and the experimenter and a copy of the signed form should be given to the subject for their record. For the most recent version of our IRB approved consent form see [[4]](Subjects.md)

## Presenting the stimuli and TMS

You will need to write a program to deliver the stimuli and TMS with precise control of timing of the stimuli. "Presentation" program (www.nuerobs.com) is a relatively good and easy software for this purpose. Computer control of TMS machine is explained here: [[5]](TMS.md#Computer_control_of_TMS_machines)

## Using Brainsight navigation

1- Make sure the reflective markers holder is tightly fixed to the coil and calibrate the coil. (This doesn't need to be done every time if the markers have not moved)

2- Create a new project and load the anatomical images (NifTi file).

3- (Optional) Load functional images as well if available/needed. Note that some preprocessing is needed to make the functional images have the same resolution as the anatomical. See: [[6]](TMS.md#Transferring_MRI_Data_To_The_Brainsight_System)

4- Generate 3D brain (Full Brain Curvilinear) and skin reconstructions.

5- Mark anatomical landmarks. A minimum of three is needed. Four would be better: Nose Tip, Nasion, left and right ear notches.

6- Identify and mark targets based on the anatomy and/or functional map.

7- Choose the target and move the coil around and change its orientation until the target is covered.

Extra: You can record the exact coordinates of each TMS pulse using the LabJack interface.
