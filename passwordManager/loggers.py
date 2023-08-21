import gitlab
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
        url = self.platform_api_url
        headers = {
            "Authorization": "Bearer "+ self.platform_api_token,
            "Content-Type": "application/json"
        }
        data = {
            "username": user_name,
            "password": password,
            "email": email
        }
        response = requests.post(url, headers=headers, json=data)
        try:
            return response.content
        except:
            return response.content
    
    def remove_user(self,id, status): #status = boolean
        url = self.platform_api_url + '/' + id +"/active"
        headers = {
            "Authorization": "Bearer "+ self.platform_api_token,
            "Content-Type": "application/json"
        }

        data = {
                "active":  status
                }

        try:
            response = requests.put(url, headers=headers, json=data)
            return response.content
        except:
            return response.content
    
    def get_users(self):
        url = self.platform_api_url
        headers = {
            "Authorization": "Bearer "+ self.platform_api_token,
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
        url = self.platform_api_url
        username = self.login_id
        password = self.password
        headers = {
            "Content-Type": "application/json"
        }
        data ={
            "username": user_name,
            "email": email, 
            "password": password, 
            "realname": name, 
        }
        try:
            response = requests.post(url, headers=headers,auth=(username, password), json=data)
            return response.content
        except:
            return response.content 

    def remove_user(self, id):
        url = self.platform_api_url +"/"+ id
        username = self.login_id
        password = self.password

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
        url = self.platform_api_url
        username = self.login_id
        password = self.password

        headers = {
            "Content-Type": "application/json"
        }
        data ={}
        try:
            response = requests.get(url, headers=headers,auth=(username, password), json=data)
            return response.content
        except:
            return response.content 
