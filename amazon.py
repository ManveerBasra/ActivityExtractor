#!/usr/bin/python3

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import common
import time

SERVICE = 'AMAZON'


class AmazonActivityExtractor:

    """
    Class to retrieve and download user's activity history from Amazon
    """

    def __init__(self, parameters):
        self.parameters = parameters
        self.driver = None
        self.activity_list = []

    def get_activity(self):
        """
        The main function that lets the user download their Amazon activity
        """
        self.login_amazon()

    def login_amazon(self):
        """
        Logs into Amazon
        """
        
        print('Logging into Amazon')

        # Keep track of whether user passed options in 'userconfig.ini'
        args_passed = False

        if self.parameters['chrome_args'] != '':
            args_passed = True
            self.driver = webdriver.Chrome(chrome_options=self.parameters['chrome_args'])

        # Initialising Chrome driver
        if not args_passed:
            self.driver = webdriver.Chrome()
        self.driver.get(self.parameters['url'])

        # Clearing email textbox and typing in user's email
        self.driver.find_element_by_id('ap_email').clear()
        self.driver.find_element_by_id('ap_email').send_keys(self.parameters['email'])

        time.sleep(1)

        # Clearing password textbox and typing in user's password
        self.driver.find_element_by_id('ap_password').clear()
        self.driver.find_element_by_id('ap_password').send_keys(self.parameters['password'])

        time.sleep(1)

        # Clicking on submit button
        self.driver.find_element_by_id('signInSubmit').click()

        # Navigate to viewing activity page
        self.driver.get('https://www.amazon.com/gp/yourstore/iyr/ref=pd_ys_iyr_edit_watched?ie=UTF8&collection=watched')

        self.navigate_pages()

    def navigate_pages(self):
        """
        Navigates to the Viewing History page
        """
        print('Retrieving viewing activity...')

        # List that is filled with strings of viewing activity
        self.activity_list = []

        done = False
        while not done:
            self.get_page_activity()
            try:
                self.driver.find_element_by_id('iyrNext').click()
                time.sleep(1)
            except WebDriverException:
                done = True

        common.output_activity(SERVICE, self.activity_list)

    def get_page_activity(self):
        """
        Gets all viewing activity on current page
        """

        # List that contains all row elements on viewing activity page
        row_list = self.driver.find_elements_by_xpath('//*[contains(@id, "iyrListItemTitle")]')

        for row in row_list:
            self.activity_list.append(row.text + '\n')
