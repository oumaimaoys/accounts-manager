from mattermostdriver import Driver
import gitlab
from minio import Minio
from harborapi import HarborAsyncClient

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
    def __init__(self, token, url):
        super().__init__()
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
        self.driver = Driver({'url':self.platform_api_url, 'token':self.platform_api_token})
        self.driver.login()

    def create_user(self, email, user_name, password):
        super()
        user_data = {'email': email, 'username': user_name,'password':password}
        try:
            user = self.drivar.users.create_user(user_data)
            return user
        except:
            return "user creation failed"
    
    def rmeove_user(self,id):
        return self.driver.users.deactivate_user(id)
    
    def view_users(self):
        return self.driver.users.get_users()


class MinioLogger(Logger):
    def __init__(self,token, url, id, password) -> None:
        super().__init__(token, url, id, password)

    def create_user(self):
        pass
    def remove_user(self):
        pass
    def view_users(self):
        pass

class HarborLogger(Logger):
    def __init__(self,token, url, id, password) -> None:
        super().__init__(token, url, id, password)
        self.client = HarborAsyncClient(url=self.platform_api_url,basicauth=self.platform_api_token )

    def create_user(self,email, user_name, name, password):
        user_data = {'email': email, 'username': user_name,'password':password}
        user = self.client.create_user(user_data)
        return(user)

    def rmeove_user(self):
        pass
    def view_users(self):
        return self.client.get_users()

# for testing   : delete later
#gitlab = GitlabLogger("uPSVENLpMwJdC3sRLfJN",'http://gitlab.sys.infodat.com')
mattermost = MatterMostLogger(token ="", url = "mattermost.sys.infodat.com",id="",password="")
#harbor = HarborLogger("","")

#gitlab.create_user(email= 'user_test@exxpress.ma',user_name='user_test',name='user test',password='Agadir414$')
print(mattermost.view_users())
#print(mattermost.create_user(email= 'user_test@exxpress.ma',user_name='user_test',password='Agadir414$'))
#print(harbor.create_user(email= 'user_test@exxpress.ma',user_name='user_test',password='Agadir414$'))