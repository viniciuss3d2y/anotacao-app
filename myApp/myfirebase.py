import requests
from kivy.app import App



class MyFireBase():

    my_api_key = 'AIzaSyDDsBujluz56nLTDmIDC9IFttBGv8zW0Kc'
    
    def criar_conta(self, email, senha):
        meu_aplicativo = App.get_running_app()
        pagina_login = meu_aplicativo.root.ids["loginpage"]

        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post("https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyDDsBujluz56nLTDmIDC9IFttBGv8zW0Kc",
                                   json = info)
        requisicao_dic = requisicao.json()


        if requisicao.ok:
            
            self.local_id = requisicao_dic['localId']
            self.id_token = requisicao_dic['idToken']
            refresh_token = requisicao_dic['refreshToken']
            
            requisicao_id = requests.get(f"https://myappteste-ed27f-default-rtdb.firebaseio.com/id_proximo_usuario.json?auth={self.id_token}")
            id_donovo_usuario = requisicao_id.json()

            id_proximo_usuario = int(id_donovo_usuario) + 1 
            requests.patch(f"https://myappteste-ed27f-default-rtdb.firebaseio.com/.json?auth={self.id_token}", 
                           json={"id_proximo_usuario": id_proximo_usuario})
                 
            
            with open("refreshtoken.txt", 'w') as arquivo:
                arquivo.write(refresh_token)

            info_new_user = {"anotacoes":"","avatar": "foto0.png",
                              "id_usuario": id_donovo_usuario}           
            print(requisicao_dic)
            r = requests.patch(f"https://myappteste-ed27f-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}",
                               json=info_new_user)
            
            
            meu_aplicativo.local_id = self.local_id
            meu_aplicativo.id_token = self.id_token
            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.carregar_id_usuario()
            meu_aplicativo.mudar_tela("homepage")
                               
        else:
            pagina_login.ids["mensagem_login"].text = requisicao_dic['error']['message']
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)

    

    def fazer_login(self, email, senha):
        meu_aplicativo = App.get_running_app()

        info = {"email":email, 
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.my_api_key}", 
                                   json = info)
        requisicao_dic = requisicao.json()
        print(requisicao_dic)
        if requisicao.ok:

            meu_aplicativo.local_id = requisicao_dic['localId']
            meu_aplicativo.id_token = requisicao_dic['idToken']
            
            
            with open("refreshtoken.txt", "w") as refresh_token:
                refresh_token.write(requisicao_dic['refreshToken'])

            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.carregar_id_usuario()
            meu_aplicativo.mudar_tela("homepage")
            
        else:
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = requisicao_dic['error']['message']
            pagina_login.ids["mensagem_login"].color = 1, 0, 0, 1

    
    def trocar_token(self):
        meu_aplicativo = App.get_running_app()
        try:
            with open("refreshtoken.txt", "r") as arquivo:
                refresh_token = arquivo.read()

            info = {"grant_type":  "refresh_token",
                    "refresh_token": refresh_token}
            requisicao = requests.post(f"https://securetoken.googleapis.com/v1/token?key={self.my_api_key}",
                                       json= info)
            requisicao_dic = requisicao.json()

            

            if requisicao.ok:
                meu_aplicativo.local_id = requisicao_dic['user_id']
                meu_aplicativo.id_token = requisicao_dic['id_token']

                meu_aplicativo.mudar_tela("homepage")
           

        except:
            pass

    
    def logout(self):

        meu_aplicativo = App.get_running_app()
        foto_perfil = meu_aplicativo.root.ids["foto_perfil"]
        foto_perfil.source = "icones/fotos_perfil/foto0.png"

        with open("refreshtoken.txt", "w") as refresh_token:
            refresh_token.write("")

        pagina_login = meu_aplicativo.root.ids["loginpage"]
        input_senha = pagina_login.ids["senha_input"]
        input_email = pagina_login.ids["email_input"]
        input_senha.text = ""
        input_email.text = ""


        meu_aplicativo.mudar_tela("loginpage")

        