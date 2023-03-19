# LabBench Beta Program [beta.labbench.io]

This repository contains protocols that are intended for testing Beta versions of LabBench. Beta versions of LabBench are versions of LabBench that are not yet officially released but are being tested by research groups collaborating with Inventors' Way as part of the LabBench Beta Program. The purpose of the LabBench Beta Program is a collaboration between researchers at academic institutions and the developers of LabBench that aims to create novel and open methods and devices for neuroscience research.

Currently, the following laboratories and sites participate in the LabBench Beta Program:

| Site  | Principal Investigator  | Area         |
|-------|----------|----|
| [Integrative Neuroscience Research Group, Aalborg University](https://vbn.aau.dk/en/organisations/integrative-neuroscience) | [Carsten D. Mørch]() | Research into the neuroscience of pain that aims at understanding the basic mechanisms of the pain system. Development of methods to investigate how nociceptors generate and mediate pain signals in healthy humans and pathological situations. <br /> **Beta Program focus: Development of functionality in LabBench for Perception Threshold Tracking.**
| [Steno Diabetes Center Northen Jutland](https://stenodiabetescenter.rn.dk/Forskning/Forskningsprojekter-i-SDCN/MEDON) | [Johan Røikjer]() | Research aimed at early detection of diabetic polyneuropathy which includes the use of perception threshold tracking. <br /> **Beta Program focus: Development of functionality in LabBench for Perception Threshold Tracking.** |
| [Translational Biomarkers in Pain and Precision Medicine Research Group, Aalborg University]() | [Laura Petrini](https://vbn.aau.dk/da/persons/112436)| Research in how to assess pain in elderly and vulnerable populations. <br /> **Beta Program focus: Development of functionality in LabBench for studying pain catastrophizing** |
| [?]() | [Sabata Gervasio]() | Research on sensory thresholds and sensory processing in children with autism. <br /> **Beta Program focus: Development of functionality in LabBench for studying sensory processing, such as auditory and tactile psychophysical tests, and functionality for recording auditory and tactile evoked potentials** |

If LabBench does not adequately support your research and you would like to see that change, then write to (help@labbench.io) to become a member of this Beta program. By participating in this program, you will gain access to versions of LabBench before they become generally available, have its development tailored to fit your exact research needs, and have access to extensive support in running your experiments. In return the LabBench developers gain access to your expert knowledge and help in making LabBench better for your area of research.

## LabBench Beta

### What is the Beta version of LabBench

The Beta version of LabBench is what we call a release candidate (rc) for the next upcoming release of LabBench; this means that it has yet to go through the official release process and contains experimental functionality yet to mature enough for general use.

### Installation

Installation and use of LabBench Beta is done in close collaboration with the developers of LabBench. When you need to install LabBnech Beta you will receive a download link to an zip file containing the executable files for the program. However, as it is not officially released there is not an installer for the program. Instead to use LabBench Beta you will go through the following steps the first time you install LabBench Beta on your lab computer.

**FIRST TIME INSTALLATION:**

1. Unpack the zip file to ```C:\Tools\LabBench```
2. Mark the labbench.exe file in that directory, and press Ctrl + C. 
3. Goto the Desktop, right click on the desktop and choose "Paste shortcut". Do this twice.
4. Setup one shortcut to start the LabBench Designer program:
    1. Mark the shortcut and press F2. Rename it to say ```LabBench Designer (Beta)```.
    2. Right click the shortcut and click on Properties.
    3. Change Target to: ```C:\Tools\LabBench\LabBench.exe designer -p C:\LabBeta```. If you kept the path ```C:\Tools\LabBench``` in step 1, you can copy paste this line from here to the Target property in the shortcut.
    4. Test the shortcut by double clicking it and see that it start the LabBench Designer. Close the program before you proceed to step 5 in this installation procedure.
5. Setup the other shortcut to start the LabBench Runner program:
    1. Mark the shortcut and press F2. Rename it to say ```LabBench Runner (Beta)```.
    2. Right click the shortcut and click on Properties.
    3. Change Target to: ```C:\Tools\LabBench\LabBench.exe runner -p C:\LabBeta```. If you kept the path ```C:\Tools\LabBench``` in step 1, you can copy paste this line from here to the Target property in the shortcut.
    4. Test the shortcut by double clicking it and see that it start the LabBench Runner. Close the program before you proceed to step 5 in this installation procedure.

**UPDATING LABBENCH BETA:**

To update LabBench Beta.

1. Delete all files in ```C:\Tools\LabBench```
2. Unpack the zip file to ```C:\Tools\LabBench```

## LabBench Beta Protocol Repository

