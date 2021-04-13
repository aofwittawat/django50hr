#################ส่งเมลล์ภาษาไทย########################
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendthai(sendto,subj="ทดสอบส่งเมลลล์",detail="สวัสดี!\nคุณสบายดีไหม?\n"):

	myemail = 'uncle.django50@gmail.com'
	mypassword = "c0'Fdh50"
	receiver = sendto

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subj
	msg['From'] = 'Admin EAFOREXQUANT'
	msg['To'] = receiver
	text = detail

	part1 = MIMEText(text, 'plain')
	msg.attach(part1)

	s = smtplib.SMTP('smtp.gmail.com:587')
	s.ehlo()
	s.starttls()

	s.login(myemail, mypassword)
	s.sendmail(myemail, receiver.split(','), msg.as_string())
	s.quit()


###########Start sending#############
subject = 'ยืนยันการสมัครเวปไซต์ซื้อ EA ของ EAFOREXQUANT'
newmember_name = 'สมชาย'
content = '''เนื่องจากทางด้านความปลอดภัย กรุณายืนยันผ่านลิ้งด้านล่างนี้'''
link = 'http://eaforexquant.com/confirm/dddddddddddddddddd'

msg = 'สวัสดีครับ {} \n\n {}{} \n verify link: {}'.format(newmember_name,content,link)


sendthai('aofwittawat@gmail.com,wittawatb@g.swu.ac.th',subject,msg)