GeoIP-Arduino:
  A little Project that displays the Geo-Location of the last opened website
  on a 16x2 LCD

Pre-Setup:
  * Open "Terminal"
  * from Website-"brew.sh" copy command into Terminal follow instructions
    * ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
    * install xcode ( done by brew )
  * Now execute following commands in "Terminal"
  * echo export PATH='/usr/local/bin:$PATH' >> ~/.bash_profile
  * brew install git
  * brew install python
  * brew link --overwrite python
  * mkdir ~/projects (make directory)
  * cd projects (change directory)
  * git clone https://github.com/kairichard/geoip-arduino.git

Setup:
  * plugin arduino via usb
  * upload code found in `arduino/display/geoip`
  * cd ~/projects/geoip-arduino/server
  * run `pip install -r requirements.txt`
  * then run `python app.py`
    * chose the correct usb device - likely to be tty.usbmodem411 (#1) 
  * you should see 'Initializing' on the display
  * install the chrome extension ( enable developermode -> load unpacked extension from ~/projects/geoip-arduino/crx)
  * you should see 'chrome connected' on the display
  * thats it
