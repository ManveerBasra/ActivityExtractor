"""
Module for Activity Extractor
"""
# !/usr/bin/python3

from amazon import AmazonActivityExtractor
from hulu import HuluActivityExtractor
from netflix import NetflixActivityExtractor
from configparser import ConfigParser
import argparse
import sys

SUPPORTED_SERVICES = {
    'amazon': AmazonActivityExtractor,
    'hulu': HuluActivityExtractor,
    'netflix': NetflixActivityExtractor
}


class ActivityExtractor:
    """
    Represent an main Activity Extractor object that's used to parse
    command-line arguments and call the given activity
    """

    def __init__(self):
        """
        Initialize a new ActivityExtractor object
        """
        self.args = None

        self.url = None

        self.service_class = None

    def run(self) -> None:
        """
        Main function to initialize arguments and call the given activity
        """
        # Initialize arguments and check whether the given service is supported
        self.init_arguments()
        self.check_service()

        # Get login credentials and check whether they're valid
        self.get_credentials()
        self.check_credentials()

        # Call given activity
        self.run_process()

    def check_service(self) -> None:
        """
        Check whether service in self.args is supported
        """
        if self.args.service not in SUPPORTED_SERVICES:
            print('Service not supported')
            print('Supported services include:')
            for s in SUPPORTED_SERVICES.keys():
                print('  %s' % s)
            sys.exit(2)

    def get_credentials(self) -> None:
        """
        Get login credentials and add them to self.args
        """
        # Initialising the parser
        parser = ConfigParser()
        parser.read('userconfig.ini')
        parser.optionxform = str

        # User credentials parsing dictionary
        parsing_dictionary = {'service': self.args.service.upper()}

        # Get url for browser
        self.url = parser.get(parsing_dictionary['service'], 'url')

        if self.args.email is None:
            self.args.email = parser.get(parsing_dictionary['service'], 'email')

        if self.args.password is None:
            self.args.password = parser.get(parsing_dictionary['service'],
                                            'password')

        # Netflix has an extra parameter for profile_name
        if self.args.service == 'netflix':
            self.args.user = parser.get(parsing_dictionary['service'],
                                        'profile_name')

    def check_credentials(self):
        """
        Check whether the given credentials in self.args are valid
        """
        if self.args.email is None:
            print('--email is missing\n'
                  + 'add email into \'userconfig.ini\''
                  + 'or provide email using --email')
            sys.exit(2)
        if self.args.password is None:
            print('--password is missing\n'
                  + 'add password into \'userconfig.ini\''
                  + 'or provide password using --password')
            sys.exit(2)

    def run_process(self):
        """
        Take the given arguments in self.args and call the given service class
        """
        self.service_class = SUPPORTED_SERVICES[self.args.service]({
            'url': self.url,
            'email': self.args.email,
            'password': self.args.password,
            'user': self.args.user
        })

        self.service_class.get_activity()

    def init_arguments(self):
        """
        Initialize command line argument parser and define acceptable arguments
        """
        parser = argparse.ArgumentParser(
            description='This repository gets viewing activity from user\'s '
                        'streaming service accounts.')
        parser.add_argument(
            'service',
            help='Specify streaming service to get viewing activity from.')
        parser.add_argument('--email=',
                            dest='email',
                            nargs=1,
                            help='Specify email address.')
        parser.add_argument('--password=',
                            dest='password',
                            nargs=1,
                            help='Specify password required for login.')
        parser.add_argument('--user=',
                            dest='user',
                            nargs=1,
                            help='Specify user (Only required for Netflix).')

        # Assign command line arguments to class variable
        self.args = parser.parse_args()

if __name__ == "__main__":
    extractor = ActivityExtractor()
    extractor.run()
