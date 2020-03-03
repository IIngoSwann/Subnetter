#!/usr/bin/env python3
#Created by: Markus Constantino
import argparse
import os
import socket

def getinfo():
    parser = argparse.ArgumentParser(description="Used to parse subnets.", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-i', type = str, dest = 'input', help = 'Name of input file containing IP addresses.', required = True)
    parser.add_argument('-16', action = 'store_true', dest = 'mask', help = 'Switches subnetmask from 24 to 16', required = False)
    parser.add_argument('--hosts', action = 'store_true', dest = 'hosts', help = 'Flag denoting that the input file contains host names rather than IP addresses.', required = False)
    parser.add_argument('-o', type = str, dest = 'output', help = 'Write to output file.', required = False)
    args = parser.parse_args()
    return args.input, args.mask, args.output, args.hosts
    
def hostNameToIPAddress(hostName):
    IPAddy = socket.gethostbyname(hostName)
    return IPAddy

def main():
    input_file, subnetmask, output_file, hosts = getinfo() #Need to add hosts
    if not os.path.isfile(input_file):
        print ("File does not exist!")
        exit()
    with open(input_file, 'r') as myFile:  
        fileData = [line.rstrip('\n') for line in myFile]
    mylist = []
    addresses = []

    if hosts:
        for i in fileData:
            try:
                singleAddress = hostNameToIPAddress(i)
                addresses.append(singleAddress)
            except:
                print(f"Failed to resolve {i}")
    else:
        addresses = fileData

    for i in addresses:
        splitip = i.split(".")
        if not subnetmask:
            splitip[3] = '0/24'
        else:
            splitip[2] = '0'
            splitip[3] = '0/16'
        splitip[0 : 4] = ['.'.join(splitip[0 : 4])]
        toAdd = splitip[0]
        mylist.append(toAdd)
    #This gets rid of any duplicates
    mylist = list(set(mylist))

    if output_file:
        with open(output_file, 'w') as out:
            out.writelines(mylist)
        print('Output has been written to a file.')
    else:
        for x in mylist:
            print(x)

if __name__ == "__main__":
    main()