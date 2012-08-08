# TurboScan Backup
# 
# This script is designed to create nightly backups of all the
# documents a user scans into their iPhone using the TurboScan 
# application.
#
# This app works by connecting to a users gmail account and then
# pulling all of the emails in a specified directory. These emails
# are then scanned for all emails sent by the TurboScan app
# (determined by special tags in the subject line), downloaded,
# and the image attachments are sent to a server for safe keeping.
#
# For more information, view the README document.

import imaplib
import email
import os
import sys


###### Variables ######
turbo_label = 'Turbo'
detach_dir = '.'
#######################

## 
#	This method attempts to make a connection to http://gmail.com using the
#	username and password provided via command line arguments
##
def connect(username, password):
	print('Connecting to GMail...')
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login(username, password)
	print('Retrieving emails...')
	mail.select(turbo_label)


	numDownloaded = 0

	typ, data = mail.search(None, 'UNSEEN')
	for num in data[0].split():
		typ, data = mail.fetch(num, '(RFC822)')
	
		newmail = email.message_from_string(data[0][1])

		for part in newmail.walk():
        		if part.get_content_maintype() == 'multipart':
            			continue
	        	if part.get('Content-Disposition') is None:
        			continue
			filename = part.get_filename()
			counter = 1
	        	if not filename:
        			filename = 'part-%03d%s' % (counter, 'bin')
		        	counter += 1
        		att_path = os.path.join(detach_dir, filename)
        		if not os.path.isfile(att_path) :
            			fp = open(att_path, 'wb')
            			fp.write(part.get_payload(decode=True))
				numDownloaded += 1
            			fp.close()

	print "Downloaded %s email attachments" % numDownloaded

	mail.close()
	mail.logout()

##
#	The main method. Accepts the command line arguments of -username -password
#	and displays a usage statement if the wrong number of arguments is given
##
def main():
	print "length: %s" % len(sys.argv)
	if( len(sys.argv) != 3 ):
		print "usage: turbo-scan-backup -username@gmail.com -password"
	else:
		username = sys.argv[1]
		password = sys.argv[2]
		connect(username, password)

# Runs the main() method first
if __name__ == "__main__":
    main()
