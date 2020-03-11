import unittest
import time
from flask import url_for
from urllib.request import urlopen
from os import getenv
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from application import app, db, bcrypt
from application.models import Users


test_admin_first_name = "admin"
test_admin_last_name = "admin"
test_admin_email = "admin@email.com"
test_admin_password = "admin2020"


class TestBase(LiveServerTestCase):

	def create_app(self):
		app.config['SQLACHEMY_DATABASE_URI'] = str(getenv('TEST_DATABASE'))
		app.config['SECRET_KEY'] = getenv('SKEY')
		return app

	def setUp(self):
		print("--------next-test----------")
		chrome_options = Options()
		chrome_options.binary_location ="/usr/bin/google-chrome-stable"
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--no-sandbox")
		chrome_options.add_argument("disable-gpu")
		chrome_options.add_argument("window-size=1920,1080")
		chrome_options.add_argument("disable-dev-shm-usage")
		chrome_options.add_argument("disable-features=VizDisplayCompostior")
		self.driver = webdriver.Chrome(executable_path="/home/adam301093/chromedriver", chrome_options=chrome_options)
		self.driver.get("http://localhost:5000")
		db.session.commit()
		db.drop_all()
		db.create_all()

	def tearDown(self):
		self.driver.quit()
		print("--------------------End-Of-Test---------------------------\n\n\n------------------------Unit-And-Selenium-Tests-------------------")


	def test_server_is_up_and_running(self):
		response = urlopen("http://localhost:5000")
		self.assertEqual(response.code, 200)

class TestRegistration(TestBase):

	def test_registration(self):
		"""
		Test that a user can create an account using the registration form
        	if all fields are filled out correctly, and that they will be 
		redirected to the login page
		"""

		# Click register menu link
		self.driver.find_element_by_xpath("/html/body/div[1]/a[4]").click()
		time.sleep(1)

		# Fill in registration form
		self.driver.find_element_by_xpath('/html/body/div[2]/form/div[3]/input').send_keys(
			test_admin_email)
		self.driver.find_element_by_xpath('/html/body/div[2]/form/div[1]/input').send_keys(
			test_admin_first_name)
		self.driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/input').send_keys(
			test_admin_last_name)
		self.driver.find_element_by_xpath('/html/body/div[2]/form/div[4]/input').send_keys(
			test_admin_password)
		self.driver.find_element_by_xpath('/html/body/div[2]/form/div[5]/input').send_keys(
			test_admin_password)
		self.driver.find_element_by_xpath('/html/body/div[2]/form/div[6]/input').click()
		time.sleep(1)

		# Assert that browser redirects to login page
		assert url_for('login') in self.driver.current_url


if __name__ == '__main__':
	unittest.main(port=5000)

