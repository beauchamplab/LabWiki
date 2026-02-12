---
layout: default
title: "AWS"
parent: Beauchamp
---

# AWS

|  |  |
| --- | --- |
|  | Beauchamp Lab wiki |

* [Home](index.md "Beauchamp")
* [Publications](Publications.md "Beauchamp:Publications")
* [Resources](DataSharing.md "Beauchamp:DataSharing")

[![](../../attachments/Beauchamp_RAVE:AWS/RAVE_LogoJan2019.jpg)](../../attachments/Beauchamp_RAVE:AWS/RAVE_LogoJan2019.jpg)

RAVE Logo

## Deploy RAVE on AWS EC2 Server

We are no longer providing a community instance of RAVE on AWS. RAVE 1.0 can be downloaded to your local machine along with demo data.

The following instructions were correct as of late 2019, though, if someone wants to deploy their own AWS instance of RAVE.

### Step 1: Create AWS EC2 Server

* Login to <https://aws.amazon.com> Management Console, searching for service **EC2**

* In EC2 console, click **instances** link on the left navigation sidebar. Then click **launch instances**

* Select **Amazon Linux AMI**. There might be multiple choices, select the first one. Make sure it's a **x86** instance (R doesn't work in ARM CPUs)

* In **Choose Instance Type**, select a proper instance scale (I recommend t2.large for testing purpose) depending on RAM, and click Next.

* In **Configure Instance**, check

```
 [X] Protect against accidental termination
```

* In **Add Storage**, add volume size to at least 16GB

* In **Configure Security Group**, check

```
 [X] Select an existing security group
```

and check

```
 [X] sg-995c66e4   RAVE   RAVE Demo Service
```

On your local machine,
Copy file **rave.pem** from **Box/RAVE/AWS EC2 Key** to your home directory. To find this directory, open Spotlight (command+space) and type "~/".

* When You click **launch** button, a message box will pop out asking to **select a keypair**. Select

```
 rave
```

and launch instance

### Step 2: Connect to EC2 via terminal

* Login to <https://aws.amazon.com> Management Console. Go to **instances**, Right-click on the instance you created. Click **connect**. Copy the line below "Example".

In my case, it's

```
 ssh -i "rave.pem" ec2-user@ec2-34-215-14-112.us-west-2.compute.amazonaws.com
```

* Open terminal on your local machine, paste the line you just copied, hit enter. If this is the first time, it might asks you to store ssh key. Enter "yes"

### Step 3: Install RAVE on EC2

* Install **epel**

```
 sudo yum install epel-release
```

If error occurs, read error message. Usually it will give you solution. For example in my case,

```
 ...
 epel-release is available in Amazon Linux Extra topic "epel"
 To use, run
 # sudo amazon-linux-extras install epel
 ...
```

Then I copied the last line ("sudo amazon-linux-extras install epel", with no "#") and paste that in command line, hit enter.

* Install **R**

```
 sudo yum install R
```

* Install **OpenMPI**

```
 sudo yum install openmpi-devel -y
 MPI_DIR=/usr/lib64/openmpi
```

Check if library is installed

```
 ls /usr/lib64/openmpi
```

If files are printed out, then it means the library is installed, then

```
 export LD_LIBRARY_PATH=/usr/lib64/openmpi/lib:$LD_LIBRARY_PATH
 export PATH=$PATH:/usr/lib64/openmpi/bin
```

* Install **HDF5**

Download and compile

```
 HDF5_VERSION=1.10.4
 HDF5_RELEASE_URL="https://support.hdfgroup.org/ftp/HDF5/releases"
 wget "$HDF5_RELEASE_URL/hdf5-${HDF5_VERSION%.*}/hdf5-$HDF5_VERSION/src/hdf5-$HDF5_VERSION.tar.gz"
 tar -xzf "hdf5-$HDF5_VERSION.tar.gz"
 cd "hdf5-$HDF5_VERSION"
 ./configure --prefix=/usr/local
```

Make install

```
 sudo make install
```

Add HDF5 lib path to environment (Important)

```
 export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
 echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib' >> ~/.bashrc
```

* Install Devtools

```
 sudo yum groupinstall 'Development Tools' -y
 sudo yum install libcurl-devel -y
 sudo yum install openssl-devel -y
 sudo yum install libxml2-devel -y
 sudo yum install fftw-devel -y
 sudo yum install v8-devel -y
```

Enter R,

```
 sudo R
```

Copy:

```
 install.packages('devtools', repos='https://cran.rstudio.com/')
```

Exit R

```
 q(save='no')
```

* Install Github Repos.

Enter R command line:

```
 R
```

Install dependencies

```
 devtools::install_github('dipterix/rutabaga')
 devtools::install_github('dipterix/threeBrain') 
 devtools::install_github('beauchamplab/ravebuiltins')
```

Install dev version of RAVE (optional)

```
 devtools::install_github('beauchamplab/rave@dev-0.1.6.1')
```

Quit R commandline

```
 q(save='no')
```

### Step 4:Install Shiny Server and configure R

* Install Shiny Server

```
 wget https://download3.rstudio.org/centos6.3/x86_64/shiny-server-1.5.9.923-x86_64.rpm
 sudo yum install --nogpgcheck shiny-server-1.5.9.923-x86_64.rpm
```

* Configure shiny server

```
 sudo nano /etc/shiny-server/shiny-server.conf
```

Check the server conf file as follows:

```
 run_as ec2-user;
 server {
   listen 80;...
```

Use **control+X** to quit, press **Y** and hit enter to save

* Create a file to launch RAVE

In terminal,

```
 cd ~
 nano app.R
```

Edit app.R like follows

```
 require(rave)
 tempdir(check = TRUE)
 rave::init_app(port=80)
```

Use **control+X** to quit, press **Y** and hit enter to save

* Move app.R to shiny server and restart

In terminal:

```
 sudo cp app.R /srv/shiny-server/
 sudo rm /srv/shiny-server/index.html
 sudo systemctl restart shiny-server
```

* Test if shiny server starts

```
 Go to AWS console, click your instance, find Public DNS (IPv4), copy to browser as URL, open that web address
```

You should be able to see RAVE running

* Download RAVE demo subject

In your terminal

```
 R
```

In R environment, download a demo subject

```
 rave::download_sample_data()
```

Quit R

```
 q(save='no')
```

* Link your instance to a public IP address

If you have a public IP address, for example, in openwetware RAVE section, I have a RAVE instance link, this link is an IP address. It's important that this IP address linked to correct instance.

Go to AWS instances, keep down your instance ID. For example, in my case is "i-095a9e12dc083544a".

Go to Elastic IPs (from sidebar)

```
 Action > Associate address > Choose your instance ID (select i-095a9e12dc083544a) > [X] Allow Elastic IP to be reassociated if already attached
```


