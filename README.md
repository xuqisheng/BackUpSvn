# BackUpSvn
back up svn use python.
dump svn to a file ,and send the file to ftp server.

1.set up a ftp server .

you should test your ftp server,before run this script.

2.crontab execute python file 

// give permission

chmod a+x /svnBackup.py

// run it at 1:10,Thursday

10 1 * * 4 /usr/bin/python /home/svnBackup.py

