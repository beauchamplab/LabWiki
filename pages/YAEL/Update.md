# Update

> **Navigation:** [Home](../Beauchamp/index.md) • [Publications](../Beauchamp/Publications.md) • [Resources](../Beauchamp/DataSharing.md)

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/RAVE/RAVE_Logo_new.jpg) | **Y**our **A**dvanced **E**lectrode **L**ocalizer   ***YAEL*** |

- [Home](index.md "YAEL")
- [Install](Install.md "YAEL:Install")
- Update
- [Launching](Launching.md "YAEL:Launching")
- [Tutorials and Help](Help.md "YAEL:Help")
- [Community](Community.md "YAEL:Community")

## Updating and Upgrading YAEL

For more efficient software maintenance, RAVE and YAEL are installed and updated together because they share common elements. The steps below will update both YAEL and RAVE.

Because YAEL runs on top of R and RStudio, it is important to update both of these before updating RAVE.
For major updates (about every 6-12 months) it is necessary to completely reinstall:
<Install_prerequisites.md#2._R_and_R_Studio>
For minor updates, start RStudio, "Help"/"Check for Updates"; start R, "R"/"Check For R Updates").

Regardless of your current YAEL version, enter the following command into the R console

```
 ravemanager::version_info()
```

This prints out current RAVE package versions. If all the core packages are up-to-date, you will see the message "Everything is up to date", otherwise please follow the following steps.
Quit all instance of "R" and "RStudio" before proceeding, or RAVE will not be able to update. Restart R and enter the following command into the R console

```
 lib_path <- Sys.getenv("RAVE_LIB_PATH", unset = Sys.getenv("R_LIBS_USER", unset = .libPaths()[[1]]))
 loadNamespace("ravemanager", lib.loc = lib_path)
 ravemanager::update_rave()
```

Press "enter" if you are asked "yes/no/cancel".

**After this command completes, quit and restart RStudio**. Then restart the updated RAVE:

```
 rave::start_yael()
```

Notes: Be sure to quit ALL other running R and RStudio instances before running "ravemanager::update\_rave()", otherwise packages will be locked and upgrade will fail. For other problems, the fallback is to completely reinstall RAVE.
