### Import necessary modules
import csv
from googlesearch import search
import requests

### Take user input for name of CSV file. Append '.csv' to the end. Store in dirty_dataset_name.
### Slice .csv off dirty_dataset_name. Append '_clean' and store in clean_dataset_name.
dirty_dataset_name = 'addresses.csv' #input("Enter name of address CSV file: ") + '.csv'
clean_dataset_name = dirty_dataset_name[:-4] + '_clean'

def file_import():
    """
    Open and import CSV file dirty_dataset_name. Returns dirty_list, a list of dictionaries, 
    one for each row.
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
    """
    For each value in each dictionary, if the key is 'State', make it uppercase. For other 
    keys, make the value title case, ignoring 'and'.
    """
    bad_chars = ['+', '.', '#',]
    for row in dirty_addr_list:
        for key in row.keys():
            value = row[key]
            for char in bad_chars:
                value = value.replace(char,'')
            value = value.strip()
            if key.lower() == 'state':
                new_value= value.upper()
            else:
                new_value = value.title().replace(' And ', ' and ')
            row.update({key: new_value})

def remove_list_id():
    """
    If dictionary contains a key named 'Mailing ListID', remove it. If not, ignore.
    """
    for row in dirty_addr_list:
        try:
            del row['Mailing ListID']
        except:
            pass

def search_goog(address):
    """
    Takes address from address_check and searches google for 1 result and stores it in top_result.
    Dumps html from top_result into page_html. Returns string containing all html.
    """
    page_html = ''
    g_search_url = 'https://www.google.com/search?q='
    top_result = list(search(address, num_results=1))[0]
    print(top_result)
    page_html = requests.get(url = top_result).text
    return page_html

def scrape_html(page):
    pass

def address_check():
    """
    Takes address components for each row and formats them to be searchable on Google. Then runs
    the address string as arg for search_goog. Runs html as arg for scrape_html.
    """
    for row in dirty_addr_list:
        if row['Address'] and row ['City']:
            address = (row['Address'].replace(' ', '+') + '+' + row['City'].replace(' ', '+') + '+' + 
            row['State'])# + '+' + row['Postal Code'])
        print(address)
        #search_results = search_goog(address)
        #scrape_html(search_results)



dirty_addr_list = file_import()
remove_list_id()
normalize_case()
address_check()

#print(dirty_addr_list) 
