from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from botoes import LabelButton, ImageButton
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.uix.label import Label



class pop_up(GridLayout):
    def __init__(self):
        super().__init__()
        self.rows = 1
       
        
        self.size_hint = 0.44, 0.38
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        with self.canvas:
            Color(rgba=(226/255, 239/255, 238/255, 0.3))
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos= self.atualizar_popup, size=self.atualizar_popup)

        
        botoes = FloatLayout()

        self.botao1 = LabelButton(text  = "Não", pos_hint = {"right": 0.4 , "top":0.5},
                                            size_hint= (0.23, 0.32), font_size = '12sp', bold = True,
                                            on_release = self.tirar_popup)  
        with self.botao1.canvas.before:
            #Color(rgb=(0, 0, 0 ,1))
            self.rect_bt1 = Rectangle(pos=self.botao1.pos, size=self.botao1.size, source = "icones/botao.png")       
        self.botao1.bind(pos=self.atualizar_botao1, size = self.atualizar_botao1)
       
             

        self.botao2 = LabelButton(text  = "Sim", pos_hint = {"right": 0.85 , "top":0.5},
                                   size_hint= (0.23, 0.32), font_size = '12sp', bold = True,
                                   on_release = self.teste)
        with self.botao2.canvas.before:
            #Color(rgba=(0, 0, 0, 1))
            self.rect_bt2 = Rectangle(pos=self.botao2.pos, size=self.botao2.size, source = "icones/botao.png")
        self.botao2.bind(pos=self.atualizar_botao2, size=self.atualizar_botao2)

        self.label = Label(text = "",  pos_hint = {"center_x": 0.5 , "top":1},
                                   size_hint= (1, 0.5), font_size = '12sp',
                                   text_size=(150, None), markup = True)
        

            
        
        botoes.add_widget(self.botao1)
        botoes.add_widget(self.botao2) 
        botoes.add_widget(self.label)    
        
        self.add_widget(botoes)


    def atualizar_popup(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def atualizar_botao1(self, *args):
        self.rect_bt1.pos = self.botao1.pos
        self.rect_bt1.size = self.botao1.size
    
    def atualizar_botao2(self, *args):
        self.rect_bt2.pos = self.botao2.pos
        self.rect_bt2.size = self.botao2.size


    def teste(self, *args):
        print('dasdfsa')

    def tirar_popup(self, *args):
              
        meu_aplicativo = App.get_running_app()
        pagina_lista_anotacoes = meu_aplicativo.root.ids["listaanotacoespage"]
        floatlayout_popup = pagina_lista_anotacoes.ids["float_popup"]

        for widget in list(floatlayout_popup.children):
            floatlayout_popup.remove_widget(widget)