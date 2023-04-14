from selenium import webdriver
import gspread
import os

# Set the URL of the Vanguard login page
url = 'https://login.vanguardinvestor.co.uk/login'

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
driver.get(url)

# Fill in the login form
username_field = driver.find_element_by_id('vg-auth0-login-username')
username_field.send_keys(username)

password_field = driver.find_element_by_name('vg-auth0-login-password')
password_field.send_keys(password)

login_button = driver.find_element_by_id('vg-sign-in-header-1')
login_button.click()

# Wait for the page to load
driver.implicitly_wait(10)

# Extract the rate of return from the page
rate_of_return = driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/div[1]/div[3]/div[2]/div/div/div/div[1]/div[3]/div/div/div[1]/div/div/span')
rate_of_return = rate_of_return.text

# Close the Chrome driver
driver.quit()

# Authenticate with Google Sheets API
gc = gspread.service_account()

# Open the Google sheet
worksheet = gc.open_by_url(google_sheet_url).worksheet(worksheet_name)
currentRow = len(worksheet.row_values(1))
nextRow = currentRow + 1
# Write the rate of return to the worksheet
worksheet.update_cell(1, nextRow, rate_of_return)
