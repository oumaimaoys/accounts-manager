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
    platform_api_token = "glpat-wtAzNm4yqvrwGmDUsXGc"
    platform_api_url = "https://gitlab.example.com/" # make sure ot change this later