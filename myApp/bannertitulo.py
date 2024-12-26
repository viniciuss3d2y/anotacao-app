from botoes import LabelButton, ImageButton
import requests
from kivy.app import App
from functools import partial
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.image import Image
from pop_up import pop_up





class Titulo(GridLayout):
    def __init__(self,**kwargs):
        self.rows= 1
        super().__init__()
        138, 234, 223, 1
        with self.canvas.before:#50, 255, 201, 1
            Color(rgba=(50/255, 225/255, 201/255, 1))
            self.rect = Rectangle(size = self.size, pos = self.pos)
        
        self.bind(pos=self.atualizar_rect, size=self.atualizar_rect)

        self.titulo = kwargs['titulo']

        label = LabelButton(text = self.titulo, on_release = partial(self.carregar_anotacoes_usuario, self.titulo),
                             font_size="30sp", text_size=(200, None), halign='center',
                            font_name = "fonts/Pixel_Emulator.otf")
        #label.bind(size=self.ajustar_label_size)
        label.color = (1, 1, 1, 1)#RGB 204, 247, 239, 1
        
        imagem = ImageButton(source = "icones/titulo.png",on_release = partial(self.carregar_anotacoes_usuario, self.titulo),
                             size_hint=(0.5, 0.1), size = (30, 30))
        
        imagem_excluir = ImageButton(source = "icones/lixeira.png", size_hint = (0.12, 0.01), 
                                    on_release = self.pop_up)
                                        
        
        self.add_widget(imagem)
        self.add_widget(label)                                                                  #size_hint = (0.12, 0.01),
        self.add_widget(imagem_excluir)
        for widget in list(self.children):
            widget.font_size = str(widget.width / 10)+"sp"


    def carregar_anotacoes_usuario(self, *args):
         
        meu_aplicativo = App.get_running_app()
        pagina_texto_anotacoes = meu_aplicativo.root.ids["textoanotacoespage"]
        scroll_texto = pagina_texto_anotacoes.ids["texto_anotacoes"]
        for widget in list(scroll_texto.children):
            scroll_texto.remove_widget(widget)
            
        pagina_texto_anotacoes.ids["titulo_dotexto"].text = self.titulo
        pagina_texto_anotacoes.ids["titulo_dotexto"].color = (35/255, 253/255, 147/255, 1)

        requisicao = requests.get(f"https://myappteste-ed27f-default-rtdb.firebaseio.com/{meu_aplicativo.local_id}/anotacoes/{self.titulo}.json?auth={meu_aplicativo.id_token}")
        texto_anotacoes = requisicao.json()

        label = Label(text = texto_anotacoes)
        label.color = (1, 0, 0.98, 1)
        label.bold = True

        scroll_texto.add_widget(label)

        meu_aplicativo.mudar_tela("textoanotacoespage")



        


    def atualizar_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


    def ajustar_label_size(self, label, *args):
        label.font_size = label.width / 10




    def excluir_anotacao(self, titulo, *args):
        meu_aplicativo = App.get_running_app()
        requisicao = requests.delete(f"https://myappteste-ed27f-default-rtdb.firebaseio.com/{meu_aplicativo.local_id}/anotacoes/{titulo}.json?auth={meu_aplicativo.id_token}")


        pagina_lista_anotacoes = meu_aplicativo.root.ids["listaanotacoespage"]
        floatlayout_popup = pagina_lista_anotacoes.ids["float_popup"]
        
        try:
            for widget in list(floatlayout_popup.children):
                floatlayout_popup.remove_widget(widget)
        except:
            pass


        if requisicao.ok:
            print("sucesso meu pa")


            pagina_lista_anotacoes = meu_aplicativo.root.ids["listaanotacoespage"]
            try:
                for widget in list(pagina_lista_anotacoes.ids["lista_anotacoes"].children):
                    pagina_lista_anotacoes.ids["lista_anotacoes"].remove_widget(widget)
        
                requisicao = requests.get(f"https://myappteste-ed27f-default-rtdb.firebaseio.com/{meu_aplicativo.local_id}/anotacoes.json?auth={meu_aplicativo.id_token}")
                requisicao_dic = requisicao.json()

                for titulo in requisicao_dic:
                    banner = Titulo(titulo = titulo)
                    pagina_lista_anotacoes = meu_aplicativo.root.ids["listaanotacoespage"]
                    pagina_lista_anotacoes.ids["lista_anotacoes"].add_widget(banner)
            except:
                pass


        else:
            print("desgraaaaaaaaaaaaaaaaaaaaca")
        
    
    def pop_up(self, *args):
             
        meu_aplicativo = App.get_running_app()
        pagina_lista_anotacoes = meu_aplicativo.root.ids["listaanotacoespage"]
        floatlayout_popup = pagina_lista_anotacoes.ids["float_popup"]
        
        try:
            for widget in list(floatlayout_popup.children):
                floatlayout_popup.remove_widget(widget)
        except:
            pass

        popup = pop_up()
        popup.label.text = f"[color=#131318]Você quer mesmo excluir[/color] [color=#ef30ef]'{self.titulo}'?[/color]"
        popup.botao2.on_release = partial(self.excluir_anotacao, self.titulo)
        #popup.botao2.on_release = 

        floatlayout_popup.add_widget(popup)
