# Vaccine Booker

A python script to try and give the user the best chance of booking a vaccine on the CoWIN portal, without use of the CoWin APIs (which have become useless :/)

## Installation

### 0. Fork, Clone and Extract:
* Fork the repository, and in a terminal opened in a folder of your choosing, run:
```
	git clone [your_forked_repository_url]
```
* Extract the downloaded folder and navigate to inside the folder.
### 1. Python dependencies:

* Set up a virtual environment. Run ```sudo apt install python3-venv``` if you do not have venv in your system.

```
	python3 -m venv [yourVenv]
```

* Activate your virtual environment.
```
	source [yourVenv]/bin/activate
```
* Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the Python3 requirements for the project, as shown:

```
	pip install -r requirements.txt
```

### 2. Webdriver:

* Included are the chromedrivers for Linux and Windows for Chrome version 90; change as you see fit.

### 3. Setting up a dummy account to receive the OTP:

* Create a dummy gmail account, following which, delete all mails from the inbox.
* Enable Less Secure App access [here](https://myaccount.google.com/intro/security).
* Navigate to your [Google API console](https://console.cloud.google.com/apis/dashboard), and create a new project.
* Under “Credentials”, select “Create credentials” and create a new “OAuth client ID”
* You will be asked which type of app will use this ID, choose “Desktop Application”.
* This will allow you to access your client ID and secret key; Paste these in oauthcredentials.txt; Make sure to have no spaces between the '=' symbol in the file.

### 4. Forwarding your OTP to this email:

* Download any app on your phone that allows message forwarding to an email, and set up a filter to make sure only the OTPs that contain the word 'CoWin' or such are forwarded to this email.

### 5. Refresh Token:

* Run the vaccine python script once, as:
```
	python3 vaccinev4.py [MOBILE] [DUMMY EMAIL]
```
It will prompt you to go to a link; Follow the instructions there and then on your terminal.

### 6. Finish up

* Close everything and restart the script; You can also change the alert sound. Run it as:
```
	python3 vaccinev4.py [MOBILE] [DUMMY EMAIL]
```

## Limitations

* The website recently introduced a captcha to confirm your appointment, which means that the script will take you all the way to that screen and alert by playing a loud sound. The entering of the captcha and pressing confirm is on you. (IF ANYONE KNOWS HOW TO AUTOMATE CAPTCHAS, FEEL FREE TO SEND A PR!)

* The OTP system has become a bit wonky, meaning that sometimes, it will bug out and not send. In that case, a manual reboot can help.

* It works best when the script is allowed to scan the website uninterrupted/unminimised.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.