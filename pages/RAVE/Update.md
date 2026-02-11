> **Navigation:** [Home](index.md) • [Install](Install.md) • [Help](Help.md)

# Update

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/Update/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

Thank you for visiting the RAVE wiki update instructions, for the current version, visit:

### [New RAVE update instructions](https://rave.wiki/posts/installation/update.html)

[Click here for notes on editing the new website](https://rave.wiki/posts/editor-notes/how-to-edit-this-website.html)

### Updating and Upgrading RAVE

Because RAVE runs on top of R and RStudio, it is important to update both of these before updating RAVE.
For major updates (about every 6-12 months) it is necessary to completely reinstall:
[Install prerequisites](Install_prerequisites.md#2._R_and_R_Studio)
For minor updates, start RStudio, "Help"/"Check for Updates"; start R, "R"/"Check For R Updates").

If you have a RAVE version older than October 2022, you must first enter the following command into the R console (if you are not sure, it is OK to run it just in case).

```
 lib_path <- Sys.getenv("RAVE_LIB_PATH", unset = Sys.getenv("R_LIBS_USER", unset = .libPaths()[[1]]))
 install.packages('ravemanager', repos = 'https://rave-ieeg.r-universe.dev', lib = lib_path)
```

Regardless of your current RAVE version, enter the following command into the R console

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

After this command completes, quit and restart RStudio. Then restart the updated RAVE:

```
 rave::start_rave()
```

Notes: Be sure to quit ALL other running R and RStudio instances before running "ravemanager::update\_rave()", otherwise packages will be locked and upgrade will fail. For other problems, the fallback is to completely reinstall RAVE.
