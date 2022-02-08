### Import necessary modules
import csv
from bs4 import BeautifulSoup   # BeautifulSoup4
from playwright.sync_api import sync_playwright   # Playwright


### Take user input for name of CSV file. Append '.csv' to the end. Store in dirty_dataset_name.
### Slice .csv off dirty_dataset_name. Append '_clean' and store in clean_dataset_name.




def file_import():
    """
    Open and import CSV file dirty_dataset_name. Returns dirty_list, a list of dictionaries, 
    one for each row.
    """
    dirty_dataset_name = 'addresses.csv' #input("Enter name of address CSV file: ") + '.csv'
    try:
        with open(dirty_dataset_name, 'r') as f:
            dirty_list = list(csv.DictReader(f))
            return dirty_list
    except:
        print("""File error: file not found or incorrect type. File must be in the directory
        with the python script. Please try again.""")
        file_import()

def file_export():
    """
    Pulls field names from dictionary key list. Creates a new CSV file and appends everything from
    the clean dataset.
    """
    clean_dataset_name = dirty_dataset_name[:-4] + '_clean'
    field_names = dirty_addr_list[0].keys()
    with open(clean_dataset_name + '.csv', 'w') as f:
        address_writer = csv.DictWriter(f, fieldnames=field_names)
        address_writer.writeheader()
        for address in clean_dataset:
            address_writer.writerow(address)

def normalize_case(dirty_list):
    """
    For each value in each dictionary, if the key is 'State', make it uppercase. For other 
    keys, make the value title case, ignoring 'and'.
    """
    bad_chars = ['+', '.', '#',]
    for row in dirty_list:
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

def remove_list_id(dirty_list):
    """
    If dictionary contains a key named 'Mailing ListID', remove it. If not, ignore."""
    for row in dirty_list:
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
    """
    Takes full page contents including dynamic payloads and parses html looking for the google maps img.
    Scrapes the title from the image.
    """
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
    """
    Uses playwright to open a headless chromium tab, navigates to the page URL, and returns the full
    page contents including dynamic payloads
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(page_url)
        page_content = page.content()
        browser.close()
        return page_content

def clean_map_title(map_title):
    """
    Slices the full address from the map image title. Adds comma after state for processing."""
    full_address = map_title[7:]
    cs_full_address = full_address[:-6] + ',' + full_address[-6:]
    return full_address, cs_full_address

def merge_prompt(db_addr, g_addr):
    q = input('Do you want to merge any part of this address? (y/n): ')
    if q == 'y' or q == 'Y':
        split_g_addr = g_addr.split(',')
        q2 = input('Which part would you like to merge to the database from Google? (a/c/s/z): ')
        if q2 == 'a':
            db_addr['Address'] = split_g_addr[0]
            print('The new address is: ' + db_addr)
    elif q == 'n' or q == 'N':
        pass
    else:
        print('Please check your selection.')
        merge_prompt()

def address_check(dirty_list):
    """
    Iterates the list of address dictionaries. If an adequate partial address exists, initiates address
    check against google.
    """
    q = input('Cleanup complete. Do you want to attempt to complete partial addresses with Google? (y/n): ')
    if q == 'y' or q == 'Y':
        for row in dirty_list:
            if row['Address'] and row ['City']:
                page_url = get_url(row['Address'], row['City'], row['State'], row['Postal Code'])
                print(page_url)
                page_content = get_dynamic_payload(page_url)
                map_title = scrape_map_title(page_content)
                full_address_scraped, cs_full_address = clean_map_title(map_title)
                print('The current address in the database is: {address} {city}, {state} {zipcode}'.
                    format(address = row['Address'], city = row['City'], state = row['State'], 
                    zipcode = row['Postal Code']))
                print('The address provided by Google is: ' + full_address_scraped)
                merge_prompt(row.values(), cs_full_address)
    elif q == 'n' or q == 'N':
        pass
    else:
        print('Please check your selection.')
        address_check()

def main():
    q = input('Do you want to clean up a CSV address book? (y/n): ')
    if q == 'y' or q == 'Y':
        dirty_addr_list = file_import()
        remove_list_id(dirty_addr_list)
        normalize_case(dirty_addr_list)
        address_check(dirty_addr_list)
    elif q == 'n' or q == 'N':
        pass
    else:
        print('Please check your selection.')
        main()
     

if __name__ == '__main__':
    main()


