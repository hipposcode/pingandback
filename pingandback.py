import subprocess
import datetime
import socket


def ping(hostname):
    p = subprocess.Popen('ping ' + hostname, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pingStatus = 'ok'
    for line in p.stdout:
        output = line.rstrip().decode('UTF-8', 'ignore')
        if (output.endswith('unreachable.')):
            # No route from the local system. Packets sent were never put on the wire.
            pingStatus = 'unreacheable'
            break
        elif (output.startswith('Ping request could not find host')):
            pingStatus = 'host_not_found'
            break
        if (output.startswith('Request timed out.')):
            # No Echo Reply messages were received within the default time of 1 second.
            pingStatus = 'timed_out'
            break
            # end if
    # endFor
    return pingStatus
# endDef

def printPingResult(hostname):
    statusOfPing = ping(hostname)
    if (statusOfPing == 'host_not_found'):
        outputfile.write(hostname + ',not found' + "\n")
    elif (statusOfPing == 'unreacheable'):
        outputfile.write(hostname + ',unreachable' + "\n")
    elif (statusOfPing == 'timed_out'):
        outputfile.write(hostname + ',timed out' + "\n")
    elif (statusOfPing == 'ok'):
        try:
            ipaddress = socket.gethostbyname(hostname)
            reverselookuphostname = socket.gethostbyaddr(ipaddress)
            outputtuple = (hostname, "good ping reply", ipaddress, reverselookuphostname[0])
            outputline = str(outputtuple)
            outputfile.write(outputline + "\n")
        except (socket.gaierror, socket.herror):
            outputfile.write(hostname + ", address related error/other error" + "\n")
        # endIf
# endPing

count = 1
outputfilename = ("pbresults" + datetime.datetime.now().strftime("%Y%m%d%H%M") + ".txt")
inputfile = open("hosts.txt")
outputfile = open(outputfilename, "w")
try:
    for item in inputfile:
        printPingResult(item.strip())
        print (count)
        count = count+1
        # endFor
finally:
    inputfile.close()
    outputfile.close()
