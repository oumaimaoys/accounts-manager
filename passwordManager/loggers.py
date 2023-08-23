import gitlab
import requests
from bmc import *
import datetime as dt

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
            return user
        except Exception as e:
            print(f"user failed to be created: {e}")
        
    def block_user(self, id, user_name): # blocking them
        if id:
            user = self.gl.users.get(id) # by id       
        elif user_name:
            user = self.gl.users.list(username=user_name)[0]
        else:
            raise ValueError
        user.block()

    def unblock_user(self, user_id, user_name): # blocking them
        if user_id:
            user = self.gl.users.get(user_id) # by id       
        elif user_name:
            user = self.gl.users.list(username=user_name)[0]
        else:
            raise ValueError
        user.unblock()

    def update_user(self):
        pass

    def view_users(self):
        return self.gl.users.list(get_all=True)
    

class MatterMostLogger(Logger):
    def __init__(self,token, url, id, password):
        super().__init__(token, url, id, password)

    def create_user(self, email, user_name, password,name):
        data = {
            "username": user_name,
            "password": password,
            "email": email
        }
        try: 
            return self.make_request(method="post",endpoint="", data=data )
        except Exception as e:
            print(f"user failed to be created: {e}")
    
    def block_user(self,id,user_name): #status = boolean
        endpoint = '/' + str(id) +"/active"
        data = { "active":  False}

        return self.make_request(method="put", endpoint=endpoint, data= data)
    def delete_user(self, id):
        pass
    
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
        try:
            return user.content
        except Exception as e:
            print(f"user failed to be created: {e}")

        
    def block_user(self,id, user_name): # disable user
        user = admin_user_disable(target='infodat', username=user_name)
        return user.content
    
    def enable_user(self, user_name):
        user = admin_user_enable(target='infodat', username=user_name)
        return user.content
        
    def remove_user(self, user_name):
        user = admin_user_remove(target="infodat",username=user_name)
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
        try:
            return self.make_request(method="post",endpoint="", data=data )
        except Exception as e:
            print(f"user failed to be created: {e}")

    def block_user(self, id, user_name): #removes it but not permanently
        endpoint = "/"+ str(id)
        return self.make_request(method="delete",endpoint=endpoint, data={} )

    def get_users(self):
        return self.make_request(method="get", endpoint="", data={})


minio = MinioLogger(token="", url="https://minio-s3.sys.infodat.com", id="GwmN8IbR2PCq1pDJ", password="VvHVl2UuQ8JKYE5LKs50gzqnfFVvMH3o")
#print(minio.create_user(email="",user_name="new_user23",password="Agadir414$",name=""))
#print(minio.disable_user(user_name="new_user23"))
#print(minio.remove_user("new_user23"))
#print(minio.get_users())

g = GitlabLogger(token="uPSVENLpMwJdC3sRLfJN", url="http://gitlab.sys.infodat.com", id="", password="")
m = MatterMostLogger(token="74yg6ftb13dgfbbaq88y8kdk6c", url="https://mattermost.sys.infodat.com/api/v4/users", id="", password="")
h = HarborLogger(token="", url="https://harbor.conacom.net/api/v2.0/users", id="sadik.sajid", password="Liefero414$$")

#print(g.create_user(email="new.user@infodat.ma",user_name="new.user", name="new user", password="passwordtemp123"))
#user = g.gl.users.get(27)
#user.confirmed_at = str(dt.date.today())
#user.save()



#print(g.gl.users.delete(id=30))
#print(m.get_users())
#m.block_user(id="4y3wshgmptdz3r4hzjrsryk3uy",user_name="")

#print(h.block_user(id=13, user_name=""))
#print(h.get_users())

