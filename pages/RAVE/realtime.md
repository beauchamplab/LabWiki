> **Navigation:** [Home](index.md) | [Install](Install.md) | [Help](Help.md)

# realtime

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/realtime/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

1. Ensure that the BlackRock files from the NSP are sync-ed to DropBox
2. Copy each raw files to a separate directory, e.g.

```
 beauchamplab\rave_data\raw_dir\PAV010\Block23\
```

1. if needed, use rave::rave\_options to change directory

```
 rave::start_rave2
```

1. Import Signals, Notch Filter, Wavelet (speed up with down-sample=2 and single-float)
