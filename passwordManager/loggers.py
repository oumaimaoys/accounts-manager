from mattermostdriver import Driver
import gitlab
from minio import Minio

# an abstract class that has abstract methods for an abstract platform

class Logger(): #an abstract logger
    def __init__(self, token, url):
        self.platform_api_token = token
        self.platform_api_url = url

        def create_user( email, user_name, name, password):
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
    def __init__(self) -> None:
        super().__init__()
        self.drivar = Driver({'url':self.platform_api_url,'token':self.platform_api_token})
        self.drivar.login()

    def create_user(self, email, user_name, password):
        super()
        user_data = {'email': email, 'username': user_name,'password':password}
        try:
            user = self.drivar.users.create_user(user_data)
            return user
        except:
            return "user creation failed"
    
    def rmeove_user(self,id):
        return self.drivar.users.deactivate_user(id)
    
    def view_users(self):
        return self.drivar.users.get_users()


class MinioLogger(Logger):
    def __init__(self) -> None:
        super().__init__()

    def create_user(self):
        pass
    def rmeove_user(self):
        pass
    def view_users(self):
        pass

class HarborLogger(Logger):
    def __init__(self) -> None:
        super().__init__()

    def create_user(self):
        pass
    def rmeove_user(self):
        pass
    def view_users(self):
        pass

    
gitlab = GitlabLogger("uPSVENLpMwJdC3sRLfJN",'http://gitlab.sys.infodat.com')
mattermost = MatterMostLogger("", "https://mattermost.sys.infodat.com/")

#gitlab.create_user(email= 'user_test@exxpress.ma',user_name='user_test',name='user test',password='Agadir414$')
mattermost.create_user(email= 'user_test@exxpress.ma',user_name='user_test',password='Agadir414$')