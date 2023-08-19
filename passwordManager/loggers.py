import gitlab
import subprocess
import requests

# an abstract class that has abstract methods for an abstract platform

class Logger(): #an abstract logger
    def __init__(self, token, url, id, password):
        self.platform_api_token = token
        self.platform_api_url = url
        self.login_id = id
        self.password = password

    def create_user(self,email, user_name, name, password):
        #here we validate the data
        pass


class GitlabLogger(Logger):
    def __init__(self, token, url, id , password):
        super().__init__(token, url, id , password)
        self.gl = gitlab.Gitlab(url=self.platform_api_url, private_token=self.platform_api_token)

    # create account
    def create_user(self, email, user_name, name, password):
        user_data = {'email': email, 'username': user_name, 'name': name,'password':password}
        try:
            user = self.gl.users.create(user_data) 
        except : # defien error messages for each variabels
            print("user failed to be created")
        #gl.users.delete(id=24)

    def remove_user(self, user_id, user_name): # blocking them
        if user_id:
            user = self.gl.users.get(user_id) # by id       
        elif user_name:
            user = self.gl.users.list(username=user_name)[0]
        else:
            raise ValueError
        user.block()

    def update_user(self):
        pass

    def view_users(self):
        return self.gl.users.list(get_all=True)
    
    def get_token_expiration_date(self):
        access_tokens = self.gl.personal_access_tokens.list()
        #for token in access_tokens:
            #if token.token == self.platform_api_token:
                #return access_tokens[1].expires_at
        return(access_tokens[2])


class MatterMostLogger(Logger):
    def __init__(self,token, url, id, password):
        super().__init__(token, url, id, password)

    def create_user(self, email, user_name, password):
        super()
        url = "https://mattermost.sys.infodat.com/api/v4/users"
        headers = {
            "Authorization": "Bearer 74yg6ftb13dgfbbaq88y8kdk6c",
            "Content-Type": "application/json"
        }
        data = {
            "username": "newuser3",
            "password": "Agadir414$",
            "email": "newuser3@example.com"
        }
        response = requests.post(url, headers=headers, json=data)
        try:
            return response.content
        except:
            return response.content
    
    def remove_user(self,id):
        url = "https://mattermost.sys.infodat.com/api/v4/users/jqdfyuqozidm5n1oyqc6jbh3ba/active"
        headers = {
            "Authorization": "Bearer 74yg6ftb13dgfbbaq88y8kdk6c",
            "Content-Type": "application/json"
        }

        data = {
                "active":  False
                }

        try:
            response = requests.put(url, headers=headers, json=data)
            return response.content
        except:
            return response.content
    
    def get_users(self):
        url = "https://mattermost.sys.infodat.com/api/v4/users"
        headers = {
            "Authorization": "Bearer 74yg6ftb13dgfbbaq88y8kdk6c",
            "Content-Type": "application/json"
        }
        data ={}
        try:
            response = requests.get(url, headers=headers, json=data)
            return response.content
        except:
            return response.content

class MinioLogger(Logger):
    def __init__(self,token, url, id, password) -> None:
        super().__init__(token, url, id, password)

    def create_user(self):
        pass
    def remove_user(self):
        pass
    def get_users(self):
        
        pass
class HarborLogger(Logger):
    def __init__(self,token, url, id, password) -> None:
        super().__init__(token, url, id, password)
   

    def create_user(self,email, user_name, name, password):
        url = "https://harbor.conacom.net/api/v2.0/users"
        username = "sadik.sajid"
        password = "Liefero414$$"
        headers = {
            "Content-Type": "application/json"
        }
        data ={
            "username": "test_user12",
            "email": "test_user12e@gmail.com", 
            "password": "Agadir414$", 
            "realname": "test User", 
        }
        try:
            response = requests.post(url, headers=headers,auth=(username, password), json=data)
            return response.content
        except:
            return response.content 

    def remove_user(self):
        url = "https://harbor.conacom.net/api/v2.0/users/11"
        username = "sadik.sajid"
        password = "Liefero414$$"

        headers = {
            "Content-Type": "application/json"
        }
        data ={}
        try:
            response = requests.delete(url, headers=headers,auth=(username, password), json=data)
            return response.content
        except:
            return response.content 

    def get_users(self):
        url = "https://harbor.conacom.net/api/v2.0/users"
        username = "sadik.sajid"
        password = "Liefero414$$"

        headers = {
            "Content-Type": "application/json"
        }
        data ={}
        try:
            response = requests.get(url, headers=headers,auth=(username, password), json=data)
            return response.content
        except:
            return response.content 

# for testing   : delete later
gitlab = GitlabLogger(token = "uPSVENLpMwJdC3sRLfJN",url = 'http://gitlab.sys.infodat.com', id="", password="")
mattermost = MatterMostLogger(token ="gkk", url = "mattermost.sys.infodat.com",id="kgkgk",password="kkgk")
harbor = HarborLogger(token ="", url = "",id="",password="")

#gitlab.create_user(email= 'user_test@exxpress.ma',user_name='user_test',name='user test',password='Agadir414$')
#print(mattermost.remove_user(id=""))
#print(mattermost.get_users())
#print(mattermost.create_user(email= 'user_test@exxpress.ma',user_name='user_test',password='Agadir414$'))
#print(gitlab.get_users())
#print(harbor.create_user(email= '',user_name='',password='', name=""))
print(harbor.remove_user())
print(harbor.get_users())

