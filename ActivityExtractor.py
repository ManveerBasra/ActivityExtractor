#!/usr/bin/python3

from selenium import webdriver
from amazon import AmazonActivityExtractor
from hulu import HuluActivityExtractor
from netflix import NetflixActivityExtractor
from configparser import ConfigParser
import argparse
import sys


class ActivityExtractor:
    def __init__(self):
        self.args = None

        self.chrome_args = None
        self.url = None

        self.service_class = None

        self.supported_services = {
            'amazon': AmazonActivityExtractor,
            'hulu': HuluActivityExtractor,
            'netflix': NetflixActivityExtractor}

    def run(self):
        self.init_arguments()
        self.check_service()
        self.get_credentials()
        self.check_credentials()
        self.run_process()

    def check_service(self):
        supported = False
        for service in self.supported_services:
            if self.args.service == service:
                supported = True

        if not supported:
            print('Service not supported')
            print('Supported services include:')
            for s in self.supported_services.keys():
                print('  %s' % s)
            sys.exit(2)

    def get_credentials(self):
        # Initialising the parser
        parser = ConfigParser()
        parser.read('userconfig.ini')
        parser.optionxform = str

        # User credentials parsing dictionary
        parsing_dictionary = {'service': self.args.service.upper()}

        # Chrome parsing dictionary
        chrome_parsing_dictionary = {'service': 'CHROME'}

        # Potential chrome options obtained from arguments variable
        raw_chrome_args = parser.get(chrome_parsing_dictionary['service'], 'arguments')
        if raw_chrome_args.strip() != '':
            self.chrome_args = self.parse_chrome_args(raw_chrome_args)

        # Get url for browser
        self.url = parser.get(parsing_dictionary['service'], 'url')

        if self.args.email is None:
            self.args.email = parser.get(parsing_dictionary['service'], 'email')

        if self.args.password is None:
            self.args.password = parser.get(parsing_dictionary['service'], 'password')

        # Netflix has an extra parameter for profile_name
        if self.args.service == 'netflix':
            self.args.user = parser.get(parsing_dictionary['service'], 'profile_name')

    def parse_chrome_args(self, args):
        """
            Breaks up args, adds them to an instance of ChromeOptions and returns the result
            """
        chrome_options = webdriver.ChromeOptions()
        if ',' in args:
            options_list = args.split(',')
            for option in options_list:
                chrome_options.add_argument(option.strip())
        else:
            chrome_options.add_argument(args)

        return chrome_options

    def check_credentials(self):
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
        self.service_class = self.supported_services[self.args.service]({
            'url': self.url,
            'email': self.args.email,
            'password': self.args.password,
            'chrome_args': self.chrome_args,
            'user': self.args.user})

        self.service_class.get_activity()

    def init_arguments(self):
        """
        Initialize command line argument parser and define acceptable arguments
        """
        parser = argparse.ArgumentParser(description='This repository gets viewing activity from user\'s streaming '
                                                     'service accounts.')
        parser.add_argument('service',
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


def main():
    extractor = ActivityExtractor()
    extractor.run()


if __name__ == "__main__":
    main()
