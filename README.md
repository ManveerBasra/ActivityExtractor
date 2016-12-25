# ActivityExtractor
This repository gets viewing activity from user's streaming service accounts. <br>
Developed during GCI 2016

Based off of abhishek-vinjamoori's SubtitleExtractor <br>
Link: https://github.com/abhishek-vinjamoori/SubtitleExtractor/blob/master/README.md

## Setup Instructions
### Install python3

If python3 is not installed <br>
Run this in a command window:
```
sudo apt-get install python3
```
### Install pip
If pip3 is not installed <br>
Run this in a command window:
```
sudo apt-get install python3-setuptools
sudo easy_install3 pip
sudo mv /usr/local/bin/pip /usr/local/bin/pip-3
```
### Install Selenium
Run this in a command window:
```
sudo pip3 install -U selenium
```
### Install PhantomJS
Make sure you have NodeJS installed (https://nodejs.org/)<br>
Using Node's package manager run this in a command window:
```
npm -g install phantomjs-prebuilt
```

## Usage Instructions
#### If credentials are already in `userconfig.ini`
Open a command window in directory containing `ActivityExtractor.py`
Run this command:
```
python activityextractor.py [service]
```
`[service]` : Put your streaming service here <br>

#### If credentials are NOT already in `userconfig.ini`
Open a command window in directory containing `ActivityExtractor.py`
Run this command:
```
python activityextractor.py [service] --email=[email] --password=[password]
```
`[service]` : Put your streaming service here <br>
`[email]`   : Put your email address for the streaming service here <br>
`[password]`: Put your password here <br>

If you're getting activity from Netflix, you must include an additional parameter:
```
--user=[user]
```
`[user]`    : Put your Netflix username here
