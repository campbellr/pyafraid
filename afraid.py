#!/usr/bin/env python
""" This script updates the the afraid.org DDNS server to point to the
    the new current public IP address.
"""
import urllib2
import optparse
import sys
import pprint

import texttable

try:
    from hashlib import sha1
except ImportError: # python < 2.5
    from sha import new as sha1

API_URL = "http://freedns.afraid.org/api/?action=getdyndns&sha="

def error(msg, code=1):
    print >> sys.stderr, "%s: error: %s" % (sys.argv[0], msg)
    sys.exit(code)

def validate_args(parser, options, args):
    if len(args) != 1:
        parser.error("Incorrect number of arguments.")

    action= args[0]

    if action.lower() == "update":
        required_options = ['username', 'password', 'hostname']
    elif action.lower() == "query":
        required_options = ['username', 'password']
    else:
        parser.error("Either 'update' or 'query' must be provided.")

    for required_opt in required_options:
        if not getattr(options, required_opt, None):
            parser.error("The --%s option must be provided." % required_opt)

def parse_args():
    parser = optparse.OptionParser(usage="%prog update|query [-h] [-u <username>] [-p <password>] [-n <hostname>]")
    parser.add_option('-u', '--username', help="The freedns.afraid.org username",
                      dest="username", default=None)
    parser.add_option('-p', '--password', help="The associated password",
                      dest='password', default=None)
    parser.add_option('-n', '--hostname', help="The name of the host to update or query",
                       dest='hostname', default=None)

    options, args = parser.parse_args()
    validate_args(parser, options, args)

    return options, args[0]

def get_sha(username, password):
    to_hash = "|".join([username, password])
    return sha1(to_hash).hexdigest()

def parse_ascii_api(s):
    keys = ('desc', 'ip', 'url')
    records = []
    for record_str in s.splitlines():
        if record_str.strip():
            records.append(dict(zip(keys, record_str.split('|'))))

    return records

def get_records(sha_hash):
    url = API_URL + sha_hash
    f = urllib2.urlopen(url)
    #TODO: handle invalid hash
    result = f.read()
    records = parse_ascii_api(result)
    return records

# TODO: handle errors
def update_url(record):
    print "Attempting to update %s..." % record['desc']
    f = urllib2.urlopen(record['url'])
    result = f.read()
    print "response from server:\n %s" % result

# TODO: this should really be a method of some Records class...
def get_record_by_desc(records, desc):
    for record in records:
        if record['desc'] == desc:
            return record

    error("No record with description '%s'" % desc)

def perform_update(opts):
    sha_hash = get_sha(opts.username, opts.password)
    records = get_records(sha_hash)
    record = get_record_by_desc(records, opts.hostname)
    update_url(record)

def print_record(record):
    for key, value in record.iteritems():
        print "%s:\t%s" % (key, value)

    print "\n",

def print_results(records):
    if not isinstance(records, list):
        records = [records]

    print "\n",
    for record in records:
        print_record(record)


def perform_query(opts):
    sha_hash = get_sha(opts.username, opts.password)
    result = get_records(sha_hash)
    if opts.hostname:
        result = get_record_by_desc(result, opts.hostname)

    print_results(result)

def perform_action(action, opts):
    if action == "query":
        perform_query(opts)
    elif action == "update":
        perform_update(opts)

def main():
    opts, action = parse_args()
    perform_action(action, opts)

if __name__ == "__main__":
    main()
