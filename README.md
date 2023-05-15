# ansible-meraki
Configure Meraki sites and add switches

Much of the Ansible code here originall came from 
* [Meraki-Ansible-Deployment](https://github.com/sttrayno/Meraki-Ansible-Deployment/tree/master)

I have added a script (scripts/create_yaml_from_aruba.py) to help with creating the yaml vars files needed for Ansible based on "show running-config" output from Aruba switches. The resulting addresses.yaml and devices.yaml files will need some manual editing to add in device serial numbers, and device configuration templates for each site.

The network name for each site is derived from the folder that contains the .log files for the switches.

