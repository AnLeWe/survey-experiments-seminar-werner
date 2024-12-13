from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import string

# This is the session-wide link
link = 'http://localhost:8000/join/zesirape'

def build_driver():
    # Set up the driver
    return webdriver.Chrome()  # Alternatively, use ChromeDriverManager for automatic setup

def check_exists_by_xpath(driver, xpath):
    try:
        x = driver.find_element(By.XPATH, xpath)
        if x.is_displayed():
            return 1
    except NoSuchElementException:
        return 0
    
def check_exists_by_id(driver, id):
    try:
        x = driver.find_element(By.ID, id)
        if x.is_displayed():
            return 1
    except NoSuchElementException:
        return 0

def click_next_button(driver):
    driver.find_element(By.XPATH, '//*[@id ="form"]/div/button').click()

# Function to handle the Welcome page
def welcome_page(driver):
    # Entry question
    entry_question_input = 'Testing Input for Entry Question'
    driver.find_element(By.ID, 'id_entry_question').send_keys(entry_question_input)

    click_next_button(driver)

# Function to handle the Demo page
def demo_page(driver):
    """
    Interacts with the demo page, filling in the age question, selecting a gender, 
    answering the travel question, and filling any associated popouts.

    Args:
        driver: Selenium WebDriver instance controlling the browser.
    """

    # Fill in the "How old are you?" field
    age = random.randint(18, 39)  # Generate a random age between 18 and 39 (>40 is screenout)
    driver.find_element(By.ID, 'id_age_question').send_keys(age)

    # Select a gender option
    gender_options = driver.find_elements(By.NAME, 'gender_question')
    rand_gender_index = random.randint(0, len(gender_options) - 1)
    gender_options[rand_gender_index].click()

    # Handle "Other" gender popout if selected
    if rand_gender_index == 4:  # "Other" is the 5th option (index 4)
        other_gender_input_xpath = "//*[@id='id_gender_popout']"
        if check_exists_by_xpath(driver, other_gender_input_xpath):
            driver.find_element(By.XPATH, other_gender_input_xpath).send_keys('Custom Gender')

    # Answer "Have you ever travelled before?"
    travel_choice = random.choice(["Yes", "No"])
    if travel_choice == "Yes":
        driver.find_element(By.ID, "travelYes").click()
        # Handle travel destination popout
        travel_destination_xpath = "//*[@id='id_travel_destination_popout']"
        if check_exists_by_xpath(driver, travel_destination_xpath):
            driver.find_element(By.XPATH, travel_destination_xpath).send_keys("Random Destination")
    else:
        driver.find_element(By.ID, "travelNo").click()

    click_next_button(driver)

# Function to handle the Screening page
def screening_page(driver):
    """
    Handles the Screening page, checking for screenout or quota conditions,
    and navigating accordingly.

    Args:
        driver: Selenium WebDriver instance controlling the browser.
    """
    pass
    # Screenout and quota URLs (modify these as needed)
    url_screenout = "/static/ScreenoutLink.html" # these are also in the Screening.html template...
    url_quota = "/static/QuotaFullLink.html"

    # Check for screenout condition
    screenout = driver.execute_script("return window.screenout;")
    if screenout == 1:
        driver.get(url_screenout)

    # Check for quota condition
    quota = driver.execute_script("return window.quota;")
    if quota == 1:
        driver.get(url_quota)

    click_next_button(driver)

# Function to handle the Cats and Dogs page
def cats_and_dogs_page(driver):
    cats_or_dogs_options = driver.find_elements(By.NAME, 'cats_or_dogs')
    choice = random.choice(['1', '2', '3', '4'])  # Random choice
    for option in cats_or_dogs_options:
        if option.get_attribute('value') == choice:
            option.click()
            break

    click_next_button(driver)

# Function to handle the Pineapple on Pizza page
def pineapple_on_pizza_page(driver):
    choice = random.choice([0, 1, 2, 3, 4])
    driver.find_element(By.ID, f'id_pineapple_on_pizza-{choice}').click()

    click_next_button(driver)

# Function to handle the Money page
def money_page(driver):

    donation = random.randint(21, 2000)
    driver.find_element(By.ID, 'id_money_essay').send_keys('This is my essay.')
    driver.find_element(By.ID, 'id_money_question').send_keys(donation)

    click_next_button(driver)

# Function to handle the End page (final submission)
def end_of_survey(driver):
    # Submit the form to end the survey
    click_next_button(driver)

def run_bots(times, link):
    driver = build_driver()
    for i in range(times):  # Iterate through the survey
        driver.get(link)  # Open the browser to the URL of your survey
        # Welcome page - entry question and eligibility
        welcome_page(driver)
        # Demo page - age, gender, etc.
        demo_page(driver)
        # Screening page – to old?, to many male?
        #screening_page(driver)
        # Randomized pages (Cats and Dogs or Pineapple on Pizza)
        if check_exists_by_id(driver, 'id_pineapple_on_pizza-0') == 1:  # Check for Pineapple on Pizza
            pineapple_on_pizza_page(driver)
        else:  # Otherwise, it's the Cats and Dogs page
            cats_and_dogs_page(driver)
        # Money page
        money_page(driver)
        # End page
        end_of_survey(driver)

    print("Success!")

run_bots(times=20, link=link)