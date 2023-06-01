# ansible-meraki
Add Meraki switches to network sites

Much of the Ansible code here originall came from 
* [Meraki-Ansible-Deployment](https://github.com/sttrayno/Meraki-Ansible-Deployment/tree/master)

# Normal workflow
## Update Excel Inventory Workbook and export CSV
The easiest way I have found to do this so far is:
1. Fill in the site_name, site_address, and device_name fields in the inventory spreadsheet on sharepoint for the devices you want to add
2. Select the entire Inventory tab's fields by clicking the upper left box in the sheet
3. Copy to clipboard (CTRL-C)
4. Open Excel on your machine, paste the data, Save As csv

## Place the CSV file on the machine where you will run ansible
You could run ansible from a linux machine in the lab or even from WSL on your windows machine
I would recommend placing the csv file in a directory that is easy to type, ie. C:\Temp

## Clone this repo to the linux machine where you will run ansible (or to WSL)
git clone https....
cd ansible-meraki
## Run the create_yaml_from_csv.py script
python3 scripts/create_yaml_from_csv.py
Type the path to the csv file and the network name you want to work with
This should output a devices.yaml file in the current directory. Verify the file looks good.

## Verify the Network is created
ansible-playbook -i inventories/hosts query-sites.yml
This will prompt for the network name. If the Network is not yet created stop and talk to the network engineers.

## Run query-and-add-devices.yml to add the devices to the Network
ansible-playbook -i inventories/hosts query-and-add-devices.yml

# scripts

## create_yaml_from_csv.py
This script will prompt for a CSV file to use as input. Next, it will prompt for the Network Name you want to search the CSV file for. It will then search the CSV file for column headings of "device_name, serial_no, site_name, site_address" and rows that have the site_name set to the Network name specified, and output the data from those columns to a devices.yaml file which can be used as input to the playbooks.

# playbooks

## query-sites.yml
Run with: ansible-playbook -i inventories/hosts query-sites.yml

This playbook will query the user for what network name they want to check Meraki Cloud for. You can choose to enter a specific name to search for or leave it blank and it will display all of the networks in the org. It will error out if the network has not been created yet. If successful, it will either display a list of all Networks in the Org or it will display a list of devices attached to the network specified.

## query-and-add-devices.yml
Run with: ansible-playbook -i inventories/hosts query-and-add-devices.yml

This playbook will read the devices.yaml file in the same directory and check Meraki Cloud for the devices listed. If the device is not already attached to the network in the site_name field then it will call the playbook deploy-newdevice-fromyaml.yml in order to add it

## deploy-newdevice-fromyaml.yml
Run with: DO NOT run this individually. It is called by query-and-add-devices.yml

This playbook will read the devices.yaml file in the same directory and add the device specified at runtime to
the Network listed in the site_name field on Meraki Cloud

## delete-device.yml
Run with: ansible-playbook -i inventories/hosts delete-device.yml

This playbook will query the user for a serial number and network name. It will then delete the device with that serial number from the network specified. Do not run this unless you really intend to delete the device.
# archive
## create_yaml_from_aruba.py
This script is not updated and not currently used
I have added a script (scripts/create_yaml_from_aruba.py) to help with creating the yaml vars files needed for Ansible based on "show running-config" output from Aruba switches. The resulting addresses.yaml and devices.yaml files will need some manual editing to add in device serial numbers, and device configuration templates for each site.
## deploy-branch-readyaml.yml
This was originally created when working with the above script and was never completed
