---
title: Tobii
parent: Beauchamp
---
# Tobii

Notes by Santiago on using the Tobii Glasses

## Data Analysis

The Tobii Pro Lab analysis software enables the user to actively manipulate the received data from the Tobii Pro glasses. This can be help ensure that the produced data is concise and clear. The eye tracking data from the glasses is displayed in real-time on the software while it is being recorded, along with a visual representation of the user's field of vision. The software uses these features to output useful metrics describing the position of the eyes, their velocity (according to several eye point values), and other useful quantitative values.

The manual for the Tobii Pro Lab software, as well as other useful documentation and the software itself, can be found [here](https://www.tobiipro.com/product-listing/tobii-pro-lab/).

### Velocity Classification

One of the useful aspects of the Tobii Pro software is its classification of gaze data according to their relative velocities. Essentially, a specific threshold velocity is set, being a neutral point, such that any velocity point above this is classified as a **saccade** and any point below is classified as a **fixation**. This is useful as a fixation refers to generally fixed eye movement, such that the subject is holding his gaze in relatively the same position, possibly indicating concentration and awareness. Although a saccade is generally linked to rapid eye movement, it should be understood that brief saccades, termed **micro-saccades**, could be the result of arbitrary noise from an eyelash or the like, and the surrounding data may still be useful.

With the Tobii Pro's velocity classification system, it is easy to implement a method of categorization of outputted data and metrics in order to use fixation points as valid data points for further analysis (i.e. a fixation point would represent a point where the subject was directly looking at the stimuli).

### Times of Interest

The Tobii Pro software also allows for the creation of [**times of interest**](https://www.tobiipro.com/learn-and-support/learn/steps-in-an-eye-tracking-study/data/Setting-up-and-using-Times-of-interest/) which enable the user to segment the overall data from the initial analysis in order to make the handling of the data easier. There are two types of times of interest:

1. **Automatic Times of Interest**: Created through the implementation of snapshot mapping (explained below), holding all of the data that corresponds to the snapshot that was mapped.
2. **Custom Times of Interest**: Created manually by the user.

The times of interest allow for quick data manupilation once the data has been exported. For example, if data had been pulled from an EEG experiment where the subject was shown a bright color on a screen at random time intervals, times of interest that correspond to the onset and offset of the stimuli would result in the exported data having a classification for this specific time of interest, allowing for any extra unnecessary data to be easily avoided.

### Snapshot Mapping

Snapshot mapping is another useful feature of the Tobii Pro analysis software, allowing the user to obtain classification of gaze data points on an image of interest quickly. This feature uses an imported "snapshot" (being an image of less than 25 MP) to automatically map gaze data from a recording onto the snapshot according to the points the program matches. This allows for specific analysis of stimuli to be done easily as the program does the bulk of the work. If any points are off the user can simply manually map the corresponding gaze data onto the snapshot.

This feature works even better with the times of interest feature, allowing for custom times of interest to be generated according to the imported snapshot. In implementing snapshot mapping to the example described in the last section, if the specific stimulus image that appeared on the recording was imported as an image, the program would automatically generate times of interest according to the exact points when the snapshot was present in the original video, making data acquisition and classification even faster and easier.

### Areas of Interest

Areas of interest are another useful feature of the Tobii Pro analysis software, functioning similarly to the snapshot feature. This allows the user to select specific objects in the video that are of interest and force the program to map their location in the video, further classifying gaze data according to that specific area of interest.

Of even more interest are the more complex [**dynamic stimuli** that can be tracked with the AOI feature](https://www.tobiipro.com/learn-and-support/learn/steps-in-an-eye-tracking-study/data/analyzing-dynamic-stimuli-with-the-aoi-tool/). These are useful for dynamic environments such as video clips or moving objects, as the AOI is mapped and located even with movement. This could be helpful in EEG tasks that utilize moving parts (i.e. if a stimuli has a face rotating around a square, the face could be the AOI which is followed around, with gaze data being classified accordingly).

### Changes in Set Parameters

The Tobii Pro software also allows the user to change the parameters followed by the program as well as its management of data. Mainly, the user can change the following:

1. **Eye Selection**: The user can select to discard data from a specific eye if needed. This is currently not available for **Glasses project**s, however I thought it would be useful to understand that this is also done if only one eye is detected by the glasses, allowing for a rather manual approach to this if it is needed.
2. **Noise Reduction**: The user can also manipulate the noise reduction median used by the software, in order to use a smaller sample of data points for noise reduction or a larger one.
3. **Velocity**: The user can also manipulate the velocity parameter in the software, changing the threshold velocity for which fixations and saccades are defined, as well as the actual calculation of velocity (amount of data points to be used for velocity calculation).
4. **Gaze Data Error Filling**: The software also has a parameter for fixing empty gaps of data due to noise, with the parameter being the **max gap length** for which the software will utilize the surrounding data to fill in the gap with in order to avoid segmentation of the data at the point. The user can manipulate the size of this parameter as needed.
5. **Merging Adjacent Fixations**: The software also automatically merges fixations that it deems to have been separated accidentally, utilizing two parameters: **max time between fixations** which defines the maximum time between fixations that should be merged, and **max angle between fixations** which defines the maximum visual angle of the eyes between fixations that should be merged.
6. **Discarding Short Fixations**: The program also automatically discards fixations that are deemed to short, in order to keep the data as clean and accurate as possible. For this the program uses the parameter **minimum fixation duration**, setting the value for the minimum duration a time segment can have to be classified as a fixation.

### Exporting Data

The Tobii Pro software allows for two types of exportation:

1. **Metrics Export**: Which involves exporting only the eye tracking metrics based on AOIs or Events to third-party software such as Excel or Matlab. Only available to export as an **xslx** file.
2. **Data Export**: Here the data exported is not tied to AOIs, being the raw gaze point data (such as gaze point in different coordinate systems, pupil diameter, eye position, and recording information). Metrics regarding the AOIs is not provided in this exportation type. Only available to export as a **tsv** file.

#### Metrics Export

The types of values available for exportation through the **metrics export** are as follows:

1. **Interval Duration**: Duration of all time intervals for each TOI, including averages, medians, sums, and counts. (Format: *HH:MM:SS:mmm*)
2. **Interval Start**: Start time of all intervals for each TOI, including averages, medians, and counts. (Format: *HH:MM:SS:mmm*)
3. **Event Count**: Number of events, including custom event types, for each TOI, including averages, medians, sums, counts, variance, and standard deviation (N-1). Here, descriptive statistics only include recordings where events occur. (Format: *Number*)
4. **Event Count (Including Zeroes)**: Same as the other **Event Count** metric except that here descriptive statistics also include recordings where no events occur. (Format: *Number*)
5. **AOI Time to First Fixation**: The time to first fixation for each AOI on all media, including averages, medians, count, and recording durations. (Format: *HH:MM:SS:mmm*)
6. **AOI Total Visit Duration**: Total time each participant has visited each AOI on all media, including averages, medians, sums, the share of total time spent in each AOI out of all AOIs, and the percentage of participants that visited each AOI at least once. Here, descriptive statistics are only based on recordings with fixations within the AOIs. (Format: *HH:MM:SS:mmm*)
7. **AOI Total Visit Duration (Including Zeroes)**: Same as other **AOI Total Visit Duration** metric except here descriptive statistics also include recordings with no fixations within the AOIs. (Format: *HH:MM:SS:mmm*)
8. **AOI Average Visit Duration**: Average duration each participant has visited each AOI on all media, including averages, medians, sums, and the percentage of participants that visited each AOI. (Format: *HH:MM:SS:mmm*)
9. **AOI Visit Count**: Number of visits within each AOI on all media, including averages, medians, and the percentage of participants that fixated within each AOI at least once. Here, descriptive statistics are only based on recordings with fixations within the AOIs. (Format: *Number*)
10. **AOI Visit Count (Including Zeroes)**: Same as other **AOI Visit Count** metric except here descriptive statistics also include recordings with no fixations within the AOIs. (Format: *Number*)
11. **AOI Total Fixation Duration**: Total time each participant has fixated on each AOI on all media, including averages, medians, sums, variance, standard deviations (N-1), the share of total time spent on each AOI out of all AOIs, and the percentage of participants that fixated within each AOI at least once. Here, descriptive statistics are only based on recordings with fixations within the AOIs. (Format: *HH:MM:SS:mmm*)
12. **AOI Total Fixation Duration (Including Zeroes)**: Same as other **AOI Total Fixation Duration** metric except here descriptive statistics also include recordings with no fixations within the AOIs. (Format: *HH:MM:SS:mmm*)
13. **AOI Average Fixation Duration**: Average duration of the fixations within each AOI on all media, including averages, medians, variances, standard deviations (N-1), the total Time of Interest, and recording durations. (Format: *HH:MM:SS:mmm')*
14. **AOI Fixation Count**: Number of fixations within each AOI on all media, including averages, medians, sums, variances, standard deviations (N-1), the percentage of participants that visited each AOI at least once, total number of fixations within the TOI, and the total TOI and recording durations. Here, descriptive statistics are only based on recordings within the AOIs. (Format: *Number*)
15. **AOI Fixation Count (Including Zeroes)**: Same as other **AOI Fixation Count** metric except here descriptive statistics also include recordings with no fixations within the AOIs. (Format: *Number*)

#### Data Export

The types of values available for exportation through the **data export** are as follows:

##### Metadata

1. **Project Name**: Name of the project.
2. **Export Date**: Date export was performed.
3. **Participant Name**: Name of participant associated with project.
4. **Recording Name**: Name of recording.
5. **Recording Date**: Date when recording was named. (Format: *YYYY-MM-DD)*
6. **Recording Start Time**: Time when recording process was started. (Format: *HH:MM:SS:mmm*)
7. **Recording Duration**: Duration of recording. (Format: *Milliseconds*)
8. **Timeline Name**: Name of timeline used during recording (only for **screen projects**).
9. **Recording Fixation Filter Name**: Name of gaze filter applied to the recording eye tracking data in the export.
10. **Snapshot Fixation Filter Name**: Name of the fixation filter applied to the snapshot eye tracking data in the export (only for **glasses projects**).
11. **Recording Software Version**: Version of the software used to make the recording.
12. **Recording Resolution Width**: Resolution width of the recording. (Format: *Pixels*)
13. **Recording Resolution Height**: Resolution height of the recording. (Format: *Pixels*)
14. **Recording Monitor Latency**: Monitor latency setting for the recording. The start and event timestamps have been offset by this number to account for the monitor latency (only for **screen projects**). (Format: *Milliseconds*)

##### Data Columns

1. **Recording Timestamp**: Timestamp counted from the start of recording (t0 = 0). (Format: *Milliseconds*)
2. **Eye Tracker Timestamp**: Recording timestamp in the eyetracker. (Format: *Milliseconds*)
3. **Gaze Point X**: Horizontal coordinate of the averaged left and right eye gaze point. (Format: *Pixels*)
4. **Gaze Point Y**: Vertical coordinate of the averaged left and right eye gaze point. (Format: *Pixels*)
5. **Gaze Point Left X**: Horizontal coordinate of the left eye gaze. (Format: *Pixels*)
6. **Gaze Point Left Y**: Vertical coordinate of the left eye gaze. (Format: *Pixels*)
7. **Gaze Point Right X**: Horizontal coordinate of the right eye gaze. (Format: *Pixels*)
8. **Gaze Point Right Y**: Vertical coordinate of the right eye gaze. (Format: *Pixels*)
9. **Gaze 3D Position Left X**: Left eye x-coordinate of gaze position in the scene camera coordinate system (only for **glasses projects**). (Format: *Millimeters*)
10. **Gaze 3D Position Left Y**: Left eye y-coordinate of gaze position in the scene camera coordinate system (only for **glasses projects**). (Format: *Millimeters*)
11. **Gaze 3D Position Left Z**: Left eye Z-coordinate of gaze position in the scene camera coordinate system (only for **glasses projects**). (Format: *Millimeters*)
12. **Gaze 3D Position Right X**: Right eye x-coordinate of gaze position in the scene camera coordinate system (only for **glasses project**s). (Format: *Millimeters*)
13. **Gaze 3D Position Right Y**: Right eye y-coordinate of gaze position in the scene camera coordinate system (only for **glasses project**s). (Format: *Millimeters*)
14. **Gaze 3D Position Right Z**: Right eye Z-coordinate of gaze position in the scene camera coordinate system (only for **glasses project**s). (Format: *Millimeters*)
15. **Gaze 3D Position Combined X**: Combined x-coordinate of gaze position in the scene camera coordinate system (only for **glasses project**s). (Format: *Millimeters*)
16. **Gaze 3D Position Combined Y**: Combined y-coordinate of gaze position in the scene camera coordinate system (only for **glasses project**s). (Format: *Millimeters*)
17. **Gaze 3D Position Combined Z**: Combined z-coordinate of gaze position in the scene camera coordinate system (only for **glasses project**s). (Format: *Millimeters*)
18. **Gaze Direction Left**: Gaze direction (X, Y, Z) of the left eye. (Format: *Millimeters*)
19. **Gaze Direction Right**: Gaze direction (X, Y, Z) of the right eye. (Format: *Millimeters*)
20. **Pupil Position Left**: Pupil position (X, Y, Z) of the left eye (only for **glasses projects**). (Format: *Millimeters*)
21. **Pupil Position Right**: Pupil position (X, Y, Z) of the right eye (only for **glasses projects**). (Format: *Millimeters*)
22. **Pupil Diameter Left**: Estimated size of the left eye pupil. (Format: *Millimeters*)
23. **Pupil Diameter Right**: Estimated size of the right eye pupil. (Format: *Millimeters*)
24. **Validity Left**: Indicates the confidence level that the left eye has been correctly identified. Values range from 0 (high confidence) to 4 (eye not found) (only for **screen projects**).
25. **Validity Right**: Indicates the confidence level that the right eye has been correctly identified. Values range from 0 (high confidence) to 4 (eye not found) (only for **screen projects**).
26. **Eye Position Left (RCSmm)**: (X, Y, Z) coordinate of the 3D position of the left eye (only for **screen projects**). (Format: *Millimeters*)
27. **Eye Position Right (RCSmm)**: (X, Y, Z) coordinate of the 3D position of the right eye (only for **screen projects**). (Format: *Millimeters*)
28. **Gaze Point Left (RCSmm)**: (X, Y, Z) coordinate of the 3D position of the unprocessed gaze point for the left eye on the screen (only for **screen projects**). (Format: *Millimeters*)
29. **Gaze Point Right (RCSmm)**: (X, Y, Z) coordinate of the 3D position of the unprocessed gaze point for the right eye on the screen (only for **screen projects**). (Format: *Millimeters*)
30. **Gaze Point Left (RCSpx)**: (X, Y, Z) coordinate of the 3D position of the unprocessed gaze point for the left eye on the screen (only for **screen projects**). (Format: *Pixels*)
31. **Gaze Point Right (RCSpx)**: (X, Y, Z) coordinate of the 3D position of the unprocessed gaze point for the right eye on the screen (only for **screen projects**). (Format: *Pixels*)
32. **Eye Movement Type**: Type of eye movement classified by the fixation filter. (Format: *Fixation, Saccade, Unclassified, Eyes Not Found*)
33. **Gaze Event Duration**: Duration of the currently active eye movement. (Format: *Milliseconds*)
34. **Eye Movement Type Index**: Count is an auto-increment number starting with 1 for each eye movement type. (Format: *Number*)
35. **Fixation Point X**: Horizontal coordinate of the averaged gaze point for both eyes. (Format: *Pixels*)
36. **Fixation Point Y**: Vertical coordinate of the averaged gaze point for both eyes. (Format: *Pixels*)
37. **Event**: Name of the event.
38. **Presented Stimulus Name**: Name of the stimulus being presented to the participant (only for **screen projects**).
39. **Presented Media Name**: Name of media presented to participant (only for **screen projects**).
40. **Presented Media Width**: Horizontal size of media presented on screen to participant, including scaling set by stimulus properties (only for **screen projects**). (Format: *Pixels*)
41. **Presented Media Height**: Vertical size of the media presented on screen to participant including scaling set by stimulus properties (only for **screen projects**). (Format: *Pixels*)
42. **Presented Media Position X**: Horizontal position of the media on the screen. Value represents the horizontal position of the left edge of the media in relation to the left edge of the screen (only for **screen projects**). (Format: *Pixels)*
43. **Presented Media Position Y**: Vertical position of the media on the screen. Value represents the vertical position of the top edge of the media in relation to the top edge of the screen (only for **screen projects**). (Format: *Pixels)*
44. **Original Media Width**: Original horizontal size of media presented to the participant (only for **screen projects**). (Format: *Pixels*)
45. **Original Media Height**: Original vertical size of media presented to the participant (only for **screen projects**). (Format: *Pixels*)
46. **Gaze Point X (MCSnorm)**: Normalized horizontal position of the averaged left and right eye gaze point on media (only for **screen project**s). (Format: *Normalized Coordinates*)
47. **Gaze Point Y (MCSnorm)**: Normalized vertical position of the averaged left and right eye gaze point on media (only for **screen project**s). (Format: *Normalized Coordinates*)
48. **Gaze Point Left X (MCSnorm)**: Normalized horizontal position of the unprocessed gaze point for the left eye on media (only for **screen projects**). (Format: *Normalized Coordinates*)
49. **Gaze Point Left Y (MCSnorm)**: Normalized vertical position of the unprocessed gaze point for the left eye on media (only for **screen projects**). (Format: *Normalized Coordinates*)
50. **Gaze Point Right X (MCSnorm)**: Normalized horizontal position of the unprocessed gaze point for the right eye on media (only for **screen projects**). (Format: *Normalized Coordinates*)
51. **Gaze Point Right Y (MCSnorm)**: Normalized vertical position of the unprocessed gaze point for the right eye on media (only for **screen projects**). (Format: *Normalized Coordinates*)
52. **Fixation Point X (MCSnorm)**: Normalized horizontal position of the fixation on the media (only for **screen projects**). (Format: *Normalized Coordinates)*
53. **Fixation Point Y (MCSnorm)**: Normalized vertical position of the fixation on the media (only for **screen projects**). (Format: *Normalized Coordinates)*
54. **Recording Media Name**: Name of the recording media.
55. **Recording Media Width**: Width of the recording media. (Format: *Pixels*)
56. **Recording Media Height**: Height of the recording media. (Format: *Pixels*)
57. **Media Width**: Width of media. Enabling this column generates one column per snapshot in a **glasses project**. (Format: *Pixels*)
58. **Media Height**: Height of media. Enabling this column generates one column per snapshot in a **glasses project**. (Format: *Pixels*)
59. **Mapped Gaze Data X [Snapshot Name]**: Horizontal coordinate of the gaze point mapped to a snapshot (only for **glasses projects**). (Format: *Pixels*)
60. **Mapped Gaze Data Y [Snapshot Name]**: Vertical coordinate of the gaze point mapped to a snapshot (only for **glasses projects**). (Format: *Pixels*)
61. **Mapped Eye Movement Type [Snapshot Name]**: Type of eye movement classified by the default fixation filter (only for **glasses projects**). (Format: *Fixation, Saccade, Eye Not Found, Unkown Eye Movement)*
62. **Mapped Eye Movement Index [Snapshot Name]**: An auto-increment number starting with 1 for each mapped eye movement type (only for **glasses projects**). (Format: *Number*)
63. **Mapped Fixation X [Snapshot Name]**: Horizontal coordinate of a fixation mapped to a snapshot (only for **glasses projects**). (Format: *Pixels*)
64. **Mapped Fixation Y [Snapshot Name]**: Vertical coordinate of a fixation mapped to a snapshot (only for **glasses projects**). (Format: *Pixels*)
65. **Automatically-Mapped Gaze Data Score [Snapshot Name]**: Validity score of the automatically-mapped gaze point. Enabling this generates one column per snapshot (only for **glasses projects**). (Format: *Pixels*)
66. **Automatically-Mapped Gaze Data X [Snapshot Name]**: Horizontal coordinate of the automatically-mapped gaze point (only for **glasses projects**). (Format: *Pixels*)
67. **Automatically-Mapped Gaze Data Y [Snapshot Name]**: Vertical coordinate of the automatically-mapped gaze point (only for **glasses projects**). (Format: *Pixels*)
68. **Manually-Mapped Gaze Data X [Snapshot Name]**: Horizontal coordinate of the manually-mapped gaze point (only for **glasses projects**). (Format: *Pixels*)
69. **Manually-Mapped Gaze Data Y [Snapshot Name]**: Vertical coordinate of the manually-mapped gaze point (only for **glasses projects**). (Format: *Pixels*)
70. **AOI Hit [Snapshot/Image Name - AOI Name]**: Reveals if there is a fixation within a given AOI on a given snapshot (only for **glasses projects**). (Format: *0;1*)
71. **Gyro**: Rotation along the X, Y, and Z axes in degrees/second (only for **glasses projects**). (Format: *degrees/second*)
72. **Accelerometer**: Acceleration along the X, Y, and Z axes (only for **glasses projects**). (Format: *degrees/second^2*)
73. **Galvanic Skin Response (GSR)**: Conductance received from the Shimmer GSR sensor. (Format: *Microsiemens*)

#### Exporting Data to Third-Party Programs

The Tobii Pro software allows the data and metric types detailed above to be outputted as an *XSLX-file* which can then be inputted into Excel and/or Matlab. Before this occurs the user can specify the specific metrics and data that will be present on the outputted file, choosing from the types named above in order to minimize te extraneous data in the file. This file can then be inputted into Matlab through built-in functions such as *xlsread*, being converted into a matrix that can be manipulated as needed by the user.

In the case that only a tsv file is available, the following steps should be done to use the data within Matlab:

1. Convert the tsv file to a csv file or xlsx file within Excel
2. Input the converted data into Matlab through functions such as *csvread,* or *readtable*
3. Manipulate the fully converted data as needed within the Matlab setting

## Sending Signals To and From the Glasses

The Tobii pro software supports transmission of signals through [[TTL signals](https://www.tobiipro.com/learn-and-support/faqs/can-tobii-pro-glasses-2-accept-ttl-signals-for-synchronization/)], set up within the software and being able to be transmitted between the glasses and the computer the software is on. Here, the more important aspect is the ability to input signals, as with this the onset of stimuli can be automatically mapped with high accuracy by the processor of the glasses and the software itself, making it easier to later classify, manipulate, and analyze data without much input from the user. This process is easily setup within the software itself, with the glasses featuring an easily accessible synchronization port.

In a traditional EEG setting this could be used by transmitting TTL signals to the eye tracking glasses dictating the stimulus onset time, this also being placed in the data that can be exported for further analysis.

## Possible Method for Typical ECOG Setting

The following is a step-by-step method of implementing the Tobii Pro glasses and its corresponding analysis software in a typical ECOG setting, according to the generation of data, its manipulation within the Tobii software and outside of it, and the use of external tools to simplify the overall process.

**Using TTL Signals**:

1. Hook up testing machine with TTL outputting capabilities to the Tobii Pro Glasses
2. Initialize both the recording through the glasses and the experiment.
3. As the experiment proceeds, use the accompanying software to ensure that the patient is actively cooperating, and to check that the TTL-sent onsets are being accurately mapped.
4. After the experiment, check the data within the analysis software, manually remapping gaze points and/or onset/offset points as needed.
5. If needed manually generate custom TOIs to be used for classification of exported data.
6. Select the specific data and metric types you want to export and export them as a tsv.
7. Use MATLAB or any other external data analyzing software to tie in recorded data with the ECOG data, taking out data that doesn't correspond to mapped eye movement, fixations/micro-saccades, or where the gaze data was not concentrated on the stimulus.

**Using AOIs** (To be used if stimulus involves dynamic movement):

1. If TTL signaling can still be used hook up the outputting machine to the Tobii glasses to enable synchronization of data, if not skip this step.
2. Initialize both the recording through the glasses and the experiment.
3. As the experiment proceeds ensure patient is actively engaging with the experiment and that the data being recorded is correct.
4. After the experiment, generate dynamic stimulus AOIs through the software.
5. Once processing of the AOIs is finished check each generated TOI to ensure that everything was mapped correctly, remapping points manually as needed.
6. If needed manually generate custom TOIs to be used for classification of exported data.
7. Select the specific data and metric types you want to export and export them as a tsv.
8. Use MATLAB or any other external data analyzing software to tie in recorded data with the ECOG data, taking out data that doesn't correspond to mapped eye movement, fixations/micro-saccades, or where the gaze data was not concentrated on the stimulus.

**Using Snapshots**:

1. If TTL signaling can still be used hook up the outputting machine to the Tobii glasses to enable synchronization of data, if not skip this step.
2. Initialize both the recording through the glasses and the experiment.
3. As the experiment proceeds ensure patient is actively engaging with the experiment and that the data being recorded is correct.
4. After the experiment, import snapshots of stimuli, ensuring that the stimuli are static (motion), that the images are from a direct perspective (taken from directly in front of the screen or screens from the program itself), and let the software run its automatic snapshot analysis with the data.
5. After the analysis is complete make sure all of the automatically mapped data is correct, manually mapping in any incorrect data as needed.
6. If needed manually generate custom TOIs to be used for classification of exported data.
7. Select the specific data and metric types you want to export and export them as a tsv.
8. Use MATLAB or any other external data analyzing software to tie in recorded data with the ECOG data, taking out data that doesn't correspond to mapped eye movement, fixations/micro-saccades, or where the gaze data was not concentrated on the stimulus.

### **MATLAB Use**

After the previously mentioned steps one could use the MATLAB script (tobii\_main) located [here](https://drive.google.com/file/d/0B1D7pO1r_W64SFc0WkRIRXE5b2c/view?usp=sharing) to deconstruct the tsv data from the Tobii Pro software into arrays of time-point data that can be used with other traditional time-series data.
