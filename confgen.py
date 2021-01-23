#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys
import time


def automatic():
    if os.path.isfile('devices.json'):
        with open('devices.json') as f:
            devices = json.load(f)
            x = int(len(devices))
    else:
        devices = {}
        x = 0

    print('Starting automatic configuration generator')
    print('Plug in a device to add to the configuration file')
    print('[NOTE] Devices that have already been added will not be added again.')
    print('Press CTRL+C to exit.')

    last_udid = []
    while True:
        device_check = subprocess.run(('idevice_id', '-l'), stdout=subprocess.PIPE, universal_newlines=True)

        if len(device_check.stdout) < 5:
            continue

        if device_check.stdout[:-1] not in last_udid:
            last_udid.append(device_check.stdout[:-1])
            device_name = subprocess.run(('ideviceinfo', '-k', 'DeviceName', '-u', device_check.stdout[:-1]), stdout=subprocess.PIPE, universal_newlines=True)
            product_type = subprocess.run(('ideviceinfo', '-k', 'ProductType', '-u', device_check.stdout[:-1]), stdout=subprocess.PIPE, universal_newlines=True)
            ecid = subprocess.run(('ideviceinfo', '-k', 'UniqueChipID', '-u', device_check.stdout[:-1]), stdout=subprocess.PIPE, universal_newlines=True)
            hardware_model = subprocess.run(('ideviceinfo', '-k', 'HardwareModel', '-u', device_check.stdout[:-1]), stdout=subprocess.PIPE, universal_newlines=True)

            for i in [device_name, product_type, ecid, hardware_model]:
                if i.returncode != 0:
                    continue

            if devices:
                for x in devices:
                    if hex(int(ecid.stdout[:-1])) in devices[x]['ecid']:
                        exists = True
                        break

                try:
                    if exists:
                        continue
                except UnboundLocalError:
                    pass

            print(f'Added device: [name: {device_name.stdout[:-1]}, identifier: {product_type.stdout[:-1]}, ecid: {hex(int(ecid.stdout[:-1]))}, boardconfig: {hardware_model.stdout[:-1]}] to configuration profile.')

            devices[x] = {'name': device_name.stdout[:-1], 'identifier': product_type.stdout[:-1], 'ecid': hex(int(ecid.stdout[:-1])), 'boardconfig': hardware_model.stdout[:-1]}

            with open('devices.json', 'w') as f:
                json.dump(devices, f, indent=4)

            x += 1

        time.sleep(1)


def menu():
    print('AutoTSS Configuration Generator\n')
    print('[0] Add a device to the AutoTSS configuration')
    print('[1] Remove a device from the AutoTSS configuration')
    print('[2] Exit')

    choice = input('Choose an option: ')
    
    try:
        if int(choice) not in range(0, 3):
            sys.exit('[ERROR] Invalid option given. Exiting...')

    except ValueError:
        sys.exit('[ERROR] Invalid option given. Exiting...')

    return int(choice)


def add_device():
    if os.path.isfile('devices.json'):
        with open('devices.json') as f:
            devices = json.load(f)
            x = int(len(devices))
    else:
        devices = {}
        x = 0

    device_name = input('Device Name: ')
    if not device_name:
        sys.exit('[ERROR] No name given. Exiting...')

    device_identifier = input('Device Identifier (ex. iPhone10,2): ')
    if not device_identifier:
        sys.exit('[ERROR] No identifier given. Exiting...')

    device_ecid = input("Device ECID (hex): ")
    if not device_ecid:
        sys.exit('[ERROR] No boardconfig given. Exiting...')
    elif not device_ecid.startswith('0x'):
        device_ecid = f'0x{device_ecid}'

    device_boardconfig = input('Device boardconfig (ex. n51ap): ')
    if not device_boardconfig:
        sys.exit('[ERROR] No boardconfig given. Exiting...')

    devices[x] = {'name': device_name, 'identifier': device_identifier, 'ecid': device_ecid, 'boardconfig': device_boardconfig}

    with open('devices.json', 'w') as f:
        json.dump(devices, f, indent=4)

    print(f'Added device [name: {device_name}, identifier: {device_identifier}, ECID: {device_ecid}, boardconfig: {device_boardconfig}] to configuration file.\n')


def remove_device():
    if not os.path.isfile('devices.json'):
        sys.exit("[ERROR] Cannot remove device from a configuration file that doesn't exist. Exiting...")

    with open('devices.json') as f:
        devices = json.load(f)
        x = int(len(devices))

    print('Which device would you like to remove?\n')
    for i in devices:
        print(f'[{i}] [name: {devices[i]["name"]}, identifier: {devices[i]["identifier"]}, ECID: {devices[i]["ecid"]}, boardconfig: {devices[i]["boardconfig"]}]')
    print(f'[{x}] Exit')

    choice = input('Choose an option: ')

    if int(choice) == x:
        sys.exit('Exiting...')
    elif choice not in devices:
        sys.exit('[ERROR] Invalid option given. Exiting...')

    print(f'Removed device [name: {devices[i]["name"]}, identifier: {devices[i]["identifier"]}, ECID: {devices[i]["ecid"]}, boardconfig: {devices[i]["boardconfig"]}] from configuration file.\n')

    del devices[choice]

    with open('devices.json', 'w') as f:
        json.dump(devices, f, indent=4)


def manual():
    while True:
        choice = menu()
        if choice == 0:
            add_device()
        elif choice == 1:
            remove_device()
        elif choice == 2:
            sys.exit('Exiting...')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AutoTSS Configuration Generator', usage="./confgen.py [-a/-m] [-v]")
    parser.add_argument('-a', '--automatic', help='Generate configuration from a connected device', action='store_true')
    parser.add_argument('-m', '--manual', help='Enter device information manually', action='store_true')
    args = parser.parse_args()

    if not args.automatic and not args.manual:
        sys.exit(parser.print_help(sys.stderr))

    elif args.automatic and args.manual:
        sys.exit(parser.print_help(sys.stderr))

    if args.automatic:
        automatic()

    if args.manual:
        manual()
