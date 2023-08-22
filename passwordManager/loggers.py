import gitlab
import requests
from bmc import *

# an abstract class that has abstract methods for an abstract platform

class Logger(): #an abstract logger
    def __init__(self, token, url, id, password):
        self.platform_api_token = token
        self.platform_api_url = url
        self.login_id = id
        self.password = password

    def make_request(self, method, endpoint, data):
        headers = {
            "Content-Type": "application/json"
        }
        if self.platform_api_token != "":
            headers["Authorization"] =  "Bearer " + self.platform_api_token
            auth= None
        else :
            auth= (self.login_id, self.password)
        
        url = self.platform_api_url + endpoint
        
        try:
            if method == 'get':
                response = requests.get(url, headers=headers, json=data, auth=auth)
            elif method == 'post':
                response = requests.post(url, headers=headers, json=data, auth=auth)
            elif method == 'put':
                response = requests.put(url, headers=headers, json=data, auth=auth)
            elif method == 'delete':
                response = requests.delete(url, headers=headers, json=data, auth=auth)
            else:
                raise ValueError("Invalid HTTP method")

            response.raise_for_status()  
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None


class GitlabLogger(Logger):
    def __init__(self, token, url, id , password):
        super().__init__(token, url, id , password)
        self.gl = gitlab.Gitlab(url=self.platform_api_url, private_token=self.platform_api_token)

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
    

class MatterMostLogger(Logger):
    def __init__(self,token, url, id, password):
        super().__init__(token, url, id, password)

    def create_user(self, email, user_name, password):
        data = {
            "username": user_name,
            "password": password,
            "email": email
        }
        return self.make_request(method="post",endpoint="", data=data )
    
    def remove_user(self,id, status): #status = boolean
        endpoint = '/' + id +"/active"
        data = { "active":  status}

        return self.make_request(method="put", endpoint=endpoint, data= data)
    
    def get_users(self):
        return self.make_request(method="get", endpoint="", data= {})

class MinioLogger(Logger):
    def __init__(self,token, url, id, password) -> None:
        super().__init__(token, url, id, password)
        self.r = config_host_add(
                alias='infodat',
                url=self.platform_api_url,
                username=self.login_id,
                password= self.password,
                )


    def create_user(self, email, user_name, password, name):
        user = admin_user_add(target='infodat', username=user_name, password=password)
        return user.content

        
    def disable_user(self, user_name):
        user = admin_user_disable(target='infodat', username=user_name)
        return user.content
    
    def enable_user(self, user_name):
        user = admin_user_enable(target='infodat', username=user_name)
        return user.content
        
    def get_users(self):
        users = admin_user_list(target='infodat')
        return users.content


class HarborLogger(Logger):
    def __init__(self,token, url, id, password) -> None:
        super().__init__(token, url, id, password)
   

    def create_user(self,email, user_name, name, password):
        data ={
            "username": user_name,
            "email": email, 
            "password": password, 
            "realname": name, 
        }
        return self.make_request(method="post",endpoint="", data=data )

    def remove_user(self, id):
        endpoint = "/"+ id
        return self.make_request(method="delete",endpoint=endpoint, data={} )

    def get_users(self):
        return self.make_request(method="get", endpoint="", data={})

"""
minio = MinioLogger(token="", url="https://minio-s3.sys.infodat.com", id="GwmN8IbR2PCq1pDJ", password="VvHVl2UuQ8JKYE5LKs50gzqnfFVvMH3o")
#print(minio.create_user(email="",user_name="new_user23",password="Agadir414$",name=""))
print(minio.disable_user(user_name="new_user23"))"""