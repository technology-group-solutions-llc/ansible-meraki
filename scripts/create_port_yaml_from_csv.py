import csv
import yaml

def create_yaml_file(csv_file, yaml_file):
  """Creates a YAML file from a CSV file.

  Args:
    csv_file: The path to the CSV file.
    yaml_file: The path to the YAML file.

  """

  new_data_yaml = {}
  new_data = {}

  with open(csv_file, 'r') as csv_file_reader:
    reader = csv.DictReader(csv_file_reader)
    data = [row for row in reader if row['serial'] != '' and row['number'] != '1' and row['Access_Policy'] != 'Not Used']
    
    new_data = [{k:v for k,v in d.items() if k in ['number', 'name', 'Access_Policy', 'type', 'vlan', 'allowed_vlans', 'tags', 'stp_guard', 'PoE', 'serial']} for d in data]
   
    for d in new_data:
        
        if d['allowed_vlans'] == '':
           d['allowed_vlans'] = ['all']
        else:
          d['allowed_vlans'] = d['allowed_vlans'].split(',')

        if 'Open' in d['Access_Policy']:
           d['access_policy_type'] =  "Open"
        elif 'Clearpass' in d['Access_Policy']:
           d['access_policy_type'] = "Custom access policy"
           d['access_policy_number'] = 1

        d['tags'] = d['tags'].split(',')

        if 'Enabled' in d['PoE']:
           d['poe_enabled'] = True
        else:
           d['poe_enabled'] = False

        if d['stp_guard'] == '':
           d['stp_guard'] = "disabled"

  with open(yaml_file, 'w') as yaml_file_writer:
    yaml_file_writer.write("ports:\n")
    yaml_writer = yaml.dump(new_data, yaml_file_writer, indent=2)

if __name__ == '__main__':
  print("")
  print("Run this from the directory where the playbook that will use the ports.yaml resides")
  print("This will create a ports.yaml file in the same directory")
  print("")
  print("The CSV file needs to have these headings:")
  print("number, name, Access_Policy, type, vlan, allowed_vlans, tags, stp_guard, PoE, serial")
  print("")
  csv_file = input("Enter name of the CSV file you would like to use as input: ")
  print("")
  yaml_file = 'ports.yaml'
  create_yaml_file(csv_file, yaml_file)