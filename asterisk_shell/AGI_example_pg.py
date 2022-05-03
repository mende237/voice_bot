#!/usr/bin/env python
#
# An example for AGI (Asterisk Gateway Interface).
#
# Answer a call. Retrieve an account number from the caller and play back
# some account information to the caller.
#
# Developed for "Asterisk: The Definitive Guide"
#
import sys
#
# AGI commands are written to stdout. After a command is processed,
# the response from Asterisk comes in via stdin.
#

def agi_command(cmd):
    '''Write out the command and return the response'''
    # print sends the command out to stdout.
    print(cmd)
    # Make sure it doesn't get buffered.
    sys.stdout.flush()
    # Read the response line from stdin. Use strip() to remove any whitespace
    # that may be present (primarily the line ending).
    return sys.stdin.readline().strip()
#
# Read the AGI environment variables sent from Asterisk to the script
# at startup. The input looks like:
#   agi_request: example1.py
#   agi_channel: SIP/000FF2266EE4-00000009
#
...
#
# After this bit of code you will be able to retrieve this information as:
#   asterisk_env['agi_request']
#   asterisk_env['agi_channel']
#
asterisk_env = {}
while True:
    line = sys.stdin.readline().strip()
    if not len(line):
        break
    var_name, var_value = line.split(':', 1)
    asterisk_env[var_name] = var_value
#
# Set up a fake "database" of accounts. In a more realistic AGI script
# that is doing account data lookup, you would connect out to an external
# database or some other API to get this information. For the purpose of
# this example, we'll skip that and do the data lookup from this local
# example set.
#
ACCOUNTS = {
'12345678': {'balance': '50'},
'11223344': {'balance': '10'},
'87654321': {'balance': '100'},
}
#
# Answer the call using the ANSWER AGI command.
#
# See: *CLI> agi show commands topic ANSWER
#
response = agi_command('ANSWER')
#
# Prompt the caller to enter an account number using the GET DATA command.
#   - Play a prompt called please-enter-account-number
#   - Set a timeout of 30 seconds
#   - Read a maximum of 8 digits (our account numbers are 8 digits long)
#
# See: *CLI> agi show commands topic GET DATA
#
response = agi_command('GET DATA please-enter-account-number 30000 8')
#
# If a timeout occurred, just exit back to the dialplan.
#
# The response will look like:
#   200 result=<digits> (timeout)
#
if 'timeout' in response:
    sys.exit(0)
#
# The response will look like:
#   200 result=<digits>
# digits will be -1 if an error occurred.
#
# Split the response on the '=', a maximum of 1 time. The result is a two
# element array. The second element in the array (index 1) is the part that
# came after the '=' and is the account number we want.
#
account = response.split('=', 1)[1]
#
# If an error occurred, just hang up.
#
# See: *CLI> agi show commands topic HANGUP
#
if account == '-1':
    response = agi_command('HANGUP')
    sys.exit(0)
# If the account is invalid, tell the caller and then exit to the dialplan.
#
# See: *CLI> agi show commands topic STREAM FILE
#
if account not in ACCOUNTS:
    response = agi_command('STREAM FILE invalid-account ""')
    sys.exit(0)
balance = ACCOUNTS[account]['balance']

#
# Tell the caller the balance and then exit back to the dialplan.
#
# See: *CLI> agi show commands topic SAY NUMBER
#
response = agi_command('STREAM FILE your-balance-is ""')
response = agi_command('SAY NUMBER %s ""' % (balance))
sys.exit(0)