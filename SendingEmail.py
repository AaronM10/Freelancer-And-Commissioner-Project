import smtplib
from email.message import EmailMessage

class SendingEmailsClass():
    
    #Done so that the account is logged in before at the start of the program. this prevents delays when sending emails as in the previous function
    #The function logged in when the code was beign sent (which caused a dealy inbetween frames which made it seem very unresponsive), so to reduce the time it takes to send the email and teh tranisition between the frames. 
    #Function just connects to the server
    def __init__(self) -> None:
        self.server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        self.server.ehlo()
        self.server.starttls()
        self.senderEmail = "ComputingProjectAlerts@outlook.com"
        self.SenderEmailPassword = "############"
        self.LogginIntoEmailAccount()
        
    #Logs into the account
    def LogginIntoEmailAccount(self):
        self.server.login(self.senderEmail,self.SenderEmailPassword)
    
    #The function that takes in a subject, body and recipient and sends the email to that person
    def SendingActualEmail(self, Subject,Content,reciever):
        CodeEmail = EmailMessage()
        CodeEmail['subject'] = Subject
        CodeEmail.set_content(Content)
        self.server.sendmail(self.senderEmail, reciever, CodeEmail.as_string())
        
        
