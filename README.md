# AutoTSS-cli
A script to automatically save [SHSH blobs](https://www.theiphonewiki.com/wiki/SHSH/) for signed iOS/iPadOS firmwares using [tsschecker](https://github.com/tihmstar/tsschecker/) and [IPSW.me](https://ipsw.me/)'s APIs.

## Usage
0. Install required libraries:
    - `pip3 install -r requirements.txt`
1. Run `confgen.py` to add your device(s) to the configuration file (2 methods):
    - Automatic:
        - Run `python3 confgen.py -a` to automatically get the device information from a connected device
    - Manual:
        - Run `python3 confgen.py -m` to manually enter in device information
        - [Find your device identifier](https://ipsw.me/device-finder/)
        - [Find your device ECID](https://www.theiphonewiki.com/wiki/ECID#Getting_the_ECID) (only hex is allowed)
        - Find your device boardconfig (You can find this in the GeekBench app under 'Motherboard')
2. Build & install the latest version of [tsschecker](https://github.com/tihmstar/tsschecker/)
3. Run `python3 autotss.py`
4. (Optional) Schedule autotss to run frequently to save blobs for firmwares as they are signed
    - Install cron on your system
    - Add `*/10 * * * * /bin/bash -c "cd AUTOTSS_DIR && python3 autotss.py"` to your crontab
        - Replace `AUTOTSS_DIR` with the full path to your AutoTSS-cli folder
        - This runs every 10 minutes, but the frequency can be altered by changing the `10` in `*/10` to a different number of minutes.
            - It's not recommended to go any lower than 10 minutes, as this may result in your IP being blacklisted from Apple's servers

## Requirements
* python 3
* cron (optional, but recommended for full automation)
* [libimobiledevice](https://github.com/libimobiledevice/libimobiledevice/)
* [tsschecker](https://github.com/tihmstar/tsschecker/)

## To Do
- [ ] Add support for signing automatically when a new iOS/iPadOS version is released