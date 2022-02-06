### Import necessary modules
import csv


### Take user input for name of CSV file. Append '.csv' to the end. Store in dirty_dataset_name.
### Slice .csv off dirty_dataset_name. Append '_clean' and store in clean_dataset_name.
dirty_dataset_name = 'addresses.csv' #input("Enter name of address CSV file: ") + '.csv'
clean_dataset_name = dirty_dataset_name[:-4] + '_clean'

def file_import():
    """
    Open and import CSV file dirty_dataset_name. Returns dirty_list, a list of dictionaries, one for each row.
    """
    with open(dirty_dataset_name, 'r') as f:
        dirty_list = list(csv.DictReader(f))
        return dirty_list

def file_export():
    with open(clean_dataset_name + '.csv', 'w') as clean_addresses:
        address_writer = csv.DictWriter(clean_addresses)
        address_writer.writeheader()
        for address in clean_dataset:
            address_writer.writerow(address)

def normalize_case():
    for row in dirty_addr_list:
        for key in row.keys():
            value = row[key]
            if key.lower() == 'state':
                new_value= value.upper()
            else:
                new_value = value.title().replace(' And ', ' and ')
            row.update({key: new_value})

def remove_list_id():
    for row in dirty_addr_list:
        try:
            del row['Mailing ListID']
        except:
            pass




dirty_addr_list = file_import()

remove_list_id()
normalize_case()
print(dirty_addr_list) 