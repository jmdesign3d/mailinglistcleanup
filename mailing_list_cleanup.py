### Import necessary modules
import csv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


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

def get_url(address, city, state, zipcode):
    """
    Takes address from address_check and searches google for 1 result and stores it in top_result.
    Dumps html from top_result into page_html. Returns string containing all html.
    """
    query_name = (address.replace(' ', '+') + '+' + city.replace(' ', '+') + '+' + 
        state) # + '+' + zipcode)
    g_search_url = 'https://www.google.com/search?q='
    page_url = g_search_url + query_name
    return page_url

def scrape_map_title(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    soup.prettify()
    try:
        map_class = soup.find('div', 'lu_map_section')
        map_img = map_class.find('img')
        map_title = map_img.attrs['title']
        return map_title
    except AttributeError:
        return 'address error'


def get_dynamic_payload(page_url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(page_url)
        page_content = page.content()
        browser.close()
        return page_content

def clean_map_title(map_title):
    full_address = map_title[7:]
    return full_address

def address_check():
    """
    Takes address components for each row and formats them to be searchable on Google. Then runs
    the address string as arg for search_goog. Runs html as arg for scrape_html.
    """
    for row in dirty_addr_list:
        if row['Address'] and row ['City']:
            page_url = get_url(row['Address'], row['City'], row['State'], row['Postal Code'])
            print(page_url)
            page_content = get_dynamic_payload(page_url)
            map_title = scrape_map_title(page_content)
            print(clean_map_title(map_title))


dirty_addr_list = file_import()
remove_list_id()
normalize_case()
address_check()




#print(dirty_addr_list) 
