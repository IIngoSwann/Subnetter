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
    parser.add_argument('-d', type = str, dest = 'domain', help = "Local domain name, only used with --hosts (test.local)", required = False, default = '')
    args = parser.parse_args()
    return args.input, args.mask, args.output, args.hosts, args.domain

def fileCheckAndRead(input_file):
    if not os.path.isfile(input_file): #Checks to see if the input_file exists in the folder being searched.
        print ("File does not exist!")
        exit()
    with open(input_file, 'r') as myFile: 
        fileData = [line.rstrip('\n') for line in myFile] # Takes the data from myFile line by line, removes the '\n' from the end of each entry and then puts it into an array containing either IP addresses
                                                          # or Host Names.
    filteredData = list(filter(lambda x: x != "", fileData))
    return filteredData

def hostsCheck(fileData, hosts, domain):
    addresses = []
    if hosts: # If the '--hosts' argument is used (denoting that the input file is a list of host names and not IP addresses).
        for i in fileData: # Loops through all of the lines in fileData.
            try:
                singleAddress = hostNameToIPAddress(i, domain) # Gets a single address from a single host name.
                addresses.append(singleAddress) # Adds the resulting IP address to the list called addresses.
            except Exception as e:
                print(f"Failed to resolve {i}") # If the script is unable to resolve an IP from a host name then it throws an error printing out the host name.
                print(e)
    else: 
        addresses = fileData
    return addresses

def hostNameToIPAddress(hostName, domain): # This does resolving of the IP from the host.
    if domain == "":
        IPAddy = socket.gethostbyname(hostName)
    else:
        IPAddy = socket.gethostbyname(hostName + '.' + domain)
    return IPAddy

def subnetMaskingAndDuplicateRemoval(addresses, subnetmask):
    mylist = [] # 'mylist' is the final list of masked IP addresses that is either printed to the screen or written to an output file.
    try:
        for i in addresses: # Loops through all of the IPs in the addresses list
            splitip = i.split(".") # At i in addresses split the address by the periods it contain. Worth noting that 'splitip' is actually an array with a length of 4.
            if not subnetmask: # If the default subnet mask is used.
                splitip[3] = '0/24'
            else:
                splitip[2] = '0'
                splitip[3] = '0/16'
            splitip[0 : 4] = ['.'.join(splitip[0 : 4])] # Joins indexes 0-4 (don't really know why its 0 - 4 when the array only has elements in indexes 0 - 3, but I digress) together and then adds a period
                                                        # between each index, making it a complete IP address and now split IP only has one element and its under the index 0.
            toAdd = splitip[0]
            mylist.append(toAdd)
        mylist = list(set(mylist)) #Removal of duplicates.

        return mylist
    except:
        print ("There was an error when masking IP addresses, input file may contain host names... try \'--host\'.")
        exit()

def writeToOutputFile(mylist, output_file):
    if output_file: # If the user wants to write to a designated output file
        with open(output_file, 'w') as out:
            out.write("\n".join(mylist))
        print('Output has been written to a file.')
    else:
        print("Masking complete... results are shown below.\n")
        for x in mylist:
            print(x)

def main():
    input_file, subnetmask, output_file, hosts, domain = getinfo()

    fileData = fileCheckAndRead(input_file)

    addresses = hostsCheck(fileData, hosts, domain)

    mylist = subnetMaskingAndDuplicateRemoval(addresses, subnetmask)

    mylist.sort() 

    writeToOutputFile(mylist, output_file)

if __name__ == "__main__":
    main()
