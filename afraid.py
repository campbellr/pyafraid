#!/bin/env python
""" This script updates the the afraid.org DDNS server to point to the
    the new current public IP address.
"""
import urllib2
import optparse
import sys
import pprint

try:
    from hashlib import sha1
except ImportError: # python < 2.5
    from sha import new as sha1

API_URL = "http://freedns.afraid.org/api/?action=getdyndns&sha="

def error(msg, code=1):
    print >> sys.stderr, "%s: error: %s" % (sys.argv[0], msg)
    sys.exit(code)

def parse_args():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--username', help="The freedns.afraid.org username",
                      dest="username", default=None)
    parser.add_option('-p', '--password', help="The associated password",
                      dest='password', default=None)
    parser.add_option('-n', '--hostname', help="The name of the host to update",
                       dest='hostname', default=None)

    options, args = parser.parse_args()
    for required_opt in ['username', 'password', 'hostname']:
        if not getattr(options, required_opt, None):
            error("the --%s option must be provided." % required_opt)

    return options

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

def main():
    opts = parse_args()
    sha_hash = get_sha(opts.username, opts.password)
    records = get_records(sha_hash)
    record = get_record_by_desc(records, opts.hostname)
    print "record: %s" % pprint.pformat(record)
    #update_url(record)

if __name__ == "__main__":
    main()
