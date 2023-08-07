from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import gitlab


# an abstract class that has abstract methods for an abstract platform

class Logger(): #an abstract logger
    platform_api_url = ""
    platform_api_token = ""
    platform_sign_up_url = ""


    def create_account_with_scrapper(self):
        pass

    def create_account_with_api(self):
        pass


class GitlabLogger(Logger):
    platform_api_token = "uPSVENLpMwJdC3sRLfJN"
    platform_api_url = 'https://gitlab.sys.infodat.com'

    # create account
    def create_user(self):
        gl = gitlab.Gitlab(url=self.platform_api_url, private_token=self.platform_api_token)
        user_data = {'email': 'user_test@exxpress.ma', 'username': 'user_test', 'name': 'user test','password':'Agadir414$'}
        #user = gl.users.create(user_data) # create new user
        #gl.users.delete(id=)
        #print(gl.users.list())

    
    

new = GitlabLogger()

new.create_user()