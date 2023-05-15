from ciscoconfparse import CiscoConfParse
import sys
import yaml
import os
import ipaddress


def append_dict_if_new(list_of_dicts, new_dict, matching_key):
    """
    Iterates over a list of dicts and appends another dict to the list if one of its values does not already exist.

    Args:
    list_of_dicts: The list of dicts to iterate over.
    new_dict: The dict to append to the list.

    Returns:
    The updated list of dicts.
    """
    value_exists = False

    for dict in list_of_dicts:
        for key, value in new_dict.items():
            if dict[matching_key] == new_dict[matching_key]:
                value_exists = True
                break
    #   if key not in dict:
    if not value_exists:
        list_of_dicts.append(new_dict)

    return list_of_dicts

def append_dict_title(list_of_dicts, new_dict, title):
    """
    Iterates over a list of dicts and appends an outer dict to each one with an increasing number identifier
    """
    for dict in list_of_dicts:
        identifier = title + "-" + str(len(new_dict) + 1)
        new_dict[identifier] = dict

    return new_dict

def parse_config_logs(logdir):
    addresses = []
    devices = []
    addresses_yaml = {}
    devices_yaml = {}

    os.chdir(logdir)

    for file in os.listdir(logdir):

        if file.endswith(".log"):

            parse = CiscoConfParse(file, syntax='ios')


            network_name = ""
            templ_name = ""
            device_type = ""
            serial_no = ""
            default_vlan_id = "1"
            cur_address = {}
            cur_device = {}

            for gw_obj in parse.find_objects('^ip route'):

                default_gw = gw_obj.re_match_typed('^ip\sroute\s\d+\.\d+\.\d+\.\d+\/\d+\s(\d+\.\d+\.\d+\.\d+)$')

            for intf_obj in parse.find_objects('^interface vlan'):

                vlan_id = intf_obj.re_match_typed('^interface\svlan\s(\d+?)$')

                intf_ip_addr = intf_obj.re_match_iter_typed(
                    r'ip\saddress\s(\d+\.\d+\.\d+\.\d+\/\d+)$', result_type=str,
                    group=1, default='')
                
                if intf_ip_addr:
                    subnet = str(ipaddress.ip_network(intf_ip_addr, strict=False))
                else:
                    subnet = "0.0.0.0/0"

                intf_name = intf_obj.re_match_iter_typed(
                    r'description\s(.*)$', result_type=str,
                    group=1, default='')
             
                cur_address = {
                        "network_name": network_name,
                        "template_name": templ_name,
                        "name": intf_name,
                        "vlan_id": vlan_id,
                        "subnet": subnet,
                        "default_gw": default_gw,
                }

                append_dict_if_new(addresses, cur_address, 'vlan_id')

            for hostname_obj in parse.find_objects('^hostname'):

                hostname = hostname_obj.re_match_typed('^hostname\s(.*)$')

            cur_device = {
                "network_name": network_name,
                "template_name": templ_name,
                "device_name": hostname,
                "device_type": device_type,
                "serial_no": serial_no,
                "vlan_id": default_vlan_id,
                "default_gw": default_gw,
            }
            append_dict_if_new(devices, cur_device, 'device_name')

    append_dict_title(addresses, addresses_yaml, 'subnet')
    append_dict_title(devices, devices_yaml, 'device')

    yaml.dump(devices_yaml, devicefile)
    yaml.dump(addresses_yaml, addressfile)

if __name__ == "__main__":

    print("")
    print("The path provided below should be structured like:")
    print("<path>/Site1/*.log")
    print("<path>/Site2/*.log... etc")
    print("Each log file should contain the text output from show running-config on Aruba switches")
    print("")
    directory = input("Enter full path to directory: ")

    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            filepath = os.path.join(directory, dir)
            addresspath = filepath + "/addresses.yaml"
            devicepath = filepath + "/devices.yaml"
            addressfile = open(addresspath, "w")
            addressfile.write("---\n")
            devicefile = open(devicepath, "w")
            devicefile.write("---\n")
            parse_config_logs(filepath)
            addressfile.close()
            devicefile.close()

