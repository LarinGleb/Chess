
import os
import smtplib                
from email.mime.text import MIMEText                      
from email.mime.multipart import MIMEMultipart
PORT = 587
SERVER = "smtp.gmail.com"
USER, PASSWORD = open(os.path.dirname(__file__) + "/Settings.txt", "r").read().split("\n")
def SendMail(Addr: str, code: str):
    msg = MIMEMultipart()                                  
    msg['From']    = USER                     
    msg['To']      = Addr        
    msg['Subject'] = "Protocol"   
    body = f"Your code: {code}"
    msg.attach(MIMEText(body, 'plain'))         
    server = smtplib.SMTP(SERVER, PORT)       
    server.starttls()                          
    server.login(USER, PASSWORD)    
    server.send_message(msg)
    server.quit()  
