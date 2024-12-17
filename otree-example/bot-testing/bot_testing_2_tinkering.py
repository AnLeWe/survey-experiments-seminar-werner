from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, WebDriverException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

# fails at: 
# - Demo page when travel popout? Here the destination is not filled in.
# I'm not sure if this is because of overlays. I have popouts. But they are not designed as elements that overlay others. Right?

# This is the session-wide link
link = 'http://localhost:8000/join/dunajigi'

def build_driver():
    """Sets up and returns a Selenium WebDriver instance with full-screen mode."""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()  # Maximizes the browser window
    return driver  # Alternatively, use ChromeDriverManager for automatic setup

def check_exists_by_xpath(driver, xpath):
    try:
        a_gender_question = wait_for_clickable_element(driver, 'gender_question', By.NAME)
        driver.execute_script("arguments[0].scrollIntoView(true);", a_gender_question)
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

def wait_for_clickable_element(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """Waits for an element to become clickable."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )

def wait_for_visible_element(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """Waits for an element to become visible."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, selector))
    )

def wait_for_elements(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """Waits for multiple elements to become visible."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((by, selector))
    )

def safe_click(driver, element):
    """Scrolls an element into view, and clicks it."""
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element.click()

def click_next_button(driver):
    """
    Scrolls the 'Next' button into view and clicks it. Falls back to JavaScript if standard click fails.
    """
    try:
        next_button = wait_for_clickable_element(driver, '//*[@id ="form"]/div/button', By.XPATH)
        # Scroll into view before clicking
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
        next_button.click()
    except ElementClickInterceptedException as e:
        print(f"Element click intercepted: {e}. Retrying with JavaScript click.")
        driver.execute_script("arguments[0].click();", next_button)
    except Exception as e:
        print(f"Failed to click 'Next' button: {e}")
        raise


#Pages
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
        wait_for_visible_element(driver, 'travel_destination_xpath', By.XPATH)
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
        options = wait_for_elements(driver, 'cats_or_dogs', By.NAME)
        selected_option = random.choice(options)
        safe_click(driver, selected_option)
    except Exception as e:
        print(f"Failed to interact with Cats and Dogs page: {e}")
        raise

    click_next_button(driver)

# Function to handle the Pineapple on Pizza page
def pineapple_on_pizza_page(driver):
    choice = random.choice(range(5))
    option = wait_for_clickable_element(driver, f'id_pineapple_on_pizza-{choice}', By.ID)
    safe_click(driver, option)

    driver.implicitly_wait(2)
    click_next_button(driver)

# Function to handle the Money page
def money_page(driver):
    essay_field = wait_for_visible_element(driver, 'id_money_essay', By.ID)
    essay_field.send_keys('This is my essay.')

    donation_field = wait_for_visible_element(driver, 'id_money_question', By.ID)
    donation = random.randint(21, 2000)
    donation_field.send_keys(donation)

    click_next_button(driver)

# Function to handle the End page (final submission)
def end_of_survey(driver):
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