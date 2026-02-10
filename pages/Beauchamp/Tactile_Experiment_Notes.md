# Tactile Experiment Notes

> **Navigation:** [Home](index.md) | [Publications](Publications.md) | [Resources](DataSharing.md)

1- Do not exceed 90 Volts Peak to the Piezos

2- Pay attention to the clipping of various amplifiers:

**a)** Lenovo T61 Laptop’s soundcard output is pretty much linear up to 75% volume after which it clips the waveforms (red shade in the plot). Below is a plot of the output audio voltage of this laptop as a function of its volume:

[![](../../attachments/Tactile_Experiment_Notes/Lenovo_T61_Laptop_Audio_output.jpg)](../../attachments/Tactile_Experiment_Notes/Lenovo_T61_Laptop_Audio_output.jpg)

At 42% volume, the output is 1 Volt.

**b)** Macbook Pro does not clip waveforms even at 100% volume but when the power supply is plugged in, the audio signal picks up some noise. Below is a plot of the output audio voltage of this laptop as a function of its volume:

[![](../../attachments/Tactile_Experiment_Notes/MacbookPro_Audio_output.jpg)](../../attachments/Tactile_Experiment_Notes/MacbookPro_Audio_output.jpg)

**c)** PylePro PCA1 amplifier clips at 8.6V Peak (17.2V Peak-to-Peak). Below is a plot of the its gain as adjusted by its knob:

[![](../../attachments/Tactile_Experiment_Notes/PylePro_amplifier_gain.jpg)](../../attachments/Tactile_Experiment_Notes/PylePro_amplifier_gain.jpg)

So with this amplifier:

- With Lenovo at 75% volume do not exceed 4.9X gain

- With MacBookPro at 100% volume do not exceed 2.8X gain

**d)** The Sony Home Theater amplifier seems to saturate at ~33 Volts. So to be on the safe side do not exceed 28 V. Its volume is scaled from 0-74 but the amplification is nonlinear (~logarithmic). The amplification graph was experimentally determined to be:

[![](../../attachments/Tactile_Experiment_Notes/Sony_STR_DG500_amplification_graph.jpg)](../../attachments/Tactile_Experiment_Notes/Sony_STR_DG500_amplification_graph.jpg)

So if the laptop is playing a waveform at its maximum output per a) above which is 60% or 15 out of 25 (1.65 volts output) then 28/1.65≈17X amplification is needed which according to the graph above would mean that the Sony volume should not exceed ~62 (on its 0-74 scale) [data in the file Sony\_STR\_DG500\_Amplification\_Graph.xls on data2\TMS\Siavash]

**e)** The Pioneer VSX-517 Home Theater amplifier did not up to maximum tested voltage of ~200V. Its volume (attenuation) is scaled from 0-94 and the amplification is again nonlinear (~logarithmic). The amplification graph was experimentally determined to be:

[![](../../attachments/Tactile_Experiment_Notes/Pioneer_vsx_517_gain_plot.jpg)](../../attachments/Tactile_Experiment_Notes/Pioneer_vsx_517_gain_plot.jpg)

If we want 90V to go to Piezos and the laptop is playing a waveform at its maximum output per a) above which is 60% or 15 out of 25 (1.65 volts output) then 90/1.65 ≈ 55X amplification is needed which according to the graph above corresponds to attenuation of -7 dB on the Pioneer amplifier (on its 0 to -94 scale). [data in the file Pioneer\_VSX\_517\_gain.xls on data2\TMS\Siavash]

**f)** Krohn-Hite 7500 amplifier did not saturate at the maximum tested voltage of 170V. Note that the amplification gain of this amplifier is also nonlinear. When using the 0-100 variable gain, the dial has 3 notches between 0 and 100. The first notch is ~2X, the second one is ~8X, and the third one is ~35X. Given that we don’t want to put more than 90V through the Piezos, if a waveform is played on the laptop at the maximum allowed volume of 15 (on the 0-25 scale), then the Gain dial should be only slightly past the third notch. Use a 10X oscilloscope probe to find the exact location.

3. The simplest method to generate waveforms to drive the piezos is to use the auditory output from a computer, possibly amplified (by an amplifier, above). The waveform can be generated directly in Presentation by the AudioSpace library, or for more sophisticated waveforms, an audio file can be made in another program, like Matlab, and played back in Presentation (or Python).
Here is Matlab code to make a simple touch stimulus using a Gaussian monopulse (GMP).

The GMP is like one cycle of a sine wave; therefore, the center frequency (cf) should equal the approximate desired duration of your pulse,
e.g.
a 200 Hz cf produces a GMP of duration 6.2 ms. This produces a good touch percept.
sampling frequency (sf) is typically 44100 (CD audio)

```
 cf = 200
 sf = 44100
 tc = gmonopuls('cutoff',cf)
 t = -2*tc:1/sf: 2*tc;
 snd = gmonopuls(t,cf);
```

To hear the sound in Matlab, type

```
 sound(snd,sf)
```

To save the sound to disk, additional options are needed:
number of bits is usually 16 (also standard CD audio).
Linear is standard for compression of amplitudes

```
 auwrite(snd,sf,16,'linear','s1.au');
```

This writes out an .AU file that must be converted to .WAV using another program, such as "Awave Audio"
Alternately, a WAV file can be written out directly

```
 wavwrite(snd,sf,'s1.wav');
```

To make multiple channels, create a matrix with multiple columns and save as above. This may only work for AU files.
A sound file with only a single column is a "mono" file, and should be played through all speakers equally. However, Presentation may interpret it as being a stereo file with all of the sound in the left channel and no sound in the right channel. Therefore, if you wish to play the sound through both channels, it is good to make a stereo file with both columns identical. This can also be made after the fact in a sound editing program like Audacity.

Notes on playing sounds and videos in Presentation software
To avoid the drawbacks of Presentation, it may be preferable to play videos and sounds in Python. However, this is more difficult and requires extensive programming.

In general, playing videos in Presentation is relatively simple:

```
 trial {
  video { filename = "D5v2_100.avi"; } v2;      
  } t2; 
  t2.present();
```

Shows the video, as long as the correct CODECs are installed. The same CODEC must be used to create and playback the clip.
xVid from www.xvid.org is recommended because it is high quality, creates small files, and is GPL.
Frame-by-frame control of video playback is possible but makes video playback appear much choppier.

```
 vid.set_end_frame( 34 );
```

tells presentation to stop playback after the 34th frame.
However, this makes playback choppier as Presentation checks after each frame to see if frame 34 has been reached.
There are other unexpected interactions as well. Turning audio off, or using a custom mixer, can slow or stop playback for unclear reasons.
Therefore, if it desired to stop and resume playback at a certain point, it may be better to simply create two movie clips and play each of the uniterrupted with a gap in between.
