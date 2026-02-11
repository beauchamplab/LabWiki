---
title: electrode-localization
parent: RAVE
---
# electrode-localization

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/vignettes:electrode-localization/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

RAVE provides a complete pipeline to localize the iEEG electrodes using imaging data from each patient. MR imaging (which shows high-resolution brain anatomy) is collected before electrode implantation while CT imaging (which shows the precise location of electrodes) is collected after implantation. Localizing electrodes can be accomplished within the RAVE GUI using the following steps:

1. The dcm2niix script consolidate the MRI and CT raw data (series of many DICOM images) into two Nifti-1 (.nii) files.
2. To bring the MRI and CT datasets into alignment, RAVE calls image registration routines from either AFNI or FSL (the user can specify which).
3. The MR dataset is skull-stripped and normalized.
4. RAVE shows the CT data overlaid on the MRI dataset in the 3D viewer.
5. Users select electrode locations in the 3D viewer. RAVE provide a variety of tools to make this easier, faster and more accurate.

## Convert DICOM to NifTi and Import to RAVE

In the GUI, click on the "Import MRI button".
If you see error message "can't find dcm2niix" then go to this web page to install it:

```
 https://github.com/rordenlab/dcm2niix#install
```

RAVE uses Nifti format to read and process the imaging data. However, most MR and CT scanners store imaging slices in DICOM files. To import the CT and MR images in DICOM files, an external `dcm2niix` program is needed. To install `dcm2niix`, please check their official website <https://github.com/rordenlab/dcm2niix#install>.

Once `dcm2niix` is installed and added to the system path, users can test the installation by opening the shell terminal (e.g. bash, zsh) and typing the following command:

```
 dcm2niix -v
```

If users see a message that is similar to the following output, congratulations, `dcm2niix` is installed.

```
Chris Rorden's dcm2niiX version v1.0.20211006  Clang13.0.0 ARM (64-bit MacOS) v1.0.20211006
```

In normal situations, RAVE should automatically detect the location of `dcm2niix`. Users can check the `dcm2niix` path by running the following R command:

```
 raveio::cmd_dcm2niix()
 #> [1] "/opt/homebrew/Cellar/dcm2niix/1.0.20211006/bin/dcm2niix"
```

If this command returns an empty string or raises an error, please manually set the `dcm2niix` by running the following command. Please replace the keyword \*"path to dcm2niix"\* to the actual `dcm2niix` path accordingly.

```
 raveio::raveio_setopt("dcm2niix_path", "path to dcm2niix")
```

Please make sure `raveio::cmd\_dcm2niix()` returns a valid path before proceeding to the next step, otherwise the rest command will result in errors.

Once the RAVE command `raveio::cmd\_dcm2niix()` returns a valid path, the next procedure is to merge DICOM files into NifTi format. This step can be easily accomplished by running the RAVE command

```
 raveio::cmd_run_dcm2niix(subject, source_path, type)
```

where `subject` is a valid RAVE subject string, `source\_path` is the file directory containing DICOM images, and `type` specifies the image type. For example, to import T1 MRI located at "~/Documents/scans/YAB/MRI" for subject "demo/YAB", users can simply run

```
 raveio::cmd_run_dcm2niix(subject = "demo/YAB", source_path = "~/Documents/scans/YAB/MRI", type = "MRI")
```

If the image is CT, the argument `type` needs to be changed to "CT".

In the backend, RAVE creates a working directory "rave-imaging" under the subject's raw folder. In this directory, four sub-folders will be created. They are "scripts", "log", "inputs/MRI", and "inputs/CT". When importing the T1 MRI (with `type="MRI"`), `raveio::cmd\_run\_dcm2niix` first saves the shell script to "scripts/cmd-import-mri.sh", then internally RAVE invokes shell command to execute this file. All the messages will be saved to "log/log-dcm2niix-xxx.log". Finally, if any NifTi files are generated, they will be saved under "inputs/MRI". For CT images, this procedure is the same, except that the saved files will be under the folder "inputs/CT".

In some institutions, there are existing pipelines that convert DICOM to NifTi, hence there is no need to repeat this procedure. In this case, please set the argument `source\_path` to the NifTi file, and `raveio::cmd\_run\_dcm2niix` will automatically check the file format and copy it to the RAVE directory. We highly recommended that users use this RAVE function to import imaging files to avoid any manual file manipulations, which could be error pruning.

Once T1 MRI is imported, users can normalize the images, strip the skulls, or reconstruct the brain surfaces via FreeSurfer. If the CT images are also imported, the CT-MRI coregistration can be accomplished via AFNI or FSL. Please check the next two sections for technical details.
