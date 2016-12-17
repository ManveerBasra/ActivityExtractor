#!/usr/bin/python3

from selenium import webdriver
from selenium.common.exceptions \
    import TimeoutException, NoSuchElementException, ElementNotVisibleException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import common
import time

SERVICE = 'HULU'


class HuluActivityExtractor:

    """
    Class to retrieve and download user's activity history from Hulu
    """

    def __init__(self, parameters):
        self.parameters = parameters
        self.driver = None
        self.activity_list = []

    def getActivity(self):
        """
        The main function that lets the user download their Hulu activity
        """
        self.loginHulu()

    def loginHulu(self):
        """
        Logs into Hulu
        Calls: getActiveProfile()
        """
        print('Logging into Hulu')

        # Keep track of whether login was successful
        logged_in = True

        # Keep track of whether user passed options in 'userconfig.ini'
        args_passed = False

        if self.parameters['chrome_args'] != '':
            args_passed = True
            self.driver = webdriver.Chrome(chrome_options=self.parameters['chrome_args'])

        # Initialising Chrome driver
        if not args_passed:
            self.driver = webdriver.Chrome()
        self.driver.get(self.parameters['url'])

        # Close potential pop-ups
        try:
            self.driver.find_element_by_class_name('lightbox-close').click()
        except NoSuchElementException:
            pass
        try:
            self.driver.find_element_by_class_name('cancel').click()
        except NoSuchElementException:
            pass

        # Press login to open up login window
        try:
            self.driver.find_element_by_class_name('login').click()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click()", self.driver.find_element_by_class_name('login'))

        # Switch driver to pop-up iframe
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="login-iframe"]'))

        # Activate email and passwords fields
        self.driver.find_element_by_name('dummy_login').click()

        # Clearing email textbox and typing in user's email
        self.driver.find_element_by_id('user_email').clear()
        self.driver.find_element_by_id('user_email').send_keys(self.parameters['email'])

        # Clearing password textbox
        self.driver.find_element_by_id('password').clear()

        # Typing in user's password
        self.driver.find_element_by_id('password').send_keys(self.parameters['password'])

        # Clicking on submit button
        self.driver.find_element_by_class_name('btn-login').click()

        # Sometimes Hulu displays a reCAPTCHA container
        # Incase that happens, ask user to complete it and press 'Login'
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'reCAPTCHA')))
            print('Please complete the reCAPTCHA task and press \'Login\'')
            input('Switch back to this window and press enter when you\'re done: ')
        except TimeoutException:
            pass

        try:
            # Wait for profiles page to load
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'TV')))
        except TimeoutException:
            # If a TimeoutException occurs, it means user credentials were incorrect
            logged_in = False

        # Switch driver back to main frame
        self.driver.switch_to.default_content()

        # Only navigate site if login was successful
        if logged_in:
            self.navigateSite()
        else:
            print('Error: Incorrect Credentials.\n' 
                  + '       Please check if you entered the correct email and password in \'userconfig.ini\'')

    def navigateSite(self):
        """
        Navigates to 'History' page
        Calls: navigatePages()
        """
        # Wait for browse page to load
        print('Navigating Site')

        time.sleep(2)
        self.driver.get('https://secure.hulu.com/account/history')

        # Call next function to get viewing activity and proceed to next pages
        self.navigatePages()

    def navigatePages(self):
        """
        Scrolls to bottom of 'Watch History' page
        Calls: outputActivity()
        """

        print('Retrieving viewing activity')

        # List that is filled with strings of viewing activity
        self.activity_list = []

        lastpage = 1
        currentpage = 1
        # Get total number of pages
        try:
            lastpage = int(self.driver.find_element_by_class_name('last-page-button').text)
        except:
            pass

        print('Progress:')
        done = False
        while not done:
            self.getPageActivity(lastpage, currentpage)
            try:
                self.driver.find_elements_by_class_name('next-page-button')[1].click()
                currentpage += 1
            except ElementNotVisibleException:
                done = True

        print('\t[' + ('#' * 20) + ']' + ' 100%')
        # Close driver
        self.driver.close()

        common.outputActivity(SERVICE, self.activity_list)

    def getPageActivity(self, lastpage, currentpage):
        """
        Gets all viewing activity on current page
        """
        # List that contains all row elements on viewing activity page
        row_list = self.driver.find_elements_by_class_name('beaconid')

        for row, i in zip(row_list, range(len(row_list))):
            self.activity_list.append(row.text + '\n')
            page_percent_comp = i / len(row_list)
            percent_comp = page_percent_comp * (currentpage / lastpage)
            fill_bar = round(19 * percent_comp)
            print('\t[' + ('#' * fill_bar) + (' ' * (20 - fill_bar)) + '] ' + str(round(percent_comp * 100)) + '%',
                  end='\r')
