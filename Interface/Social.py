from kivy.app import App

from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

kv = """
<MyWidget>:
    ap: ap

    ActionBar:
        background_color:0, 0, 0, 0.1
        pos_hint: {'top':1}


        ActionView:
            ActionPrevious:
                id: ap
                with_previous: False
                title:"NomeSocial"
                color: 0, 0, 255, 1
                app_icon: 'aven.jpg'



               # markup:True
               # font_size:"16dp"

            ActionButton:
                icon: 'bianco.png'


"""

Builder.load_string(kv)

#caratteristiche predefinite all'immagine
class MyImage(Image):
    def __init__(self, name, *args):
        super(MyImage, self).__init__(*args)
        self.source = name
        self.size_hint =(None, None)
        self.size= (300, 300)
        #self.pos=(self.x+470, self.y+160)
        self.pos_hint = {'x': 0.400, 'y': 0.375}

# caratteristiche predefinite del testo
class MyText(Label):
    def __init__(self, mytext, *args):
        super(MyText, self).__init__(*args)
        self.text = mytext
        self.color=(0,0,0,1)
        self.size_hint = (None, None)
        self.halign='left'

        #self.pos=(self.x+470, self.y+160)
        self.pos_hint = {'x': 0.5, 'y': 0.6}

class ShowComment(Label):
    def __init__(self, string, *args):
        super(ShowComment, self).__init__(*args)
        self.text = string
        self.color =  0, 0, 255, 1
        self.size_hint=(None,None)
        self.pos_hint={'center_x':0.375,'center_y':0}
        self.font_size = '14sp'

    # quando un nuovo commento "string" viene inserito, lo aggiungo
    def add_comment(self, stringa):
        self.text = self.text + "\n" + stringa


#classe per postare una immagine nel layout
class PostImage(FloatLayout):
    def __init__(self, name_img, *args):
        super(PostImage, self).__init__(*args)

        self.add_widget(MyImage(name_img))
        self.add_widget(Button(text="Like", size_hint=(0.04, 0.046), pos_hint={'x': 0.400, 'y': 0.390}, font_size='12sp'))
        self.add_widget(TextInput(text="commenta", multiline=False, size_hint=(0.1, 0.046), pos_hint={'x': 0.440, 'y': 0.390},
                      font_size='14sp'))
        #prova = ShowComment("comm1")
        #self.add_widget(prova)
        #prova.add_comment("comm2")
        #prova.add_comment("comm3")
        #prova.add_comment("sto scrivendo tante parole")

class PostText(FloatLayout):
    def __init__(self, my_text, *args):
        super(PostText, self).__init__(*args)

        self.add_widget(MyText(my_text))
        self.add_widget(Button(text="Like", size_hint=(0.04, 0.046), pos_hint={'center_x': 0.5, 'y': 0.590}, font_size='12sp'))
        self.add_widget(TextInput(text="commenta", multiline=False, size_hint=(0.1, 0.046), pos_hint={'center_x': 0.570, 'y': 0.590},
                      font_size='14sp'))


class MyWidget(FloatLayout):
    def __init__(self, *args):
        super(MyWidget, self).__init__(*args)
        # self.ap.clear_widgets()

        #aggiungo uno sfondo al layout, aggiungengo un rettangolo colorato
        with self.canvas.before:
            Color(255, 255, 255, 1) #bianco
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # listen to size and position changes (aggiorno la posizione del rettangolo colorato/layout)
        self.bind(pos=update_rect, size=update_rect)

        #ricerca utenti
        self.add_widget(TextInput(text='Search users', multiline=False, size_hint=(None, 0.04),
                                  pos_hint={'right': 1, 'y': 0.879}, font_size='12sp'))

        self.add_widget(PostImage("magic.jpg"))
        #self.add_widget(PostText('Text in a very long lineeeeeeeeeeeeeee\nother line'))





class MySocialApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MySocialApp().run()


