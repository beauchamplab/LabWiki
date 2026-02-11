> **Navigation:** [Home](index.md) • [Install](Install.md) • [Help](Help.md)

# select data

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/select_data/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

**Select data to load**

1. Choose the **Project** using the drop-down menu. For data located outside the default directory, point RAVE to it with

```
rave::rave_options()
```

1. Choose a **Subject** using the dropdown menu of the different subjects that are available for a given project.
2. Choose the **Epoch Table** and select the window to load around the epoch.
3. Select **Electrodes** by specifying a range (e.g., 4-20), or individual electrodes (4, 8, 19) or a combination (4-20, 23, 34-35). Invalid electrode numbers are automatically skipped. You can also use a mask file to select specific electrodes. Click 'Load Mask' to select file. Note you should delete any entries under 'Electrodes' so the text box is blank prior to loading mask.
4. After selection of a subject and electrodes, click on **> Load Data** in the bottom right corner

[![Data Selection](../../attachments/select_data/Data_selection_output.png)](../../attachments/select_data/Data_selection_output.png "Data Selection")

:   [Return to Getting Started.](RAVEGUI_Help.md "RAVE:RAVEGUI Help")
