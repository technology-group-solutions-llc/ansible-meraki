import csv
import yaml

def create_yaml_file(csv_file, yaml_file):
  """Creates a YAML file from a CSV file.

  Args:
    csv_file: The path to the CSV file.
    yaml_file: The path to the YAML file.

  """

  new_data_yaml = {}

  with open(csv_file, 'r') as csv_file_reader:
    reader = csv.DictReader(csv_file_reader)
    data = [row for row in reader if row['S/N'] != "" and row['Meraki Port'] != "1" and row['Access Policy'] != "Not Used"]
    new_data = [{k:v for k,v in d.items() if k in ['Meraki Port', 'Name', 'Access Policy', 'Access/Trunk', 'Access/Native VLAN', 'Tagged VLANs', 'Port Tag', 'STP guard', 'PoE', 'S/N']} for d in data]
  
  # append_dict_title(new_data, new_data_yaml, 'device')
    
  with open(yaml_file, 'w') as yaml_file_writer:
    yaml_file_writer.write("ports:\n")
    yaml_writer = yaml.dump(new_data, yaml_file_writer)

def append_dict_title(list_of_dicts, new_dict, title):
    """
    Iterates over a list of dicts and appends an outer dict to each one with an increasing number identifier

    Args:
    list_of_dicts: The list of dicts to iterate over
    new_dict: The new dict to append to
    title: The outer dict title to add to the new dict (ie - "subnet-" would add an outer dict of subnet-1, subnet-2, etc)

    Returns:
    The updated dict.
    """
    for dict in list_of_dicts:
        identifier = title + "-" + str(len(new_dict) + 1)
        new_dict[identifier] = dict

    return new_dict

if __name__ == '__main__':
  print("")
  print("Run this from the directory where the playbook that will use the devices.yaml resides")
  print("This will create a devices.yaml file in the same directory")
  print("")
  print("The CSV file needs to have these headings:")
  print("device_name, serial_no, network_name, site_address")
  print("")
  csv_file = input("Enter name of the CSV file you would like to use as input: ")
  print("")
  yaml_file = 'ports.yaml'
  create_yaml_file(csv_file, yaml_file)