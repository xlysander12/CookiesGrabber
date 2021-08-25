# CookiesGrabber
Small python tool designed to grab all the cookies from browsers

# Requisites
- Python 3.x
- Windows OS

# How to use
You can use the script with no extra arguments by using `python main.py`. This will create a file `cookies.json` will all cokkies from Google Chrome.\n
If there is a need to change any setting run `python main.py -h` to see available options

# Compatibility
This script is useful when used together with [InstagramDMScraper](https://github.com/xlysander12/InstagramDMScraper) as the cookie `sessionid` from instagram is needed

# Why only Google Chrome?
So far, the script only supports Chrome because it's the only browser (so far) that encrypts the cookies values. This script decrypts everything and outputs it nicely to a json file

# WARNING
This must be ran at the target pc. If ran from another computer with the Cookies file from a different one, it won't work.
