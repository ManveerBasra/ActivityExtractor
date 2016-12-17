#!/usr/bin/python3

from selenium import webdriver
from selenium.common.exceptions \
    import StaleElementReferenceException, WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import common
import time

SERVICE = 'NETFLIX'


class NetflixActivityExtractor:

    """
    Class to retrieve and download user's activity history from Netflix
    """

    def __init__(self, parameters):
        self.parameters = parameters
        self.driver = None

    def getActivity(self):
        """
        The main function that lets the user download their Netflix activity
        """
        self.loginNetflix()

    def loginNetflix(self):
        """
        Logs into Netflix
        Calls: getActiveProfile()
        """
        print('Logging into Netflix')

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
        mutliPageLogin = False

        # Clearing email textbox and typing in user's email
        self.driver.find_element_by_name('email').clear()
        self.driver.find_element_by_name('email').send_keys(self.parameters['email'])

        # Clearing password textbox
        try:
            self.driver.find_element_by_name('password').clear()
        except NoSuchElementException:
            # It is a double page login. So we first need to click on "Next" and then send the password
            self.driver.find_element_by_class_name('login-button').click()
            mutliPageLogin = True

        time.sleep(1)

        if mutliPageLogin:
            self.driver.find_element_by_name('password').clear()

        # Typing in user's password
        self.driver.find_element_by_name('password').send_keys(self.parameters['password'])

        # Sometimes Netflix displays the password in a drop-down menu, if that happens
        # this block of code hides the password
        try:
            self.driver.find_element_by_link_text('Hide Password').click()
        except NoSuchElementException:
            pass

        # Clicking on submit button
        self.driver.find_element_by_class_name('login-button').click()

        try:
            # Wait for profiles page to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'profile-icon')))
        except TimeoutException:
            # If a TimeoutException occurs, it means user credentials were incorrect
            logged_in = False

        if logged_in:
            self.getActiveProfile()
        else:
            print('Error: Incorrect Credentials.\n' 
                  + '       Please check if you entered the correct email and password in \'userconfig.ini\'')

    def getActiveProfile(self):
        """
        Selects Netflix profile
        Calls:  navigateSite()
        """
        # Obtain profiles and names
        profiles = self.driver.find_elements_by_class_name('profile-icon')
        users = self.driver.find_elements_by_class_name('profile-name')

        # If profiles in empty, it means there is only one default profile on the account
        if profiles is not None:
            print('Selecting Profile')
            # Iterate through names to check for a match with user's profile name
            for i in range(len(profiles)):
                try:
                    if users[i].text == self.parameters['user']:
                        # Click profile image associated with name
                        profiles[i].click()
                        self.navigateSite()
                    elif i == len(profiles):
                        print('Error: Your profile name (\'%s\') was not found.\n' % self.parameters['user']
                              + '       Please check if you entered the correct profile name in \'userconfig.ini\'')
                except StaleElementReferenceException:
                    pass
                except WebDriverException:
                    pass

    def navigateSite(self):
        """
        Navigates to 'Viewing Activity' page
        Calls: hoverClick(), scrollToBottom()
        """
        # Wait for browse page to load
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'profile-icon')))
        print('Navigating Site')

        time.sleep(2)
        hoverClicked = self.hoverClick()

        # Navigate to page containing viewing activity
        if hoverClicked:
            self.driver.find_element_by_link_text('Viewing activity').click()
            self.scrollToBottom()
        else:
            print('Closing Program')

    def hoverClick(self):
        """
        Hovers on user avatar and clicks 'Your Account'
        Returns: Boolean
        """
        # Hover then click sometimes fails, so it runs until it works with a maximum of 3 attempts
        hov_profile = self.driver.find_element_by_class_name('profile-icon')
        error_count = 1
        while True:
            try:
                # On some systems the profile icon is displayed differently.
                # For this reason if the previous attempt doesn't work,
                # the program searches for a different item that will do the same thing when clicked as the profile-icon
                if error_count == 1:
                    hov_profile = self.driver.find_element_by_class_name('profile-name')
                elif error_count == 2:
                    hov_profile = self.driver.find_element_by_class_name('profile-arrow')
                elif error_count == 3:
                    hov_profile = self.driver.find_element_by_class_name('avatar')
                elif error_count == 4:
                    hov_profile = self.driver.find_element_by_class_name('profile-link')
                elif error_count == 5:
                    hov_profile = self.driver.find_element_by_class_name('account-dropdown-button')
                elif error_count == 6:
                    hov_profile = self.driver.find_element_by_class_name('account-menu-item')
                elif error_count == 7:
                    hov_profile = self.driver.find_element_by_class_name('current-profile')
                else:
                    print('Error: Program was unable to find profile picture.\n'
                          + '       Please report this issue to m13basra@gmail.com')
                    return False

                # Attempt to move to profile icon
                hov = ActionChains(self.driver).move_to_element(hov_profile)
                hov.perform()

                time.sleep(1)

                # Click on 'Your Account' which appears from drop-down menu provoked in previous step
                self.driver.find_element_by_link_text('Your Account').click()
                return True
            except:
                error_count += 1

    def scrollToBottom(self):
        """
        Scrolls to bottom of 'Viewing Activity' page
        Calls: outputActivity()
        """

        print('Scrolling to bottom of page (this may take a while)')

        # Scroll to the bottom of the page
        lenOfPageScript = \
            'window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;'
        lenOfPage = self.driver.execute_script(lenOfPageScript)
        match = False
        while not match:
            lastCount = lenOfPage
            time.sleep(2)
            lenOfPage = self.driver.execute_script(lenOfPageScript)
            if lastCount == lenOfPage:
                match=True

        self.getPageActivity()

    def getPageActivity(self):
        """
        Gets viewing activity and outputs into 'netflix_activity.txt'
        """
        print('Retrieving viewing activity')

        # List that is filled with strings of viewing activity
        activity_list = []
        # List that contains all row elements on viewing activity page
        row_list = self.driver.find_elements_by_class_name('retableRow')
        # For every item viewed, appends to activity_list
        print('Progress:')
        print('\t[' + (' ' * 20) + ']' + ' 0%', end='\r')
        for row, i in zip(row_list, range(1, len(row_list))):
            date_cell = row.find_elements_by_tag_name('div')[0]
            title_cell = row.find_elements_by_tag_name('div')[1]
            activity_list.append(date_cell.text + ' - ' + title_cell.text + '\n')
            # Display progress bar to user
            percent_comp = i / len(row_list)
            fill_bar = round(19 * percent_comp)
            print('\t[' + ('#' * fill_bar) + (' ' * (20-fill_bar)) + '] ' + str(round(percent_comp*100)) + '%', end='\r')

        print('\t[' + ('#' * 20) + ']' + ' 100%')
        # Close driver
        self.driver.close()

        common.outputActivity(SERVICE, activity_list)
