#!/usr/bin/env python3

import glob
import json
import os
import requests
import subprocess
import sys


class autotss:
    def __init__(self):
        self.tsschecker = self.check()
        self.devices = self.get_devices()
        self.check_devices()
        self.api = self.get_api()
        self.save_blobs()

    def get_devices(self):
        if not os.path.isfile('devices.json'):
            sys.exit('[ERROR] No devices.json found. Exiting...')

        with open('devices.json', 'r') as f:
            return json.load(f)

    def get_api(self):
        api = requests.get('https://api.ipsw.me/v2.1/firmwares.json/condensed').json()

        for x in list(api['devices']):
            if x in self.devices:
                api['devices'].pop(x)
                return

            for y in list(api['devices'][x]['firmwares']):
                if y['signed'] is False:
                    api['devices'][x]['firmwares'].pop(api['devices'][x]['firmwares'].index(y))

        return api['devices']

    def check_devices(self):
        api = requests.get('https://api.ipsw.me/v2.1/firmwares.json/condensed').json()

        for x in range(len(self.devices)):
            if self.devices[str(x)]['identifier'] not in api['devices']:
                sys.exit(f"[ERROR] Device [Name: {x['name']}, Identifier: {x['identifier']}] does not exist. Please remove it from the config. Exiting...")

    def save_blobs(self):
        for x in list(self.devices):
            for i in list(self.api[self.devices[x]['identifier']]["firmwares"]):
                save_path = f"blobs/{self.devices[x]['identifier']}/{self.devices[x]['ecid']}/{i['version']}/{i['buildid']}"
                os.makedirs(save_path, exist_ok=True)

                if len(glob.glob(f'{save_path}/*.shsh*')) > 0:
                    print(f"[NOTE] Blobs already saved for [Device: {self.devices[x]['name']}, iOS Version: {i['version']}, buildid {i['buildid']}].")
                    continue

                tsschecker_args = (self.tsschecker,
                                   '-d', self.devices[x]['identifier'],
                                   '-e', self.devices[x]['ecid'],
                                   '--boardconfig', self.devices[x]['boardconfig'],
                                   '--buildid', i['buildid'],
                                   '--save-path', save_path,
                                   '-s')

                tsschecker = subprocess.run(tsschecker_args, stdout=subprocess.PIPE, universal_newlines=True)

                if 'Saved shsh blobs!' in tsschecker.stdout:
                    print(f"Saved SHSH blobs for [Device: {self.devices[x]['name']}, iOS Version: {i['version']}, buildid {i['buildid']}].")
                else:
                    print(f"[ERROR] Failed to save SHSH blobs for [Device: {self.devices[x]['name']}, iOS Version: {i['version']}, buildid {i['buildid']}].")
                    print(tsschecker.stdout)

    def check(self):
        tsschecker = subprocess.run(('which', 'tsschecker'), stdout=subprocess.PIPE, universal_newlines=True)
        if tsschecker.returncode == 0:
            path = tsschecker.stdout[:-1]
        else:
            sys.exit(f"[ERROR] tsschecker was not found. Build & install the latest version from 'https://github.com/tihmstar/tsschecker'. Exiting...")

        tsschecker = subprocess.run((path), stdout=subprocess.PIPE, universal_newlines=True)

        version = int(tsschecker.stdout.split('\n')[0].split('-')[1][1:])
        if version < 319:
            sys.exit("[ERROR] Your version of tsschecker is too old. Build & install the latest version from https://github.com/tihmstar/tsschecker. Exiting...")

        return path


def main():
    autotss()

if __name__ == "__main__":
    main()
