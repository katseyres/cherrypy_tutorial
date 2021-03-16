import cherrypy
import base64
import json


class Main(object):
    # index est la première fonction appelée, elle renvoie vers différentes pages en fonction des paramètres passés dans l'url
    # args n'est pas vraiment utilisé, c'est plus kwargs => 127.0.0.1:5000/index?firstname=jhon&lastname=doe
    # firstname et lastname sont des kwargs
    # kwargs est un dictionnaire alors que args est une liste
    @cherrypy.expose
    def index(self, *args, **kwargs):
        print(args, kwargs) 
        
        # s'il y a un paramètre dans l'url
        if kwargs:
            # si la valeur du paramètre 'action' est 'create'
            if kwargs['action'] == 'create':
                # appelle la fonction RegisterPage()
                return Main.RegisterPage(self, kwargs['username'], kwargs['password'])
            elif kwargs['action'] == 'connect':
                # appelle la fonction DecodeAndCheck() pour savoir si elle retourne True
                if Main.DecodeAndCheck(kwargs['username'], kwargs['password']):
                    # appelle ConnectionPage()
                    return Main.ConnectionPage(self, kwargs['username'])
                
                return "Wrong connection"
        
        # si aucun paramètre, appelle HomePage()
        return Main.HomePage(self)

    @cherrypy.expose
    def HomePage(self):
        # lit le fichier 'homePage.html' et le retourne
        with open('View/homePage.html', 'r') as f:
            raw_html = f.read()
        
        return raw_html

    @cherrypy.expose
    def ConnectionPage(self, username):
        # lit le fichier 'connectionPage.html' et le retourne
        with open('View/connectionPage.html', 'r') as f:
            raw_html = f.read()
        
        return raw_html

    @cherrypy.expose
    def RegisterPage(self, username, password):
        # appelle EncodeAndSave()
        Main.EncodeAndSave(username, password)

        # lit le fichier
        with open('View/registeredPage.html', 'r') as f:
            raw_html = f.read()
        
        return raw_html
    
    def EncodeAndSave(username, password):
        # encode le nom d'utilisateur et le mot de passe
        encoded_username = base64.b64encode(username.encode())
        encoded_password = base64.b64encode(password.encode())

        # lit ce qui se trouve dans le fichier 'login.json'
        with open('Data/login.json', 'r') as f:
            user_database = f.read()
        
        # passe de <string> en <list>
        user_list:list = json.loads(user_database)
        # ajoute les paramètres à la liste
        user_list.append({"user": encoded_username.decode(), "password": encoded_password.decode()})

        # pour ne pas avoir 10 000 utilisateurs dans le fichier 'login.json'
        while len(user_list) > 2:
            user_list.pop(0)

        # réécrit dans le fichier 'login.json' avec une architecture (indent=3)
        with open('Data/login.json', 'w') as f:
            json.dump(user_list, f, indent=3)
        
        return True

    def DecodeAndCheck(username, password):
        with open('Data/login.json', 'r') as f:
            user_database = f.read()
        
        user_list:list = json.loads(user_database)

        # encode les paramètres
        username = base64.b64encode(username.encode()).decode()
        password = base64.b64encode(password.encode()).decode()
        
        # compare les paramètres encodés avec ceux dans le fichier 'login.json'
        # s'il correspondent, return True
        for user in user_list:
            if username == user['user']:
                if  password == user['password']:
                    return True
        
        return False

    
if __name__ == '__main__':
    cherrypy.quickstart(Main())
