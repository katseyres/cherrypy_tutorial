import cherrypy
import base64
import json


class Main(object):
    @cherrypy.expose
    def index(self, *args, **kwargs):
        print(args, kwargs)
        
        if kwargs:
            if kwargs['action'] == 'create':
                return Main.RegisterPage(self, kwargs['username'], kwargs['password'])
            elif kwargs['action'] == 'connect':
                if Main.DecodeAndCheck(kwargs['username'], kwargs['password']):
                    return Main.ConnectionPage(self, kwargs['username'])
                
                return "Wrong connection"
        
        return Main.HomePage(self)

    @cherrypy.expose
    def HomePage(self):
        with open('View/homePage.html', 'r') as f:
            raw_html = f.read()
        
        return raw_html

    @cherrypy.expose
    def ConnectionPage(self, username):
        with open('View/connectionPage.html', 'r') as f:
            raw_html = f.read()
        
        return raw_html

    @cherrypy.expose
    def RegisterPage(self, username, password):
        Main.EncodeAndSave(username, password)

        with open('View/registeredPage.html', 'r') as f:
            raw_html = f.read()
        
        return raw_html
    
    def EncodeAndSave(username, password):
        encoded_username = base64.b64encode(username.encode())
        encoded_password = base64.b64encode(password.encode())

        with open('Data/login.json', 'r') as f:
            user_database = f.read()
        
        user_list:list = json.loads(user_database)
        user_list.append({"user": encoded_username.decode(), "password": encoded_password.decode()})

        while len(user_list) > 2:
            user_list.pop(0)

        with open('Data/login.json', 'w') as f:
            json.dump(user_list, f, indent=3)
        
        return True

    def DecodeAndCheck(username, password):
        with open('Data/login.json', 'r') as f:
            user_database = f.read()
        
        user_list:list = json.loads(user_database)

        username = base64.b64encode(username.encode()).decode()
        password = base64.b64encode(password.encode()).decode()
        
        for user in user_list:
            if username == user['user']:
                if  password == user['password']:
                    return True
        
        return False

    
if __name__ == '__main__':
    cherrypy.quickstart(Main())
