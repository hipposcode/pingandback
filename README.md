# pingandback

This does the equivalent of ping hostname to get an IPaddress and then a ping -a IPaddress to see if DNS and IPaddress match up

Open a file called hosts.txt, ping the host and if it fails write the output to results(date and time).txt.  If it succeeds write the hosts name, good ping reply, the IPaddress of the host and a hostname lookup of the IPaddress or an error message if the lookups fail.
