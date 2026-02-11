> **Navigation:** [Home](index.md) • [Install](Install.md) • [Help](Help.md)

# VScode

|  |  |
| --- | --- |
| [RAVE logo](../../attachments/VScode/RAVE_Logo_new.jpg "RAVE logo") | **R**eproducible **A**nalysis and **V**isualization of i**E**EG   ***RAVE*** |

# Using RAVE on the SSH with VSCode on remote server

When running RAVE on a remote server such as school HPC, users often encounter the following issues:

* Server does not have or users have to compete for remote desktop resources (e.g. VPN, RDP)
* Server does not expose its IP address (Cannot access to RAVE sessions remotely)

We recommend using vscode in this case.

## Prerequisite

On the server, [install/enable supported SSH server](https://code.visualstudio.com/docs/remote/troubleshooting#_installing-a-supported-ssh-server). For example, on MacOS server, go to system preferences (or system settings after Ventura) > sharing > (turn on) remote login.

On your personal computer, make sure you have proper [SSH client](https://code.visualstudio.com/docs/remote/troubleshooting#_installing-a-supported-ssh-client). On MacOS, you do not need to do anything (SSH-client has been pre-installed).

Get your server IP address. If you are running Mac/Linux, you can login to your server, open a terminal window, type

```
ifconfig | grep inet
```

This command will list all IP addresses used by your server. You should see something like

```
inet 10.100.130.3
```

## Install vscode and SSH add-on on local computer (one-time setup)

1. install [vscode](https://code.visualstudio.com/download), choose proper version and download. For MacOS, download universal application, extract the zip file, and drag the app file into your `/Applications` folder.

2. Open the `Visual Studio Code.app`. If you open the app for the first time, MacOS usually pops up a confirm window asking whether you trust the application. Click on "open". VSCode is developed and released by Microsoft so it's OK to use.

3. On the left of VSCode, click on "Extensions" icon, or use `command+shift+X` on Mac to open the extensions panel.

4. Search for `Remote-SSH` add-on. Make sure this add-on is released by Microsoft, click on install

## Create SSH key (one-time setup)

This section follows [this tutorial](https://code.visualstudio.com/docs/remote/troubleshooting#_quick-start-using-ssh-keys), but is specially tuned for MacOS.

The goal is to generate a security key so you don't need password to access the server. Instead, you will use a security key for SSH.

1. Open a terminal locally on your computer, copy-paste the following command to terminal and hit the "return/enter" key on your keyboard:

```
ssh-keygen -t ed25519
```

2. You will be asked several questions. You can accept the default by hitting "return/enter" key. A SSH key pairs will be generated at your `$HOME/.ssh`: a private key `id_ed25519` and a public key `id_ed25519.pub`. Please do NOT share the `id_ed25519` with anyone. You can do so by running the following terminal command to secure the private key:

```
chmod 400 ~/.ssh/id_ed25519
```

3. Now, register your public key to the server, MAKE SURE you change the "username" to be your login username, and "server\_ip" be your server IP address (see "Prerequisite" for instructions on getting server IP)

```
ssh-copy-id -i ~/.ssh/id_ed25519 username@server_ip
```

You will be prompted to enter the user password. Enter the password (the screen will not display anything during typing, don't worry it's normal).

4. Once you have registered ssh public key to the server, you can test it by running the following command. Again, change username and server\_ip here.

```
ssh username@server_ip
```

If you can remote-login to the server without being asked for password, congratulations!

## Login with your vscode

Open vscode locally, click on the `≷` icon on the bottom-left, a prompt will pop up, select `Connect to a Host...`, and enter your username@server\_ip (please change accordingly!)

Upon successful connection, you will see your server address at the bottom-left.

## Configure R on vscode (server side)

Please make sure you connect vscode to the server first.

1. Open "Extensions" panel, search `R`. Install the R editor support.

2. Use shortcut `command+N` (new file), you can create a blank new file

3. Select the file type as `R` (click on "Select a language"), you can start to type R commands.

4. (first-time setup) If this is the first time that you open R session on the server via vscode, copy-paste the following command into your script

```
ravemanager:::install_packages(c("languageserver", "httpgd", "startup"))
```

Use `command+return/enter` to run the line.

* In case command+return does not run, you can use `` control(⌃)+` `` to open terminal window, type R to start an R instance and run command from there
* languageserver and httpgd are R packages that help you run R commands in vscode remotely
* You only need to run the above command once.

5. (first-time setup) Open a regular bash terminal on server, type

```
echo $path
```

This will print out the system path. For example, you will see outputs like: "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/Library/Apple/usr/bin:...". Copy the output to somewhere. We will use it in the next step.

6. (first-time setup) Open an R terminal on server (you can type "R" in bash terminal, and hit return/enter key), type:

```
startup::install()
```

This will install a start-up folder at "~/.Rprofile.d". All R scripts within that folder automatically run every time when R is launched on the server.

7. (first-time setup) Create a file called "set\_path.R" under ~/.Rprofile.d, copy-paste the following scripts. Please EDIT the path here (using the path object copied from step 5)

```
addon_path <- "<Paste the path output from step 5>"
orig_path <- Sys.getenv("PATH")
paths <- unlist(strsplit(addon_path, ":"), strsplit(orig_path, ":")) 
Sys.setenv(PATH = paste(paths, collapse = ":"))
```

## Start RAVE

Please make sure you connect vscode to the server. If this is the first time, please also finish the previous part "Configure R on vscode (server side)" first.

Use the following command to start RAVE

```
 rave::start_rave2(launch.browser = FALSE, as_job = FALSE, port = 4569)
```

You can choose other ports (if multiple users are running RAVE, they need to have unique ports).

You will be prompted with a dialogue, click on "Open Browsers", you will see RAVE running on 127.0.0.1:4569 (or whatever port you have specified).

## Log-off with your vscode

If you want to log off, click on the `≷` icon again, and choose `Close Remote Connection`. PLEASE MAKE SURE you disconnect every time. Otherwise your opened applications might persist, resulting in security vulnerabilities.

## Credits

Thanks Max Krammer@CMU for showing me this possibility.
