from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import gspread
import os

def main():
    print('Run started')
    # Set the URL of the Vanguard login page
    url = 'https://login.vanguardinvestor.co.uk/login?state=hKFo2SB6ajd4YVVxNldoNE1QUmprMEw5SEsxelhxNWhuVnJTSaFupWxvZ2luo3RpZNkgaFIzU3VaZE9WM3JnempPTC10cGNfTmhTVFAzV0ZLMlWjY2lk2SBVbzlvcTgycGFONldCQ3FtSlp0S0puTkVqY2p2aTFtMw&client=Uo9oq82paN6WBCqmJZtKJnNEjcjvi1m3&protocol=oauth2&nonce=lNfr3NGO2NjeeyJyGqLzkNom&response_type=code&code_challenge_method=S256&audience=https%3A%2F%2Finternational.vanguard.com&code_challenge=kc1NQLkzLukahHFFvTmyohQ0jz9JNF530P3tSs49_rE&response_mode=query&redirect_uri=https%3A%2F%2Fsecure.vanguardinvestor.co.uk%2Flogin-callback&scope=openid%20offline_access'

    # Set the login credentials
    username = os.getenv('VANGUARD_USER')
    password = os.getenv('VANGUARD_PASS')

    # Set the URL of the Google sheet to write the data
    google_sheet_url = os.getenv('SHEET_URL')

    # Set the path to the Google Sheets credentials file
    creds_path = os.getenv('SHEET_CREDS')

    # Set the name of the worksheet to write the data
    worksheet_name = 'Sheet1'

    # Initialize the Chrome driver
    driver = webdriver.Chrome()

    # Navigate to the Vanguard login page
    print('Navigate to the Vanguard login page')
    driver.get(url)

    # Wait for the page to load
    driver.implicitly_wait(10)

    # Fill in the login form
    username_field = driver.find_element(By.ID, 'vg-auth0-login-username')
    username_field.send_keys(username)

    password_field = driver.find_element(By.ID, 'vg-auth0-login-password')
    password_field.send_keys(password)

    login_button = driver.find_element(By.ID, 'vg-sign-in-header-1')
    print('Click login')
    login_button.click()

    # Wait for the page to load
    driver.implicitly_wait(10)

    # Extract the rate of return from the page
    rate_of_return = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div/div[2]/div[1]/div[3]/div[2]/div/div/div/div[1]/div[3]/div/div/div[1]/div/div/span')
    rate_of_return = rate_of_return.text

    # Record current time
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    # Close the Chrome driver
    driver.quit()

    # Authenticate with Google Sheets API
    gc = gspread.service_account(filename=creds_path)

    # Open the Google sheet
    print('Open the Google sheet')
    worksheet = gc.open_by_url(google_sheet_url).worksheet(worksheet_name)
    current_row = len(worksheet.col_values(1))
    next_row = current_row + 1
    # Write the rate of return to the worksheet
    print('Write the rate of return to the worksheet')
    worksheet.update_cell(next_row, 1, current_time)
    worksheet.update_cell(next_row, 2, rate_of_return)

if __name__ == "__main__":
    main()