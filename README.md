# Perseverance, a Vaccine Booker
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/LaRuim/Vaccine-Booker/graphs/commit-activity)

A python script to try and give the user the best chance of booking a vaccine on the CoWIN portal, without use of the CoWin APIs (which have become useless :/)

## Installation

### 0. Fork, Clone and Extract:
* Fork the repository, and in a terminal opened in a folder of your choosing, run:
```
	git clone [your_forked_repository_url]
```
* Extract the downloaded folder and navigate to inside the folder.

* If you are unfamiliar with the above process, you can also just click on the green button that says 'Code', and download it as a zip file; Extract this zip file in a convenient location.

* Make sure to have Python and pip installed. You can do so [here](https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe). Make sure to check the 'Install pip' checkbox when installing Python.

### 1. Python dependencies:

* Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the Python3 requirements for the project, by opening up a terminal in the folder of the project, and typing:

```
	pip install -r requirements.txt
```

### 2. Webdriver:

* This program is designed to run on Google Chrome; I might add other browser support later on. As a pre-requisite, you need to download the Chromedriver [here](https://chromedriver.chromium.org/downloads). Download the one the corresponds to your Chrome version, and Operating System version. To find your Chrome version, click [here](https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have). Download the Chromedriver and place it in the same folder as the main scripts.

### 3. Setting up a dummy account to receive the OTP:

* Create a dummy gmail account, following which, delete all mails from the inbox. Make sure to be logged into this email.
* Enable Less Secure App access [here](https://myaccount.google.com/lesssecureapps).
* Navigate to your [Google API console](https://console.cloud.google.com/apis/dashboard), and create a new project.
* Under “Credentials”, select “Create credentials” and create a new “OAuth client ID”
* You will be asked which type of app will use this ID, choose “Desktop Application”.
* This will allow you to access your client ID and secret key; Paste these in [oauthcredentials.txt](resources/oauthcredentials.txt), located in the folder resources; Make sure to have no spaces before or after the '=' symbol in the file.
* Make sure to publish your Project by changing the **Publishing Status** of the project to 'In production', in the **OAuth consent screen** section. This is VERY important, and without doing this, the OTP system cannot work.

### 4. Forwarding your OTP to this email:

* Download any app on your phone that allows message forwarding to an email, and set up a filter to make sure only the OTPs that contain the word 'CoWin' or such are forwarded to this email. [This](https://play.google.com/store/apps/details?id=com.gawk.smsforwarder&hl=en_IN&gl=US) is the app I use on my Android phone; feel free to use the same one. Make sure to enable OTP forwarding, and **ONLY add YOUR dummy account in the email list.** 

### 5. Refresh Token:

* Run the vaccine python script once, as:
```
	python3 book.py [MOBILE] [DUMMY EMAIL] [NUMBER OF BENEFICIARIES IN MOBILE]
```
It will prompt you to go to a link; After okay-ing the warnings that pop up, copy the code that pops up and paste it in the terminal and press enter. You will now see another bunch of gibberish. This is your **REFRESH TOKEN**. Paste this in [oauthcredentials.txt](resources/oauthcredentials.txt). Now close the Chrome windows that opened up, as well as the terminal itself, and wait for about 5 minutes.

### 6. Finish up

* Enter the pincodes you want to scan through in [pincodes.txt](resources/pincodes.txt), one in each line, in the folder resources.
* Close everything and restart the script; You can also change the alert sound by replacing the provided [alert.mp3](resources/alert.mp3) with your own mp3 file and renaming it as 'alert.mp3'.

## Execution

Open up a terminal in the folder containing [book.py](book.py). Type the below command(s):
```
	python3 book.py [MOBILE] [DUMMY EMAIL] [NUMBER OF BENEFICIARIES IN MOBILE] [optional BENEFICIARY NUMBER]
```
or, if you prefer particular centres, enter their keywords in [centre_keywords.txt](resources/centre_keywords.txt) in the folder resources, and run as:
```
	python3 book.py [MOBILE] [DUMMY EMAIL] [NUMBER OF BENEFICIARIES IN MOBILE] [optional BENEFICIARY NUMBER] -s
```
If the script doesn't seem to be working, it's possible that your internet is a tad too slow for the script. If that's the case, run as:
```
	python3 book.py [MOBILE] [DUMMY EMAIL] [NUMBER OF BENEFICIARIES IN MOBILE] [optional BENEFICIARY NUMBER] [optional -s] --slow
```

Example values for both the above are aleady in the text files.

## Limitations

* The website recently introduced a captcha to confirm your appointment, which means that the script will take you all the way to that screen and alert by playing a loud sound. The entering of the captcha and pressing confirm is on you. (IF ANYONE KNOWS HOW TO AUTOMATE CAPTCHAS, FEEL FREE TO SEND A PR!)

* The OTP system has become a bit wonky, meaning that sometimes, it will bug out and not send. In that case, a manual reboot can help.

* It works best when the script is allowed to scan the website uninterrupted. 

* You MUST NOT minimise the window. If you need to do other tasks while it runs, press ALT+TAB instead. Be warned though, you might miss out on the vaccine by the time you ALT+TAB back to the browser.

* It is viable only for a small number of pincodes; As far as I can make out, a good amount is 3-4, and it should probably still give you results at 5-6.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.