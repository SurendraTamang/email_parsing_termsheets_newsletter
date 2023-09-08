
import email
import imaplib

import os
import mimetypes


GMAIL_IMAP_HOST = 'imap.gmail.com'
gmail_user = os.environ.get('gmail_user')
gmail_pass = os.environ.get('gmail_pass')



def main(gmail_user, gmail_pass):
    username= gmail_user
    password= gmail_pass
    mail= imaplib.IMAP4_SSL(GMAIL_IMAP_HOST)


    mail.login(username, password)
    mail.select("inbox")

    # TODO : Filteration of emails to be done here

    result, data= mail.uid('search',None,"ALL")
    print("Creating")
    #breakpoint()
    # list of messages in code
    inbox_item_list=data[0].split()

    # recent
    most_recent=inbox_item_list[-1]


    oldest=inbox_item_list[0]


    for item in inbox_item_list:

        # standard format
        result2, email_data=mail.uid('fetch',item,'RFC822')

        # decoding
        raw_email=email_data[0][1].decode("utf-8")
        email_message=email.message_from_string(raw_email)

        to_=email_message['To']
        from_=email_message['From']
        subject_=email_message['Subject']
        date_=email_message['date']
        counter=1
        for part in email_message.walk():
            if part.get_content_maintype()=="multipart":
                continue

            filename= part.get_filename()
            content_type=part.get_content_type()
            if not filename:
                ext=mimetypes.guess_extension(part.get_content_type())
                if not ext:
                    ext='.bin'
                filename='msg-part-%08d%s' %(counter, ext)
            counter +=1
    
        save_path=os.path.join(os.getcwd(),"emails")
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with open(os.path.join(save_path,filename),'wb') as fp:
            fp.write(part.get_payload(decode=True))

if __name__ == '__main__':
    print("Starting")
    main(gmail_user, gmail_pass)