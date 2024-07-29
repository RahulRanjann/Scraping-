from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import pandas as pd

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    # Open the webpage
    driver.get('https://bidkaro.net/')  # replace with the actual URL
    time.sleep(1)  # Wait for the page to load

    # Find the username and password input fields
    username_field = driver.find_element(By.ID, 'username')
    time.sleep(1)  # Wait before interacting with the next element
    password_field = driver.find_element(By.XPATH, "//input[@type='password' and @formcontrolname='password']")
    time.sleep(1)  # Wait before entering credentials

    # Enter the credentials
    username_field.send_keys('AkashAK12')
    time.sleep(1)  # Wait before entering the password
    password_field.send_keys('TataAce@123')
    time.sleep(1)  # Wait before finding and clicking the sign-in button

    # Find the sign-in button and click it
    sign_in_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'sign in')]")
    time.sleep(1)  # Wait before clicking the button
    sign_in_button.click()

    # Wait for the login process to complete
    time.sleep(5)

    # Find the "Cancel" button and click it
    cancel_button = driver.find_element(By.XPATH, "//button[@type='button' and contains(@class, 'btn-outline-secondary')]")
    time.sleep(1)  # Wait before clicking the "Cancel" button
    cancel_button.click()

    # Wait for a few seconds to observe the result
    time.sleep(3)

    # Find the "Events" dropdown link and click it
    events_dropdown = driver.find_element(By.XPATH, "//a[@role='button' and contains(@class, 'dropdown-toggle') and contains(text(), 'Events')]")
    time.sleep(1)  # Wait before clicking the "Events" link
    events_dropdown.click()

    # Wait for the dropdown to appear
    time.sleep(1)

    # Find the "Live Auctions" link and click it
    live_auctions_link = driver.find_element(By.XPATH, "//a[contains(@class, 'nav-link') and contains(text(), 'Live Auctions')]")
    time.sleep(1)  # Wait before clicking the "Live Auctions" link
    live_auctions_link.click()

    # Wait for the "Live Auctions" page to load
    time.sleep(5)

    # Find the "Location" column header and click it to apply the filter
    location_header = driver.find_element(By.XPATH, "//th[@role='columnheader' and contains(text(), 'Location')]")
    time.sleep(1)  # Wait before clicking the "Location" column header
    location_header.click()

    # Wait for the sorting/filtering to take effect
    time.sleep(3)

    # Find all table rows
    rows = driver.find_elements(By.XPATH, "//tr[@class='ui-selectable-row ng-star-inserted']")

    # List to store tab handles
    tab_handles = []

    # Iterate through each row to find "Karnataka" in the second td's span
    for row in rows:
        location_td = row.find_element(By.XPATH, ".//td[contains(., 'Location')]")
        if 'Karnataka' in location_td.text:
            # Find the "Enter" button and click it
            enter_button = row.find_element(By.XPATH, ".//td[contains(., 'Enter')]//button")
            enter_button.click()
            time.sleep(3)  # Wait to observe the result after clicking the "Enter" button

            # Switch to the new tab that opened
            driver.switch_to.window(driver.window_handles[-1])
            tab_handles.append(driver.current_window_handle)

            # Find the "Agree" button and click it
            agree_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'btn btn-orange')]")
            agree_button.click()
            time.sleep(3)  # Wait to observe the result after clicking the "Agree" button

            # Extract HTML content from the current page
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extracting data from each row
            data = []
            for auction_row in soup.find_all('tr', class_='ui-selectable-row ng-star-inserted'):
                # Extracting specific fields from each row
                image_tag = auction_row.find('img', class_='img-fluid ng-star-inserted')
                image_url = image_tag['src'] if image_tag else ''

                vehicle_name_tag = auction_row.find('a', class_='vehicle-name')
                vehicle_name = vehicle_name_tag.text.strip() if vehicle_name_tag else ''

                show_hide_links = driver.find_elements(By.XPATH, "//a[@class='show-hide-details ng-star-inserted']")
                for show_hide_link in show_hide_links:
                    print('show_hide_link', show_hide_link)
                    if 'Show details' in show_hide_link.text:
                        show_hide_link.click()
                        time.sleep(1)
                # print('show_hide_link',show_hide_link)
                # if show_hide_link and 'Show details' in show_hide_link.text:
                #     print('running')
                #     show_hide_link.click()
                #     time.sleep(1)

                field_mapping = {
                    'LAN:': 'lan_value',
                    'KM:': 'km_value',
                    'Reg No:': 'reg_value',
                    'YOR:': 'yor_value',
                    'RC:': 'rc_value',
                    'Chasis No:': 'ch_value'
                }

                extracted_values = {v: '' for v in field_mapping.values()}
                # show-hide-details ng-star-inserted

                table_para = auction_row.find_all('div', class_='table-para')
                # table_para2 = auction_row.find_all('div', class_='row ng-star-inserted')
                # for table_para_elem in table_para2:
                #     print("table_para_elem_2:",table_para_elem)
                for table_para_elem in table_para:
                    label = table_para_elem.find_all('div')[0].text.strip()
                    # print("Label:",label)
                    # print("table_para_elem:",table_para_elem)
                    if label in field_mapping:
                        extracted_values[field_mapping[label]] = table_para_elem.find_all('div')[1].text.strip()

                # table_para = auction_row.find_all('div', class_='table-para')
                # for table_para_elem in table_para:
                #     if(table_para_elem.find_all('div')[0].text.strip() == 'LAN:'):
                #         lan_value = table_para_elem.find_all('div')[1].text.strip()
                #     if(table_para_elem.find_all('div')[0].text.strip() == 'KM:'):
                #         km_value = table_para_elem.find_all('div')[1].text.strip()
                #     if(table_para_elem.find_all('div')[0].text.strip() == 'Reg No:'):
                #         reg_value = table_para_elem.find_all('div')[1].text.strip()
                #     if(table_para_elem.find_all('div')[0].text.strip() == 'YOR:'):
                #         yor_value = table_para_elem.find_all('div')[1].text.strip()
                #     if(table_para_elem.find_all('div')[0].text.strip() == 'RC:'):
                #         rc_value = table_para_elem.find_all('div')[1].text.strip()
                

                sp_incr_div = auction_row.find('bidkaro-auction-start-increment-price').find('div', class_='col-12 col-sm-12')
                sp_incr_value = sp_incr_div.text.strip() if sp_incr_div else ''

                data.append({
                    'Image': image_url,
                    'Vehicle Details': vehicle_name,
                    'LAN': extracted_values['lan_value'],
                    'KM': extracted_values['km_value'],
                    'Reg': extracted_values['reg_value'],
                    'YOR': extracted_values['yor_value'],
                    'RC': extracted_values['rc_value'],
                    'Chasis No:': extracted_values['ch_value'],
                    'SP | INCR': sp_incr_value
                })

            # Create DataFrame from extracted data
            headers = ["Image", "Vehicle Details", "LAN", "KM", "Reg", "YOR", "RC", "Chasis No", "SP | INCR"]
            df = pd.DataFrame(data, columns=headers)

            # Save to CSV
            df.to_csv('auction_data.csv', index=False)
            print("CSV file 'auction_data.csv' has been created successfully.")

            # Close the current tab
            driver.close()

            # Switch back to the main window if there are still window handles available
            if len(driver.window_handles) > 0:
                driver.switch_to.window(driver.window_handles[0])

    # Switch to each tab handle to perform further actions if required
    for tab_handle in tab_handles:
        driver.switch_to.window(tab_handle)
        # Perform additional actions in each tab if required
    
except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    # Quit the WebDriver at the end
    driver.quit()