---
layout: default
title: RAID Email Alert Setup Guide (macOS)
date_created: 2026-07-09
parent: Lab Information
grand_parent: Beauchamp
---
# RAID Email Alert Setup Guide (macOS)
 
**What this guide does:** Sets up your Mac so it automatically checks your Promise VTrak RAID units and emails you if a hard drive fails or the array becomes degraded.
 
**How it works (plain English):** Your Mac asks each RAID "are you healthy?" on a schedule. If the answer shows a problem, your Mac sends you an email. The email is sent through Gmail, using a small mail program on your Mac called Postfix.
 
```
Your Mac  --asks-->  RAID          (checks drive health via SNMP)
Your Mac  --emails you if there's a problem-->  Gmail  -->  Your inbox
```
 
**Who this is for:** Anyone. You do not need programming experience. You will copy and paste commands into an app called Terminal. Every command is provided exactly.

At the end, you should have 

1. A scheduled task that runs every weekday to check your RAID status
2. A zsh script that allows you to manually check the status via terminal command:

```
   raid_monitor --host username@server-address -i 11.0.0.1 -n RAID-1 -i 10.0.0.1 -n RAID-2
```
 
**Setup time required:** About 45–60 minutes.
 
---
 
## Before You Begin — What You Need
 
Collect these items first. You will need all of them:
 
1. **A Mac** that stays powered on (this is the machine that will do the checking). It must be able to reach the RAID over the network.
2. **The IP address of each RAID.** Example: `192.0.0.1` and `168.0.0.1`. (You can find these in the RAID's web management page or from whoever set them up.)
3. **A Gmail account** you will send alerts *through*. It is fine to use a normal personal Gmail account. Consider making a dedicated one just for alerts.
4. **The destination email address** where you want to *receive* alerts (can be the same Gmail, or any email you check).
5. **Administrator access** on the Mac (you will need to type your Mac login password when asked).
---
 
## Part 0 — Opening Terminal (the command app)
 
You will type commands into an app called **Terminal**.
 
1. Press `Command (⌘) + Space` to open Spotlight search.
2. Type `Terminal` and press `Return`.
3. A window with text and a blinking cursor appears. This is where you paste commands.
**How to run a command:** Click the Terminal window, paste the command (`Command + V`), and press `Return`.
 
**About passwords:** When a command starts with `sudo`, Terminal will ask for your Mac password. As you type it, **nothing appears on screen** — no dots, no stars. This is normal. Type it and press `Return`.
 
---
 
## Part 1 — Get a Gmail "App Password"
 
Gmail will not let a program log in with your normal password. You must create a special 16-character **App Password**. This requires 2-Step Verification to be turned on first.
 
### Step 1.1 — Turn on 2-Step Verification
 
1. In a web browser, go to **myaccount.google.com**
2. Sign in with the Gmail account you'll send alerts through.
3. Click **Security** on the left.
4. Find **2-Step Verification** and turn it **On**. Follow the prompts (it will ask for your phone number).
### Step 1.2 — Create the App Password
 
1. Go directly to **myaccount.google.com/apppasswords**
   (If it says the page isn't available, wait a few minutes after enabling 2-Step Verification, then try again.)
2. Give it a name like `RAID Monitor` and click **Create**.
3. Google shows a **16-character password** in four groups (like `abcd efgh ijkl mnop`).
4. **Write it down now** — you cannot see it again after closing. Ignore the spaces; the real password is the 16 characters with no spaces (`abcdefghijklmnop`).
Keep this password handy for Part 2.
 
---
 
## Part 2 — Set Up Postfix (the mail sender) on Your Personal Mac


>Please set this up on the machine from which you would like to set up the job/work to check. This can be the different machine than your host. For example, you could have your own personal computer to monitor the status and send out emails. In such case, you should configure `postfix` on your own mac.

 Postfix comes built into macOS. You will configure it to send mail through Gmail.
### Step 2.1 — Create the password file
 
This file tells Postfix your Gmail login. Paste this command and press Return:
 
```
sudo nano /etc/postfix/sasl_passwd
```
 
A simple text editor opens inside Terminal. Type **one line**, replacing the example with your details:
 
```
[smtp.gmail.com]:587 youremail@gmail.com:your16charpassword
```
 
- Replace `youremail@gmail.com` with your Gmail address.
- Replace `your16charpassword` with the App Password from Part 1, **no spaces**.
- Keep the `[smtp.gmail.com]:587` part exactly as shown.
To save: press `Control + O` (letter `o`, not number `0`), then `Return`, then `Control + X` to exit.
 
### Step 2.2 — Lock and process the password file
 
These two commands protect the file and prepare it for Postfix. Run them one at a time:
 
```
sudo chmod 600 /etc/postfix/sasl_passwd
```
 
```
sudo postmap /etc/postfix/sasl_passwd
```
 
### Step 2.3 — Configure Postfix settings
 
Run these commands. Each one adds a setting. (These use `postconf`, which safely updates settings without creating duplicates.)
 
```
sudo postconf -e 'relayhost = [smtp.gmail.com]:587'
```

Then, copy-paste the following command to terminal app

```
sudo postconf -e 'smtp_sasl_auth_enable = yes'
sudo postconf -e 'smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd'
sudo postconf -e 'smtp_sasl_security_options = noanonymous'
sudo postconf -e 'smtp_sasl_mechanism_filter = plain, login'
sudo postconf -e 'smtp_tls_security_level = encrypt'
sudo postconf -e 'smtp_tls_CAfile = /etc/ssl/cert.pem'
sudo postconf -e 'inet_protocols = ipv4'
```
 
**What these do, briefly:** they tell Postfix to send all mail through Gmail (`relayhost`), to log in with your App Password (the `sasl` lines), and to use encryption so your password is protected in transit (the `tls` lines).
 
### Step 2.4 — Start Postfix
 
```
sudo postfix start
```
 
If it says Postfix is already running, use this instead:
 
```
sudo postfix reload
```
 
### Step 2.5 — Send a test email
 
Replace `you@example.com` with the address where you want to receive alerts, then run:
 
```
echo "This is a test from my Mac." | mail -s "RAID Monitor Test" you@example.com
```
 
Wait a minute, then check that inbox. **If the email arrives, Postfix is working.**
 
> **First-time Gmail note:** The very first time your Mac sends through Gmail, Gmail may block it as a security precaution. Open the Gmail account in a browser and look for a "Critical security alert" or "Someone tried to sign in" message. Click **Yes, it was me**, then send the test again.
 
### If the test email does NOT arrive
 
Run this to see what went wrong:
 
```
tail -20 /var/log/mail.log 2>/dev/null || log show --predicate 'process == "smtp"' --last 5m
```
 
Common causes:
- **"authentication failed"** — the App Password in Step 2.1 is wrong or has spaces. Redo Steps 2.1 and 2.2.
- **Nothing sent / blocked** — do the Gmail security-alert step above.
- Check the waiting mail with: `mailq`
---
 
## Part 3 — Set Up the RAID Health Check

>This part needs to be configured on the server where RAID is attached to. 

Our personal Mac cannot reach the RAIDs directly — only the server can, and the server is where the actual health queries run. In this part you set up an automatic (passwordless) SSH login from your Mac to the server, then use that login to install the SNMP tool on the server.
 
### Step 3.1 — Set Up Passwordless SSH from Your Mac to the Server
 
The scheduled check must run without anyone typing a password, so your Mac needs a **key-based** login to the server.
 
**3.1a — Create an SSH key** (skip if you already have one). Run:
 
```
ls ~/.ssh/id_ed25519.pub
```
 
- If it shows the file, you already have a key — skip to 3.1b.
- If it says "No such file," create one:

```
# Do NOT run if file exists
ssh-keygen -t ed25519 -C "raid-monitor"
```
 
  Press `Return` to accept the default location. When asked for a passphrase, **press Return twice to leave it empty** — an empty passphrase is required so the scheduled job can log in on its own.
 
**3.1b — Copy your key to the server.** Replace `username@server-address` with your server's SSH login:
 
```
ssh-copy-id username@server-address
```
 
It will ask for your server password **this one time**. After this, logins won't need a password.
 
> If `ssh-copy-id` isn't available on your Mac, use this instead (same replacement):
> ```
> cat ~/.ssh/id_ed25519.pub | ssh username@server-address 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
> ```
 
**3.1c — Confirm passwordless login works.** Run (with your server login):
 
```
ssh username@server-address 'echo Connected without a password'
```
 
If it prints `Connected without a password` **without asking for a password**, SSH is set up correctly. If it still asks for a password, repeat 3.1b.
 
### Step 3.2 — Install the SNMP Tool on the Server
 
The server (not your Mac) runs the actual queries, so the SNMP tool must live there. Now that passwordless SSH works, you can log into the server and install it.
 
**3.2a — Log into the server:**
 
```
ssh username@server-address
```
 
Your Terminal is now "inside" the server. The following commands run **on the server** until you log back out.
 
**3.2b — Install the SNMP tools**, choosing the line that matches the server's operating system:
 
- **macOS server** (uses Homebrew):
```
  brew install net-snmp
```
  (If it says `brew not found`, install Homebrew first from **brew.sh**, then run the line above.)
 
- **Linux server, Debian/Ubuntu:**
```
  sudo apt install snmp
```
 
- **Linux server, RedHat/CentOS:**
```
  sudo yum install net-snmp-utils
```
 
**3.2c — Confirm the tool installed:**
 
```
snmpwalk --version
```
 
If it prints a version number, the tool is ready.
 
**3.2d — Log back out of the server** (returns you to your own Mac):
 
```
exit
```
 
You are now back on your personal Mac. The rest of the guide runs from here.
 
---
 
## Part 4 — Set Up and Test RAID Monitoring
 
Now turn on SNMP on the RAIDs, confirm the whole chain works, and install the monitoring script.
 
### Step 4.1 — Turn On SNMP on Each RAID
 
"SNMP" is the language used to ask the RAID about its health. Enable it on each RAID in the **RAID's web management page** — no Terminal needed.
 
1. Open the RAID's web management page in a browser (using its IP address).
2. Find the **SNMP** settings (often under Administration, Services, or Network).
3. **Enable** the SNMP service/agent.
4. Note the **community string** — this is like a password for reading status. It is often `public` by default. Write it down.
5. Save. **Repeat for each RAID.**
### Step 4.2 — Test the Whole Connection
 
This single test confirms all three links at once: your Mac reaches the server, the server has the SNMP tool, and the server can reach the RAID. Replace the server login, and use one of your RAID IPs and your community string:
 
```
ssh username@server-address 'snmpwalk -v2c -c public 11.0.0.1 SNMPv2-MIB::sysDescr.0'
```
 
- If it prints a line mentioning **"Promise"**, everything is connected — continue to Step 4.3.
- If it says **"snmpwalk: command not found"**, the tool didn't install on the server. Redo Step 3.2.
- If it **times out**, SNMP may not be enabled on that RAID (Step 4.1), or the IP/community string is wrong.
### Step 4.3 — Create the Monitor Script
 
Install the script on your **personal Mac**. Run:
 
```
sudo nano /usr/local/bin/raid_monitor
```
 
The editor opens. Carefully paste the **entire** block below into it:
 
```zsh
#!/bin/zsh
# raid_snmp_monitor.sh — VTrak E5800f health check (zsh)
# Usage:
#   raid_snmp_monitor.sh [--host <user@host>] -i <ip> -n <name> [-i <ip> -n <name> ...] [-e <email> ...]
# Example:
#   raid_snmp_monitor.sh -i 11.0.0.1 -n RAID-1 -i 10.0.0.1 -n RAID-2 -e me@example.com
#
# Each -i must be followed by a matching -n (paired in order).
#
# --host <user@host>: run every snmpwalk on that host over SSH (the RAID IPs are
#   reachable only from there). Defaults to $RAIDHOST from the environment; pass an
#   empty value (--host '') to run snmpwalk locally instead. NOTE: SNMP queries run
#   on the SSH host, but alert mail is sent from whichever machine runs THIS script.
#
# Reports physical drives, disk arrays, enclosures, controllers, and batteries
#   (with health: remaining capacity % and temperature). Problem rows are flagged
#   with a leading "!!" (critical) or "! " (warning). If one or more -e is given, a
#   full status report email is sent (via local sendmail/Postfix). With no -e, the
#   script just prints the report.

COMMUNITY="public"

# Host to run snmpwalk on (over SSH). Defaults to $RAIDHOST from the environment.
# Override with --host; set it empty (--host '') to run snmpwalk locally.
SSH_HOST="${RAIDHOST:-}"

PD_STATUS_OID=".1.3.6.1.4.1.7933.1.20.2.1.1.8"       # physical drive: raidv4PhydrvOperationalStatus
ARRAY_STATUS_OID=".1.3.6.1.4.1.7933.1.20.2.4.1.3"    # disk array:     raidv4DiskArrayStatus
ENCL_STATUS_OID=".1.3.6.1.4.1.7933.1.20.1.10.1.3"    # enclosure:      raidv4EnclosureStatus
CTRL_STATUS_OID=".1.3.6.1.4.1.7933.1.20.1.3.1.15"    # controller:     raidv4CtrlOpStatus
BATT_STATUS_OID=".1.3.6.1.4.1.7933.1.20.1.15.1.14"   # battery:        raidv4BatteryStatus
BATT_CAP_OID=".1.3.6.1.4.1.7933.1.20.1.15.1.11"      # battery health: raidv4BatteryRemainCapacity (%)
BATT_TEMP_OID=".1.3.6.1.4.1.7933.1.20.1.15.1.7"      # battery health: raidv4BatteryTemperature (C)

SENDMAIL="${SENDMAIL:-/usr/sbin/sendmail}"
MAIL_FROM="raid-monitor@localhost"


# --- Parse arguments ---
typeset -a ips names emails
while [[ $# -gt 0 ]]; do
    case $1 in
        -i) shift; ips+="$1" ;;
        -n) shift; names+="$1" ;;
        -e) shift; emails+="$1" ;;
        -H|--host) shift; SSH_HOST="$1" ;;
        -h|--help)
            print -r -- "Usage: $0 [--host <user@host>] -i <ip> -n <name> [-i <ip> -n <name> ...] [-e <email> ...]"
            exit 0 ;;
        *)
            print -r -- "Unknown argument: $1" >&2
            exit 2 ;;
    esac
    shift
done

if [[ ${#ips} -eq 0 || ${#ips} -ne ${#names} ]]; then
    print -r -- "Error: each -i <ip> must be paired with an -n <name>." >&2
    print -r -- "Usage: $0 [--host <user@host>] -i <ip> -n <name> [-i <ip> -n <name> ...] [-e <email> ...]" >&2
    exit 2
fi

# run_snmpwalk <ip> <oid>
# Runs snmpwalk on $SSH_HOST via SSH, or locally when SSH_HOST is empty.
run_snmpwalk () {
    local ip="$1" oid="$2"
    if [[ -n $SSH_HOST ]]; then
        ssh -o BatchMode=yes -o ConnectTimeout=10 "$SSH_HOST" \
            snmpwalk -v2c -c "$COMMUNITY" -Oqv "$ip" "$oid" 2>&1
    else
        snmpwalk -v2c -c "$COMMUNITY" -Oqv "$ip" "$oid" 2>&1
    fi
}

# add_row <label> <status> [suffix]
# Appends one report row to RB, prefixed with a 2-char problem marker so columns
# stay aligned. Display-only: the raw status text is never altered. Unrecognized
# values are treated as normal ("  ").
add_row () {
    local label="$1" val="$2" suffix="${3:-}"
    local marker s="${val:l}"
    case $s in
        *dead*|*fail*|*malfunc*|*critical*|*offline*|*missing*|*fault*|*error*|*absent*|*timeout*|*"no response"*|*"not present"*|*unplug*|*stale*)
            marker="!!" ;;   # critical — failure
        *degrad*|*rebuild*|*recondition*|*charging*|*pfa*|*transition*|*initializ*|*synchron*|*migrat*|*expand*|*background*|*"not ready"*|*learning*)
            marker="! " ;;   # warning  — attention
        *)
            marker="  " ;;   # ok / unrecognized — normal
    esac
    RB+="${marker}${label}${val}${suffix}"$'\n'
}

# add_section <title> <label-prefix> <ip> <oid>
# Walks one status column and appends "Title:" plus one row per value to RB.
add_section () {
    local title="$1" prefix="$2" ip="$3" oid="$4"
    local -a vals
    vals=("${(@f)$(run_snmpwalk "$ip" "$oid")}")
    RB+="${title}:"$'\n'
    if [[ ${#vals} -eq 0 ]]; then
        RB+="  (no data returned)"$'\n'
        return
    fi
    local n=0 v
    for v in $vals; do
        n=$((n+1))
        add_row "${prefix}${n}: " "${v//\"/}"
    done
}

# check_raid <ip> <label>
# Builds a full status report into the global REPORT and prints it. Problem rows
# are prefixed "!!" (critical) or "! " (warning); the raw status text is never
# altered. Returns 1 only if the SSH host was unreachable.
check_raid () {
    local ip="$1"
    local label="$2"

    RB=""            # report body accumulator (filled by add_row/add_section)

    local header="=================================================="$'\n'
    header+="  $label ($ip)   $(date)"$'\n'
    header+="=================================================="
    print -r -- "$header"

    # If snmpwalk is routed through SSH and that host is down, say so and stop.
    if [[ -n $SSH_HOST && -n $SSH_ERROR ]]; then
        local msg1="!! SSH to ${SSH_HOST} FAILED — could not query ${label} (${ip})."
        local msg2="   Reason: ${SSH_ERROR}"
        print -r -- "$msg1"
        print -r -- "$msg2"
        print ""
        REPORT="$header"$'\n'"$msg1"$'\n'"$msg2"$'\n'
        return 1
    fi

    add_section 'Physical drives' 'PD'         "$ip" "$PD_STATUS_OID"
    add_section 'Disk arrays'     'Array'      "$ip" "$ARRAY_STATUS_OID"
    add_section 'Enclosures'      'Enclosure'  "$ip" "$ENCL_STATUS_OID"
    add_section 'Controllers'     'Controller' "$ip" "$CTRL_STATUS_OID"

    # --- Batteries: raw status plus health (remaining capacity %, temperature C) ---
    local -a bstat bcap btemp
    bstat=("${(@f)$(run_snmpwalk "$ip" "$BATT_STATUS_OID")}")
    bcap=("${(@f)$(run_snmpwalk "$ip" "$BATT_CAP_OID")}")
    btemp=("${(@f)$(run_snmpwalk "$ip" "$BATT_TEMP_OID")}")
    RB+="Batteries:"$'\n'
    if [[ ${#bstat} -eq 0 ]]; then
        RB+="  (no data returned)"$'\n'
    else
        local bi
        for (( bi = 1; bi <= ${#bstat}; bi++ )); do
            add_row "Battery${bi}: " "${bstat[bi]//\"/}" \
                " (remaining capacity: ${bcap[bi]//\"/}%, temperature: ${btemp[bi]//\"/} C)"
        done
    fi

    print -rn -- "$RB"
    print ""

    REPORT="$header"$'\n'"$RB"
    return 0
}

send_alert () {
    # $1 = subject, $2 = body
    local subject="$1" body="$2" addr
    for addr in $emails; do
        {
            print -r -- "From: $MAIL_FROM"
            print -r -- "To: $addr"
            print -r -- "Subject: $subject"
            print -r -- "MIME-Version: 1.0"
            print -r -- "Content-Type: text/plain; charset=UTF-8"
            print -r -- "Content-Transfer-Encoding: 8bit"
            print ""
            print -r -- "$body"
        } | $SENDMAIL -t
    done
}

# --- Preflight: if routing through SSH, probe the host once so we can report a
#     clear reason (e.g. host down/timeout) instead of many snmpwalk timeouts. ---
SSH_ERROR=""
if [[ -n $SSH_HOST ]]; then
    ssh_probe=$(ssh -o BatchMode=yes -o ConnectTimeout=10 "$SSH_HOST" true 2>&1)
    ssh_rc=$?
    if (( ssh_rc != 0 )); then
        SSH_ERROR="${ssh_probe:-SSH connection failed (exit ${ssh_rc})}"
    fi
fi

# --- Main loop ---
# NOTE: requirement 4 is on hold — for now always send the full status report
# (including OK) when -e is given. Filtering by problem state comes later.
# All RAIDs are combined into a SINGLE email (not one per RAID).
typeset -i i
ALL_REPORT=""
for (( i = 1; i <= ${#ips}; i++ )); do
    REPORT=""
    check_raid "${ips[i]}" "${names[i]}"
    if [[ -n $ALL_REPORT ]]; then
        ALL_REPORT+=$'\n'
    fi
    ALL_REPORT+="$REPORT"
done

if [[ ${#emails} -gt 0 ]]; then
    send_alert "RAID STATUS: ${(j:, :)names}" "$ALL_REPORT"
fi

```
 
Save it: `Control + O`, then `Return`, then `Control + X`.
 
**If your community string is not `public`,** change the line near the top that says `COMMUNITY="public"` to your actual string before saving.
 
Then make the script runnable:
 
```
sudo chmod +x /usr/local/bin/raid_monitor
```
 
### Step 4.4 — Test the Script
 
Run it by hand, filling in your server login (after `--host`), your RAID IPs and names, and your email:
 
```
raid_monitor --host username@server-address -i 11.0.0.1 -n RAID-1 -i 10.0.0.1 -n RAID-2 -e you@example.com
```
 
What happens:
- The script connects to the server, queries each RAID, and prints a full status report for each (physical drives, arrays, enclosures, controllers, batteries).
- Because you included `-e`, it also **emails you the full report**. Check your inbox to confirm mail delivery works end to end.
**To see the report without sending email,** leave off the `-e` part:
 
```
raid_monitor --host username@server-address -i 11.0.0.1 -n RAID-1
```
 
If a drive has failed, you'll see it listed (for example `PD9: Dead`) and the array shown as `Degraded`. A healthy system lists every drive as `OK`.
 
> **Note on what gets emailed:** This version sends the **full status report every time** it runs (not only when there's a problem). So a scheduled run will email you a report on each run. If you would prefer to be emailed *only when something is wrong*, that's a change to the script — ask whoever maintains this setup.
 
---
 
## Part 5 — Make It Run Automatically (Scheduled)
 
You'll now schedule the check to run on its own. macOS uses a system called **launchd** for this.
 
### Step 5.1 — Create the schedule file
 
```
nano ~/Library/LaunchAgents/com.user.raidmonitor.plist
```
 
Paste this entire block. **Then edit** the server login, RAID IPs, names, and email to match yours (look for the `<string>` lines in the ProgramArguments section):
 
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.raidmonitor</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/zsh</string>
        <string>/usr/local/bin/raid_monitor</string>
        <string>--host</string>
        <string>username@host_ip</string>
        <string>-i</string>
        <string>11.0.0.1</string>
        <string>-n</string>
        <string>RAID-main</string>
        <string>-i</string>
        <string>10.0.0.1</string>
        <string>-n</string>
        <string>RAID-backup</string>
        <string>-e</string>
        <string>your@email.com</string>
    </array>
    
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Weekday</key><integer>1</integer>
            <key>Hour</key><integer>8</integer>
            <key>Minute</key><integer>0</integer>
        </dict>
        <dict>
            <key>Weekday</key><integer>2</integer>
            <key>Hour</key><integer>8</integer>
            <key>Minute</key><integer>0</integer>
        </dict>
        <dict>
            <key>Weekday</key><integer>3</integer>
            <key>Hour</key><integer>8</integer>
            <key>Minute</key><integer>0</integer>
        </dict>
        <dict>
            <key>Weekday</key><integer>4</integer>
            <key>Hour</key><integer>8</integer>
            <key>Minute</key><integer>0</integer>
        </dict>
        <dict>
            <key>Weekday</key><integer>5</integer>
            <key>Hour</key><integer>8</integer>
            <key>Minute</key><integer>0</integer>
        </dict>
    </array>
    
    <key>StandardOutPath</key>
    <string>/tmp/raidmonitor.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/raidmonitor.err</string>
</dict> 
</plist>


```
 
This example runs the check **every weekday at 8:00 AM**. To change the time, edit the `Hour` (0–23) and `Minute` (0–59) numbers. Each flag and value must stay on its own `<string>` line.
 
Save: `Control + O`, `Return`, `Control + X`.
 
### Step 5.2 — Turn on the schedule
 
```
launchctl load ~/Library/LaunchAgents/com.user.raidmonitor.plist
```
 
The check now runs automatically on schedule. You only do this once; it keeps working after restarts.
 
### Step 5.3 — Test the schedule immediately
 
Don't wait until the scheduled time to know it works. Force a run now:
 
```
launchctl start com.user.raidmonitor
```
 
Then view the result:
 
```
cat /tmp/raidmonitor.log
```
 
You should see the same report you saw in Step 4.4, and an email should arrive.
 
---
 
## Everyday Use — Quick Reference
 
**See the last scheduled check's result:**
```
cat /tmp/raidmonitor.log
```
 
**Run a check right now, by hand:**
```
raid_monitor --host username@server-address -i 11.0.0.1 -n RAID-1 -i 10.0.0.1 -n RAID-2 -e you@example.com
```
 
**Change the schedule or settings:** Edit the schedule file, then reload it:
```
nano ~/Library/LaunchAgents/com.user.raidmonitor.plist
launchctl unload ~/Library/LaunchAgents/com.user.raidmonitor.plist
launchctl load ~/Library/LaunchAgents/com.user.raidmonitor.plist
```
(You must always `unload` then `load` after editing for changes to take effect.)
 
**Turn off automatic checking:**
```
launchctl unload ~/Library/LaunchAgents/com.user.raidmonitor.plist
```
 
**Confirm the schedule is active:**
```
launchctl list | grep raidmonitor
```
 
---
 
## Important Things to Know
 
**Your personal Mac must be on and awake at the scheduled time.** The check only runs if your Mac is powered on then. If it's asleep, the check runs on wake. If it's fully off at the scheduled time, that run is skipped. For reliable monitoring, schedule a time your Mac is usually on, or use an always-on Mac.
 
**The server must also be reachable.** Since the queries run on the server over SSH, the server must be up and your SSH key still valid. If the server is unreachable, the script emails you a clear "SSH FAILED" report instead of silently doing nothing — so a failed connection is itself visible.
 
**This version emails a full report every run.** No "silent unless broken" behavior yet — each scheduled run sends the current status. If you want problem-only alerts, that's a script change.
 
**Gmail sending limit.** A normal Gmail account can send about 500 emails per day — never a concern for periodic reports.
 
---
 
## Troubleshooting
 
**"snmpwalk: command not found"** — The SNMP tool isn't on the **server** (that's where it runs). Log into the server and install it (Step 3.2).
 
**The script asks for a password when it runs** — Passwordless SSH isn't fully set up. Redo Step 3.1b, and confirm with 3.1c. The scheduled job cannot type a password, so this must work silently.
 
**Report shows "SSH ... FAILED"** — Your Mac couldn't reach the server. Check the server is on and that `ssh username@server-address` works by hand.
 
**Report shows "(no data returned)" for a RAID** — The server was reached, but the RAID didn't answer. SNMP may not be enabled on that RAID (Step 4.1), or the IP/community string is wrong. Confirm with the test in Step 4.2.
 
**No email arrives** — Test the mail system by itself (Part 2, Step 2.5). If that test email doesn't arrive either, the issue is the Postfix/Gmail setup on your Mac, not the RAID check. Re-check the App Password (Part 1) and the Gmail security alert.
 
**"authentication failed" in the mail log** — The Gmail App Password is wrong or has spaces. Redo Steps 2.1 and 2.2.
 
---
 
## Summary of What You Built
 
1. **Postfix** on your personal Mac sends email through your Gmail account.
2. **Passwordless SSH** lets your Mac reach the server automatically, and the server has the SNMP tool installed.
3. A **monitoring script** on your Mac tells the server to query each RAID's drives, arrays, enclosures, controllers, and batteries, then emails you the report.
4. A **daily schedule** runs the whole thing automatically.
Your RAIDs are now watched without you having to remember to check them.


