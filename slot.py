import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import smtplib

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(<your gmail id>, <password>)    # Enter your account details to allow the bot to send notification emails via this account
receiver_ids = [ <receiver id(s)> ]          # Enter the email id to which you wish to send the notification. Ex : ["xyz@gmail.com", "abc@gmail.com"]

def init_browser():
	global browser
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('--ignore-ssl-errors')
	chrome_options.add_argument('--use-fake-ui-for-media-stream')
	chrome_options.add_experimental_option('prefs', {
	    'credentials_enable_service': False,
	    'profile.default_content_setting_values.media_stream_mic': 1,
	    'profile.default_content_setting_values.media_stream_camera': 1,
	    'profile.default_content_setting_values.geolocation': 1,
	    'profile.default_content_setting_values.notifications': 1,
	    'profile': {
	        'password_manager_enabled': False
	    }
	})
	chrome_options.add_argument('--no-sandbox')

	chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

	browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

def send_mail(pin):
	server.sendmail( <your gmail id> , receiver_ids, "There is a slot for booking vaccine at pincode " + str(pin) + ". Please visit quickly!")   # Enter your details
	print("Email sent!")

def isAvailable(pin):
	ele = browser.find_elements_by_xpath("//div[@class='vaccine-box vaccine-box1 vaccine-padding']");
	found = 0
	for e in ele:
		sub = e.find_elements_by_tag_name("a")[0]
		if(sub.text not in ["Booked", "NA"]):
			found = 1
			break;

	if(found==1):
		print("Slot found!")
		send_mail(pin)

def get_slots(pin, age):
	age = "Age " + str(age) + "+"

	ele = browser.find_elements_by_xpath("//div[@class='mat-tab-label-content']");
	for e in ele:
		if e.text == "Search by PIN":
			ele = e
			break
	ele.click()

	pinCode_box = browser.find_element_by_id('mat-input-0')
	pinCode_box.send_keys(pin)

	#submit_button = browser.findelement('Search')
	ele = browser.find_elements_by_tag_name("button")
	for e in ele:
		if e.text == "Search":
			ele = e
			break
	ele.click()

	time.sleep(2)
	ele = browser.find_elements_by_tag_name("label")
	for e in ele:
		if e.text == age:
			ele = e
			break
	ele.click()
	time.sleep(1)
	isAvailable(pin)
	pinCode_box.clear()
init_browser()
#%%

cowin_website = 'https://www.cowin.gov.in/'   # Cowin website  

pin_codes = [ "<Enter you pin codes>" ]       # Example : ['678001', '678020']

age = 18   				      # Desired age group

#%%
browser.get(cowin_website)
while(1):
	print("==== Checking for slots ====")
	for pin in pin_codes:
		get_slots(pin, age)
	browser.get(cowin_website)
	time.sleep(300)     # Check after every 5 minutes (300 secs)

server.quit()
