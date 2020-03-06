subnetter.py
====================
# Description #
Input a list of either IP addresses or host names. If the input text file contains IP addresses, the script masks them appropriately with either a 16 or a 24 subnet mask. If the input text file contains hosts names, it first resolves IP addresses from the host names and then masks them. After masking is
completed the script can either write the masked addresses to the screen or write them to a <name>.txt
file.

## Install ##
Download to your machine with git clone

## Usage #
usage: Project.py [-h] -i INPUT [-16] [--hosts] [-o OUTPUT] [-d DOMAIN]

  -h, --help  show this help message and exit
  -i INPUT    Name of input file containing IP addresses.
  -16         Switches subnetmask from 24 to 16
  --hosts     Flag denoting that the input file contains host names rather
              than IP addresses.
  -o OUTPUT   Write to output file.
  -d DOMAIN   Local domain name, only used with --hosts (test.local)