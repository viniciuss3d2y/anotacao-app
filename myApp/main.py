from kivy.app import App
from kivy.lang import Builder
from telas import HomePage
from botoes import LabelButton, ImageButton
import os
from functools import partial
import requests
from myfirebase import MyFireBase
from bannertitulo import Titulo
import time
from kivy.animation import Animation
import traceback



GUI = Builder.load_file("main.kv")
class MainApp(App):
    local_id = None
    id_token = None
    myfirebase = MyFireBase()
    
    def build(self):
        return GUI
    
    def on_start(self):

        self.myfirebase.trocar_token()
        self.carregar_infos_usuario()
        self.carregar_id_usuario()
        
    def mudar_tela(self, id_tela):
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.current = id_tela

# carregar as fotos de perfil disponiveis quando o usuario entra na pagina
    def carregar_fotos_perfil(self):
        
        pagina_fotos_perfil = self.root.ids["fotosperfilpage"]
        lista_fotos_perfil = pagina_fotos_perfil.ids["lista_fotos_perfil"]

        for widget in list(lista_fotos_perfil.children):
            lista_fotos_perfil.remove_widget(widget)

        arquivos_fotos_perfil = os.listdir("icones/fotos_perfil")
        
        for arquivo in arquivos_fotos_perfil:
            imagem = ImageButton(source = f"icones/fotos_perfil/{arquivo}",
                                 on_release = partial(self.mudar_foto_perfil, arquivo))
            lista_fotos_perfil.add_widget(imagem)

        self.mudar_tela("fotosperfilpage")


    def mudar_foto_perfil(self, arquivo, *args):

        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{arquivo}"

        info = {"avatar":arquivo}
        requests.patch(f"https://myappteste-ed27f-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}",
                       json = info)
        

        self.mudar_tela("homepage")


    def carregar_avatar_usuario(self):
        try:
            requisicao = requests.get(f"https://myappteste-ed27f-default-rtdb.firebaseio.com/{self.local_id}/avatar")


        except:
            pass

    def carregar_infos_usuario(self):
        try:
            # carregar foto do usuario do banco de dados
            requisicao = requests.get(f"https://myappteste-ed27f-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}")
            requisicao_dic = requisicao.json()
            avatar = requisicao_dic['avatar']
            foto_perfil = self.root.ids["foto_perfil"]
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"
        except:
            traceback.print_exc()
            pass

    
    def salvar_anotacoes(self, titulo, anotacao):
        pagina_anotacoes = self.root.ids["anotacoespage"]
        input_titulo = pagina_anotacoes.ids["titulo_input"]
        input_dotexto = pagina_anotacoes.ids["anotacoes_input"]
        info = {titulo : anotacao}

        nova_cor = ( 255/255, 18/255, 0/255, 0.1)  # Vermelho

        if len(titulo) <= 74:
            if input_dotexto.text != "" and input_titulo != "":
                requisicao = requests.patch(f"https://myappteste-ed27f-default-rtdb.firebaseio.com/{self.local_id}/anotacoes.json?auth={self.id_token}", 
                                        json= info)
                print(self.local_id)
                if requisicao.ok:
                    # input_titulo.text = ""
                    # input_dotexto.text = ""
                    self.carregar_titulos_usuario()
        else:
            cor_original_titulo = input_titulo.background_color
            anim_input_titulo = Animation(background_color=nova_cor, duration = 0.5)+ Animation(background_color=cor_original_titulo, duration = 0.001)
            anim_input_titulo.start(input_titulo)
        
        if input_titulo.text == "":
            cor_original_titulo = input_titulo.background_color
            anim_input_titulo = Animation(background_color=nova_cor, duration = 0.5)+ Animation(background_color=cor_original_titulo, duration = 0.001)
            anim_input_titulo.start(input_titulo)

        if input_dotexto.text == "":
            cor_original_text = input_dotexto.background_color
            anim_input_text = Animation(background_color=nova_cor, duration=0.5)+Animation(background_color=cor_original_text, duration = 0.001)           
            anim_input_text.start(input_dotexto)

        
    
    def carregar_titulos_usuario(self):
        pagina_lista_anotacoes = self.root.ids["listaanotacoespage"]
        try:
            for widget in list(pagina_lista_anotacoes.ids["lista_anotacoes"].children):
                pagina_lista_anotacoes.ids["lista_anotacoes"].remove_widget(widget)
       
            requisicao = requests.get(f"https://myappteste-ed27f-default-rtdb.firebaseio.com/{self.local_id}/anotacoes.json?auth={self.id_token}")
            requisicao_dic = requisicao.json()
            print(requisicao_dic)

            for titulo in requisicao_dic:
                banner = Titulo(titulo = titulo)
                #pagina_lista_anotacoes = self.root.ids["listaanotacoespage"]
                pagina_lista_anotacoes.ids["lista_anotacoes"].add_widget(banner)
        except:
            traceback.print_exc()
            pass
        self.mudar_tela("listaanotacoespage")       


    def carregar_id_usuario(self):
        try:
            requisicao = requests.get(f"https://myappteste-ed27f-default-rtdb.firebaseio.com/{self.local_id}/id_usuario.json?auth={self.id_token}")
            self.id_usuario = requisicao.json()
            homepage = self.root.ids["homepage"]
            homepage.ids["label_id"].text = f"[color=#161173]Seu Id Único :[/color][color=#5F9D9D] {self.id_usuario}[/color]"
        except:
            traceback.print_exc()
            pass
    
    
    def olho_senha(self):
        pagina_login = self.root.ids["loginpage"]
        labelbutton_olho = pagina_login.ids["olho_senha"]
        input_senha = pagina_login.ids["senha_input"]

        if labelbutton_olho.source == "icones/olho.png":
            labelbutton_olho.source = "icones/olho_fechado.png"
            input_senha.password = False

        else:
            labelbutton_olho.source = "icones/olho.png"
            input_senha.password = True
    



MainApp().run()