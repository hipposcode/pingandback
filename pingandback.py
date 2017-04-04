import subprocess
import datetime
import socket


def ping(hostname):
    p = subprocess.Popen('ping ' + hostname, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pingstatus = 'ok'
    for line in p.stdout:
        output = line.rstrip().decode('UTF-8', 'ignore')
        if output.endswith('unreachable.'):
            # No route from the local system. Packets sent were never put on the wire.
            pingstatus = 'unreacheable'
            break
        elif output.startswith('Ping request could not find host'):
            pingstatus = 'host_not_found'
            break
        if output.startswith('Request timed out.'):
            # No Echo Reply messages were received within the default time of 1 second.
            pingstatus = 'timed_out'
            break
            # end if
    # endFor
    return pingstatus
# endDef

def printPingResult(hostname):
    outputtuple = " "
    statusOfPing = ping(hostname)
    if statusOfPing == 'host_not_found':
        outputfile.write(hostname + ',not found' + "\n")
    elif statusOfPing == 'unreacheable':
        outputfile.write(hostname + ',unreachable' + "\n")
    elif statusOfPing == 'timed_out':
        outputfile.write(hostname + ',timed out' + "\n")
    elif statusOfPing == 'ok':
        try:
            ipaddress = socket.gethostbyname(hostname)
            reverselookuphostname = socket.gethostbyaddr(ipaddress)
            if ".kingsch.nhs.uk" in reverselookuphostname[0]:
                rhostname = (reverselookuphostname[0][:-15])
            else:
                rhostname = reverselookuphostname[0]
            if hostname.lower() == rhostname.lower():
                outputtuple = (hostname, "good ping reply", ipaddress, rhostname)
            else:
                outputtuple = (hostname, "good ping reply - name mismatch", ipaddress, rhostname)
            outputline = str(outputtuple)
            outputfile.write(outputline + "\n")
        except socket.gaierror:
            outputfile.write(hostname + ", no reverse DNS entry" + "\n")
        except socket.herror:
            outputfile.write(hostname + ", host doesn't resolve to IP" + "\n")
        except:
            outputfile.write(hostname + ", something bad happened" + "\n")
        # endIf
    outputfile.flush()
# endPing

count = 1
# outputfilename = ("pbresults - assetstudio - all.txt")
outputfilename = ("pbresults" + datetime.datetime.now().strftime("%Y%m%d - %H%M") + ".txt")
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
