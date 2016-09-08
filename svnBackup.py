#!/usr/bin/python
from datetime import datetime
import subprocess
import ftplib
import os
import stat

class FtpUploadTracker:
    sizeWritten = 0
    lastshownpercent = 0

    def __init__(self, totalsize):
        self.totalSize = totalsize

    def handle(self, block):
        self.sizeWritten += 1024
        percentcomplete = round((self.sizeWritten / self.totalSize) * 100)
        if self.lastshownpercent != percentcomplete:
            self.lastshownpercent = percentcomplete
            print(str(percentcomplete) + " percent complete")

if __name__ == "__main__":
    time = datetime.now().strftime('%Y-%m-%d_%H:%M:%S_Backup')

    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    # Actually we should put file into a floder
    rel_path = time
    abs_file_path = os.path.join(script_dir, rel_path)

    commandStr = "svnadmin dump /your/svn/Repo/abs/path > " + abs_file_path
    return_code = subprocess.call(commandStr, shell=True)

    if return_code == 0:
        print "success\n"

        st = os.stat(abs_file_path)
        os.chmod(abs_file_path, stat.S_IRWXO | stat.S_IEXEC)

        if not os.access(abs_file_path, os.W_OK):
            print "SerialLinkMan: Write access not permitted on %s" % abs_file_path
        else:
            filetotalsize = os.path.getsize(abs_file_path)
            print "filetotalsize ->" + str(filetotalsize)

            filename = time
            ftp = ftplib.FTP(“*.*.*.*”)
            ftp.login(“yourusername”, “password”)
            ftp.cwd("/home/yourusername/“)
            uploadTracker = FtpUploadTracker(int(filetotalsize))
            with open(abs_file_path, 'rb') as ftpup:
                ftp.storbinary("STOR " + filename, ftpup, 1024, uploadTracker.handle)
                ftp.close()
    else:
        print "fail"
