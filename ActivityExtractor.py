#!/usr/bin/python3

from selenium import webdriver
from amazon import AmazonActivityExtractor
from hulu import HuluActivityExtractor
from netflix import NetflixActivityExtractor
from configparser import ConfigParser
import getopt
import sys


class ActivityExtractor:
    def __init__(self, service, email, password, user):
        self.service = service.lower()
        self.email = email
        self.password = password
        self.user = user

        self.chrome_args = None
        self.url = None

        self.serviceClass = None

        self.supported_services = {
            'amazon': AmazonActivityExtractor,
            'hulu': HuluActivityExtractor,
            'netflix': NetflixActivityExtractor}

    def run(self):
        self.checkService()
        self.getCredentials()
        self.checkCredentials()
        self.runProcess()

    def checkService(self):
        supported = False
        for service in self.supported_services:
            if self.service == service:
                supported = True

        if not supported:
            print('Service not supported')
            print('Supported services include:')
            for s in self.supported_services.keys():
                print('  %s' % s)
            sys.exit(2)

    def getCredentials(self):
        # Initialising the parser
        parser = ConfigParser()
        parser.read('userconfig.ini')
        parser.optionxform = str

        # User credentials parsing dictionary
        parsingDictionary = {'service': self.service.upper()}

        # Chrome parsing dictionary
        chromeParsingDictionary = {'service': 'CHROME'}

        # Potential chrome options obtained from arguments variable
        raw_chrome_args = parser.get(chromeParsingDictionary['service'], 'arguments')
        if raw_chrome_args.strip() != '':
            self.chrome_args = self.parseChromeArgs(raw_chrome_args)

        # Get url for browser
        self.url = parser.get(parsingDictionary['service'], 'url')

        if self.email is None:
            self.email = parser.get(parsingDictionary['service'], 'email')

        if self.password is None:
            self.password = parser.get(parsingDictionary['service'], 'password')

        # Netflix has an extra parameter for profile_name
        if self.service == 'netflix':
            self.user = parser.get(parsingDictionary['service'], 'profile_name')

    def parseChromeArgs(self, args):
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

    def checkCredentials(self):
        if self.email is None:
            print('--email is missing\n'
                  + 'add email into \'userconfig.ini\''
                  + 'or provide email using --email')
            sys.exit(2)
        if self.password is None:
            print('--password is missing\n'
                  + 'add password into \'userconfig.ini\''
                  + 'or provide password using --password')
            sys.exit(2)

    def runProcess(self):
        self.serviceClass = self.supported_services[self.service]({
            'url': self.url,
            'email': self.email,
            'password': self.password,
            'chrome_args': self.chrome_args,
            'user': self.user})

        self.serviceClass.getActivity()

usageOptions = [
    '-h, --help',
    '-s, --service',
    '-e, --email',
    '-p, --password',
    '-u, --user'
]

usageDescriptions = [
    'Show help.',
    'Specify streaming service to get viewing activity from.',
    'Specify email address.',
    'Specify password required for login.',
    'Specify user (Only required for Netflix)',
]


def displayUsage():
    print('\nUsage:\n  python activityextractor.py [options]')
    print('\nGeneral Options:')
    for option, desc in zip(usageOptions, usageDescriptions):
        if len(desc) > 50:
            print('  '
                  + option
                  + ' ' * (28 - len(option))
                  + desc[:49].strip())
            print(' ' * 30
                  + desc[49:].strip())
        else:
            print('  '
                  + option
                  + ' '*(28-len(option))
                  + desc)


def main(argv):
    # Get arguments passed on command line
    try:
        opts, args = getopt.getopt(argv, 's:e:p:u:h', ['service=', 'email=', 'password=','user=', 'help'])
    except getopt.GetoptError:
        displayUsage()
        sys.exit(2)

    service = None
    email = None
    password = None
    user = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            displayUsage()
            sys.exit(2)
        elif opt in ('s', '--service'):
            service = arg
        elif opt in ('-e', '--email'):
            email = arg
        elif opt in ('-p', '--password'):
            password = arg
        elif opt in ('-u', '--user'):
            user = arg
        else:
            displayUsage()
            sys.exit(2)

    if service is not None:
        extractor = ActivityExtractor(service, email, password, user)
    else:
        print('--service is missing')
        sys.exit(2)

    extractor.run()


if __name__ == "__main__":
    main(sys.argv[1:])
