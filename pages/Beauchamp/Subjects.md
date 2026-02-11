---
layout: default
title: "Subjects"
parent: Beauchamp
---
# Subjects


|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

- [Home](index.md "Beauchamp")
- [Publications](Publications.md "Beauchamp:Publications")
- [Resources](DataSharing.md "Beauchamp:DataSharing")

## Lab Location

The lab is located in the Core for Advanced MRI at Baylor College of Medicine (CAMRI). CAMRI is located on the first floor of the Smith Research Wing of Baylor College of Medicine. Here is a map of Baylor College of Medicine showing the location of the Smith Research Wing:

```
 https://www.bcm.edu/map#!BCMS
```

Visitors to CAMRI can enter BCM at one of two entrances.
The first, the main entrance to BCM, is located at 1 Baylor Plaza, Houston, TX. This entrance is most convenient for those walking, being dropped off, or taking public transit.
The second is the entrance to BCM from Garage 6, and is most convenient for those driving. Texas Medical Center Garage 6, 1300 Moursund St, Houston, TX 77030. After parking, take the elevator to the ground floor.
More information on parking at TMC is available at

```
 http://www.texasmedicalcenter.org/parking/visitors/
```

To enter Baylor College of Medicine, non-employees must have a government-issued ID and obtain a temporary badge at a security desk. Visitors must be approved by a BCM employee. To obtain approval, call CAMRI reception at 713-798-4214, or call
(713)798-3175 (Dr. Beauchamp direct line) or (713)798-1838 (lab phone) or (301)768-8758 (Dr. Beauchamp cell phone) if you need help.

Subjects who are interested but who have not been studied are in the file

```
 open /Volumes/data2/interestedsubjects.txt
```

A handy website for scheduling subjects is

```
 http://www.signupgenius.com/
```

The username is beauchamplab@gmail.com; ask MSB for the password.

The web site for human subjects education is
<http://www.citiprogram.org>

All subjects for ALL experiments MUST be entered into the ExperimentSummary spreadsheet on the server, including all demographic data.

**Forms**: Before scanning, please print the forms out, fill it in, and take to the scanner.

[Beauchamp Lab consent form (Protocol H-36039) that must be signed by all subjects](../../attachments/Subjects/ConsentForm_March2020.pdf "ConsentForm March2020.pdf")

[BCM CAMRI MRI Subject Screening Form (as of 2020)](../../attachments/Subjects/MRIScreeningformCAMRI.pdf "MRIScreeningformCAMRI.pdf")

Form #2: Subject payment form for [adults](../../attachments/Subjects/BeauchampSubjectPaymentForm_Adult.doc "BeauchampSubjectPaymentForm Adult.doc") and [children](../../attachments/Subjects/BeauchampSubjectPaymentForm_Children.doc "BeauchampSubjectPaymentForm Children.doc")
General BCM Payment Form "Reimbursement"
Fill out top with name/address, two places for them to sign; scan them in and place in subject directory.
Fill out summary form after you have a lot of forms.
Then, give to Donna and we get more.

(NOTE: the reimbursement form is: /Volumes/data/lab/paymentlogs/Baylor/BCM\_PettyCash\_PaymentForm.doc
AND, the summary sheet for reimbursement is: /Volumes/data/lab/paymentlogs/blanksafeforms.xlsx)

[Form #2: Subject Payment Form](../../attachments/Subjects/Subject_payment_form.pdf)

The experimenter must fill out an [Experiment Sheet](../../attachments/Subjects/BeauchampLabExperimentSheet_Aug2008.doc "BeauchampLabExperimentSheet Aug2008.doc") (here's one specific for [Yoshor experiments](../../attachments/Subjects/YoshorExptSheet.doc "YoshorExptSheet.doc"))

**Scanning at BCM**
Ask for the password of the experiment computer.
Instructions for accessing the BCM scanner calendar are on the Beauchamp Lab Google Docs page.
The phone number in the control from for 3T-5 is 713-798-9041

**Scanning Documents**: After the experiment, all forms must be scanned in and placed in the subject's experiment directory.
The scanner scans both sides of every page automatically, so please use the back of the experiment sheet and print the consent form two-sided.

An e-mail that could be used for subject recruitment is

```
 UTfmri@gmail.com
```

**Coordinator for Dr. Yoshor's patients**: Pam Wilson

**Scheduling**: Make sure to tell Leticia that this is a Yoshor subject (to ensure the correct account is charged). Pam will work with Audrey to determine available dates for patient scanning. She will schedule the scans at UT (typically within 2 weeks prior to implantation). Make sure patients are able to wear contact lenses and have decongestants/allergy medication with them!

**Consents**: Pam will mail them the consent forms in advance. Audrey will collect Mike and Daniel's consent forms. She will put a PDF copy of the consent forms on the server and send a copy to Ping (who can slip it into the patient binder). A hard copy of the consent forms should be given to Daniel in a folder as well.

**Payment**: Day before the scan, give Susan Papalexandris an [IOU form](../../attachments/Subjects/PaymentIOU.doc "PaymentIOU.doc") and pick up the money (call her first @ 5606). The subject is paid at the time of the scan, and fills out a [Subject Payment Form](../../attachments/Subjects/Subject_payment_form.pdf) (above). Make it clear to the subject that the payment is for the fMRI study (and not for any electrophys experiments later). This can be exchanged by the experimenter with Susan for reimbursement.

**Day of scan**: Pam will coordinate escorts with Audrey (since the patient will be getting their presurgical workup done as well as their structural and functional research scans). Pam will handle lunch and parking reimbursement. Give payment and sign forms. Go over the tasks with the patient on the laptop and explain instructions. For Yoshor patients ONLY, a CD with \*ONE\* T1 scan in DICOM format (.DCM files) must be created by Vips and then given to Yoshor or a representative. Call Pam afterwards and find out where to send the patient. Update the pt info spreadsheet, scan in documents, copy Beauchamp consent for Daniel. Copy over Presentation files into "behavioral data" folder on the server. Return payment receipt to Susan.

**MRI processing**: In the days between the scan and implantation, Audrey will make a cortical surface model. Make functional maps if time permits.

**CT scan**: Once post-implantation CT is acquired, Daniel will contact Audrey regarding where to pick it up. When she comes to pick up the CT, she will load both the structural MR and CT images onto Stealth. This will be used for anatomical orientation in case the CT-MRI merge by AFNI is not done in time for experiments. She will pick up the electrode assignments from Lisa in St. Luke's (22nd floor) and scan in the drawings.

**CT-afni merge**: Open OsiriX. Import DICOM folder from post-implantation CT. Export to data9 surface folder (hierarchical, decompress). Cd to the StealthBrain folder. Open to3d window (to3d IM-\*), select x, y and z boxes, give prefix a name and save as {$ec}\_CT. Quit to3d. Copy {$ec}\_CT files into subject's afni folder. View {$ec}\_CT in afni, make sure somewhat aligned. Use 3dAllineate to align CT to T1.

**Tagging electrodes**: In afni, set underlay to the anatomical (either T1 or SurfVol), overlay to aligned CT. Define Datamode- Plugins- Edit Tagset. Set dataset to be a +orig file (not .nii) of anatomy (T1 or surface). Tagfile = {$ec}electrodes.tag, then set each tag label to however the drawings are labelled by entering in "Tag Label" and then pressing "Relabel". For each electrode of note from Lisa's drawings, find densest view of electrode, make sure it's centered in other views. Zoom in to make sure it's centered. Press "set". Do this for all electrodes. When done, press "Write" to write the data file. Make another copy of {$ec}electrodes.tag as {$ec}electrodes.1D for surface nodes. Edit the file so that it only has the 3 columns of x,y,z. First line #spheres. Open up SUMA, set the overlay with functional maps. Then, press ctrl-command-s and select {$ec}electrodes.1D. Now the electrode spheres should appear on the fMRI activation map. Take snapshots of electrodes on interesting functional activations.

**Items to put in patient binder**: Printed snapshots, DVD labeled with both Mike and Daniel's codes that includes the relevant AFNI data to view (on the mac in Y2230) the electrodes and functional activations on the cortical surfaces, printout of the pt info spreadsheet.

**NEW--ClinCard Payment**
Before your scan, the department/PI should have already set up the study online (Greenphire), and picked up some pre-paid ClinCards. (Check details on how to set up the study on Greenphire: /Volumes/data/lab/paymentlogs/CLINCARD\_TRAINING or email clincard@bcm.edu for assistance)

```
    During study visit: After the scan, ask the participant to fill out the Research Subject/Donor ClinCard Acknowledge Form (record the Clincard # and payment amount, this form should be kept at lab for the coordinator to use).
```

[Media:Research\_Subject/Donor ClinCard Acknowledge Form.pdf](#)

```
    The first three sections needed to be all filled and signed by all subjects: Participant/Donor Section, SSN/ITIN Section, and ClinCard Stipend Disbursement Section.
    (note: for repeated visits, use the same form for the participant, and only fill from section4)
    Give the participants the Clincard and instructions for ClinCards (Greenphire ClinCard Cardholder FAQ.pdf)
```

[Media:Research\_Subject/ClinCard\_Cardholder\_FAQ.pdf](#)

```
   After study visit: Register the participant in Greenphire (http://clincard.com/login/), assign the participant to the specific study and submit payments for the visit.
   (note: the payment needs to be approved by the approval personnel from the study, and Greenphire will load the payment amount to the ClinCard # 48-72hours; participants can choose to be notified when the payment is loaded when filling the Acknowledge form).
```
