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
    platform_api_token = "glpat-UP8JuX_AnW5LYD-baBzr"
    platform_api_url = "https://gitlab.com/" # make sure ot change this later


    gl = gitlab.Gitlab(private_token=platform_api_token)

    # create account
    def create_user(self):
        gl = gitlab.Gitlab(private_token=self.platform_api_token)
        user_data = {'email': 'capswarlock@gmail.com', 'username': 'mohamed.hilali', 'name': 'mohamedhilali ','password':'pASSword2433__'}
        #user = gl.users.create(user_data)
        access_token = gl.groups.get(71022580).access_tokens.create({"name": "test", "scopes": ["api"],"expires_at" : "2023-09-01",})
        print( access_token)
    # addd user to group
    # grant access to user 

new = GitlabLogger()

new.create_user()