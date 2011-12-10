============================================
 pyafraid, command-line afraid.org DDNS tool
============================================

pyafraid is a command-line tool for updating IP addresses for the afraid.org DDNS service.

Installation
============

``pyafraid`` can be installed using the standard ``easy_install`` command::
 
 $ [sudo] easy_install pyafraid

Alternatively, you can install from a local version using ``setup.py install``::

 $ [sudo] python setup.py install

Usage
=====

Once installed, simply run::

  $ pyafraid update|query <username> -p <password> -n <hostname>


Or, if you'd like to use the SHA-1 hash instead of the
username/password combo::

  $ pyafraid update|query -s <sha_hash> -n <hostname>


For a more detailed usage description, use the ``--help/-h`` option::

 $ pyafraid -h
 Usage: pyafraid.py update|query [-h] [-u <username>] [-p <password>] [-n
 <hostname>]


 Options:
  -h, --help            show this help message and exit
  -u USERNAME, --username=USERNAME
                        The freedns.afraid.org username
  -p PASSWORD, --password=PASSWORD
                        The associated password
  -n HOSTNAME, --hostname=HOSTNAME
                        The name of the host to update or query
  -s SHA_HASH, --sha-hash=SHA_HASH
                        The SHA-1 hash from the API interface
                        URL. Don't use this with the -u and -p options.

For example, to update freedns.afraid.org to point to the current IP address,
use the ``update`` argument::

 $ pyafraid update -u myuser -p mypass -n mythbox.example.org
   Attempting to update mythbox.example.org...
   response from server:
   ERROR: Address 1.1.1.1 has not changed. 


To query freedns.afraid.org for information about an account, you can use the ``query`` argument::

 $ pyafraid query -u myuser -p mypass

  url:    http://freedns.afraid.org/dynamic/update.php?<some_hash>
  ip:     1.1.1.1
  desc:   example.org
 
  url:    http://freedns.afraid.org/dynamic/update.php?<some_other_hash>
  ip:     2.2.2.2
  desc:   deathstar.example.org


Note that specifying ``-n/--hostname`` will restrict the output to the given host.


Usage Requirements
==================

pyafraid has only been actively tested on python 2.6, but should work with minor changes on python 2.2+.
Patches are welcomed :)


Development Requirements
=========================

In order to execute unit tests (using 'make test') the following modules are required:
    * unittest2
    * discover
    * mock

All of these modules can be installed with ``easy_install``::

 $ [sudo] easy_install mock unittest2 discover


Reporting Bugs
==============

Any bugs can be reported on github (https://github.com/campbellr/pyafraid/issues/new)
or emailed to campbellr@gmail.com.

