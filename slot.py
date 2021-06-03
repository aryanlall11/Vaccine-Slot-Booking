import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import smtplib

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(<your gmail id>, <password>)    # Enter your account details to allow the bot to send notification emails via this account

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
	server.sendmail("suchitralall8@gmail.com", ["aryanlall53@gmail.com", "lallbimal@gmail.com"], "There is a slot for booking vaccine at pincode " + str(pin) + ". Please visit quickly!")
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
	#age = browser.find_element(By.PARTIAL_LINK_TEXT, 'Age 18+')
	ele = browser.find_elements_by_tag_name("label")
	for e in ele:
		if e.text == age:
			ele = e
			break
	ele.click()
	time.sleep(1)
	isAvailable(pin)
	pinCode_box.clear()
#%%

init_browser()

browser.get('https://www.cowin.gov.in/')

pin_codes = ['800001', '800020']

while(1):
	print("==== Checking for slots ====")
	for pin in pin_codes:
		get_slots(pin, 18)
	browser.get('https://www.cowin.gov.in/')
	time.sleep(300)

server.quit()
