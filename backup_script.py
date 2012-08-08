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

import imaplib
import email
import os

print('Connection to GMail...')
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('therubikscubekid@gmail.com', 'uxlkryn425')
print('Retrieving emails...')
mail.select('Turbo')

detach_dir = '.'

typ, data = mail.search(None, 'ALL')
for num in data[0].split():
	typ, data = mail.fetch(num, '(RFC822)')
	
	newmail = email.message_from_string(data[0][1])
	
#	email = email.message_from_string(data[0][1])

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
            		fp.close()



	#print 'Message %s\n%s\n' % (num, data[0][1])

type, data = mail.fetch(1, '(RFC822)')
#print 'Message %s\n\%s\n' % (1, email.message_from_string(data[0][1]))
#print 'Message %s\n%s\n' % (1, data[0][1])

#email = email.message_from_string(data[0][1])

#print email






#print message

mail.close()
mail.logout()
