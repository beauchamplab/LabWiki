# VideoStimulusCreation

> **Navigation:** [Home](index.md) • [Publications](Publications.md) • [Resources](DataSharing.md)

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

## Notes on Video Stimulus Creation

Most older stimuli in the lab use the xvid codec.
This has the advantage of being free, but is not as widely supported.
Therefore, newer stimuli use the H.264 codec.
To convert, we can use HandBrake on the Mac or mencorder (<http://www.mplayerhq.hu/design7/news.html>)

## Installing Adobe Premiere

1. Go to <https://www.adobe.com>
2. Click "Sign In" at the top right.
3. For Email Address, enter "Upenn.edu" and click on continue. You will be redirected to the Penn WebLogin Page.
4. Sign in with your PennKey and password.
5. Once you have signed in, you will be redirected to the Adobe page.
6. Next, go to "Help & Support" -> "Download and Install". You will be presented with all the available applications.
7. Download and install Premiere Pro.

## Adobe Premiere Tutorial

For a tutorial on the basics of Premiere, head over to [this link](https://www.adobe.com/max/2021/sessions/learning-premiere-pro-basics-in-one-hour-l572.html).

## Using Adobe Premiere to make the Video Stimulus

#### Creating a new project

1. Open Adobe Premiere.
2. Click on "New Project" at the top left.
3. Type in the name of your project and click on "OK".

#### Importing media files into Premiere

1. Double click on the "Project" window at the bottom left. This will open up the "Finder" window on Mac, or "My Computer" on Windows.
2. Navigate to the folder that contains your media files. Choose them and click on "Import".

#### Editing the imported files

1. Drag & drop the files (Video + Audio files) you want to combine/edit onto the "Timeline" window.
2. Next, unlink the original sound (shift-click right and scroll down to ‘unlink’)from the video and delete it (right click and select cut).
3. To add the audio, there are two choices :
   - Record audio on your phone and import the recording to your project. Adjust the length of the recording to match the video.
   OR- Record voice-over on Premiere : Select the track in the Timeline to which you want to add the voice-over. Click the mic icon to start (/stop) recording.

#### Normalizing Audio

It is important to ensure that the audio files are the same volume (especially since differences in inflection can also cause one to increase/decrease pitch when speaking).

1. Drag the cursor over all the audio files, right click, then scroll down the menu to select “Audio”.
2. Another side menu will appear and then select “Normalize”.
3. From here, you set the standard volume for all audio files (ex. -60 dB) and then hit enter.

You should see the sound waves for each recording adjust accordingly.

#### Exporting your edited video

To save your video,

1. Click on "File" -> "Export" -> "Media".
2. Choose the required format and type in the name of your file.
3. Click on "Export".

To save it as an mp4 file, after step 1 above choose the following for "Format" and "Preset" :

- **Format** : H.264
- **Preset** : Match Source - Medium Bitrate

To export only Audio, uncheck the "Export Video" option and choose your audio format.
