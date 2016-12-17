# ActivityExtractor
This repository gets viewing activity from user's streaming service accounts

Based off of abhishek-vinjamoori's SubtitleExtractor <br>
Link: https://github.com/abhishek-vinjamoori/SubtitleExtractor/blob/master/README.md

## Usage Instructions
#### If credentials are already in `userconfig.ini`
Open a command window in directory containing `ActivityExtractor.py`
Run this command:
```
python activityextractor.py --service=[service]
```
`[service]`: Put your streaming service here

#### If credentials are NOT already in `userconfig.ini`
Open a command window in directory containing `ActivityExtractor.py`
Run this command:
```
python activityextractor.py --service=[service] --email=[email] --password=[password]
```
`[service]` : Put your streaming service here <br>
`[email]`   : Put your email address for the streaming service here <br>
`[password]`: Put your password here <br>

## Setup Instructions
### Install python3

If python3 is not installed:
```
$ sudo apt-get install python3
```
### pip install requests
If pip3 is not installed:
```
$ sudo apt-get install python3-setuptools
$ sudo easy_install3 pip
$ sudo mv /usr/local/bin/pip /usr/local/bin/pip-3
```
### Install Selenium
```
$ sudo pip3 install -U selenium
```
### Install chromedriver

Make sure you already have Google Chrome installed. <br>
Then download and extract the contents of - http://chromedriver.storage.googleapis.com/index.html?path=2.25/ <br>
You will get a file named 'chromedriver' <br>
Navigate to the directory where 'chromedriver' is located and execute the following command <br>
to move chromedriver into /user/local/bin <br>
```
$ sudo mv -t /usr/local/bin/ chromedriver
```
