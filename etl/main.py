from etl import truncate_and_etl


def send_email():
    from email.mime.text import MIMEText
    from phila_mail import server

    recipientslist = ['peter.dannemann@Phila.gov', 
                      'dani.interrante@phila.gov', 
                      'philip.ribbens@phila.gov',
                      'shannon.holm@phila.gov']
    sender = 'peter.dannemann@phila.gov'
    commaspace = ', '
    email = 'PERMIT in GISLNICLD failed to update properly and may be missing rows or empty. This table supports the permit-plan-form application. Please stand by for updates.'
    text = f'AUTOMATIC EMAIL: \n {email}'
    msg = MIMEText(text)
    msg['To'] = commaspace.join(recipientslist)
    msg['From'] = sender
    msg['X-Priority'] = '2'
    msg['Subject'] = 'Important Email'
    server.server.sendmail(sender, recipientslist, msg.as_string())
    server.server.quit()

def main():
    truncate_and_etl()
    try:
        truncate_and_etl()
    except:
        send_email()

if __name__ == '__main__':
    main()