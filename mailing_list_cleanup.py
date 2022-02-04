import csv

dirty_dataset_name = 'addresses.csv' #input("Enter name of address CSV file: ") + '.csv'
clean_dataset_name = dirty_dataset_name[:-4] + '_clean'

def file_import():
    with open(dirty_dataset_name, 'r') as f:
        dirty_list = list(csv.DictReader(f))
        #for item in dirty_dict:
        #    print(item)
        return dirty_list

def file_export():
    with open(clean_dataset_name + '.csv', 'w') as clean_addresses:
        address_writer = csv.DictWriter(clean_addresses)
        address_writer.writeheader()
        for address in clean_dataset:
            address_writer.writerow(address)

def normalize_case():
    pass

#normalize_case()

dirty_addr_list = file_import()


print(dirty_addr_list)