from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

# This is the session-wide link
link = 'http://localhost:8000/join/dunajigi'

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

def wait_for_elements(driver, selector, by, timeout=10):
    """Waits for multiple elements to appear before interacting with them."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((by, selector))
    )

def wait_for_clickable_element(driver, selector, by, timeout=10):
    """Waits until the element is clickable before interacting with it."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )

def click_next_button(driver): #'//button[contains(@class, "otree-btn-next")]' '//button'
    try:
        next_button = wait_for_clickable_element(driver, '//*[@id ="form"]/div/button', By.XPATH)
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        next_button.click()
    except Exception as e:
        print(f"Failed to click 'Next' button: {e}")
        raise

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
    
    click_next_button(driver) 
    # remaining function Code below not executed!

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


# Function to handle the Cats and Dogs page
def cats_and_dogs_page(driver):
    try:
        # Wait for the radio buttons to appear
        cats_or_dogs_options = wait_for_elements(driver, 'cats_or_dogs', by=By.NAME)
        print(f"Found {len(cats_or_dogs_options)} radio buttons.")
        
        if len(cats_or_dogs_options) > 0:
            rand_cats_or_dogs_index = random.randint(0, len(cats_or_dogs_options) - 1)
            selected_radio_button = cats_or_dogs_options[rand_cats_or_dogs_index]
            
            # Scroll to the selected radio button
            driver.execute_script("arguments[0].scrollIntoView(true);", selected_radio_button)
            selected_radio_button.click()
        else:
            print("No radio buttons available to select.")
            # Handle the case where no radio buttons are available
    except Exception as e:
        print(f"Failed to interact with Cats and Dogs page: {e}")
        raise

    click_next_button(driver)

# Function to handle the Pineapple on Pizza page
def pineapple_on_pizza_page(driver):
    choice = random.choice([0, 1, 2, 3, 4])
    driver.find_element(By.ID, f'id_pineapple_on_pizza-{choice}').click()

    click_next_button(driver)

# Function to handle the Money page
def money_page(driver):
    donation = random.randint(21, 2000)
    wait_for_elements(driver, 'id_money_essay', By.ID) # Wait for "money essay" textarea
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
        screening_page(driver)
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