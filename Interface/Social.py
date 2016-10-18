from kivy.app import App

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import runTouchApp
from kivy.uix.scrollview import ScrollView

from kivy.uix.dropdown import DropDown


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


#contiene il contatore dei like, il bottone dei like, il textinput per i commenti e i commenti inseriti nel textinput
class Counter(FloatLayout):
    def __init__(self, *args):
        super(Counter, self).__init__(*args)

        with self.canvas.before:
            Color(255, 255, 0, 1)  # bianco
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # listen to size and position changes (aggiorno la posizione del rettangolo colorato/layout)
        self.bind(pos=update_rect, size=update_rect)

        self.size_hint=(None, None)
        self.width= 250
        self.height=200


        btn=ImageButton("heartblue.png")
        btn.size_hint=(None,None)
        btn.width = 18
        btn.height= 18
        btn.pos_hint = {'center_x': 0.15, 'top':1}
        btn.on_press = self.btn_pressed
        self.add_widget(btn)

        self.count = 0
        self.like_num=Label(text="0",color=(0, 0, 255, 1), halign="left", font_size='15sp', size_hint=(None, None), width=18, height=18, pos_hint={'center_x':0.05, 'top':1})
        self.add_widget(self.like_num)

        self.txt = TextInput(text="commenta", multiline=False, size_hint=(None, None), width= 90, height=27,
                             pos_hint={'center_x': 0.6, 'top':1}, font_size='13sp')
        self.txt.bind(on_text_validate=self.on_enter)
        self.add_widget(self.txt)

        self.comments = Label(text="", color=(0, 0, 255, 1), halign="left", font_size='15sp', size_hint=(None, None),
                              pos_hint={'center_x': 0.415, 'top': 0.800})
        self.add_widget(self.comments)

    def btn_pressed(self, *args):
        self.count += 1
        self.like_num.text = str(self.count)

    def on_enter(self, *args):
        self.comments.text = (self.comments.text + "\n" + self.txt.text)



# caratteristiche predefinite dell'immagine di un tipo post: immagine
#ottimizzata per il BoxLayout

class MyImage(Image):
    def __init__(self, name, *args):
        super(MyImage, self).__init__(*args)
        self.source = name
        self.size_hint = (1, None)
        self.height=500
        self.pos_hint = {'center_y':0.5, 'top':1}

# caratteristiche predefinite del testo di un tipo post: testo
class MyText(Label):
    def __init__(self, mytext, *args):
        super(MyText, self).__init__(*args)
        self.text = mytext
        self.font_size="16sp"
        self.color=(0,0,0,1)
        self.size_hint = (None, None)
        self.halign='left'

        #self.pos=(self.x+470, self.y+160)
        self.po
        s_hint = {'center_x': 0.5, 'top': 0.8}


# tipo post: immagine
class PostImage(BoxLayout):
    def __init__(self, name_img, *args):
        super(PostImage, self).__init__(*args)

        # aggiungo uno sfondo al layout, aggiungendo un rettangolo colorato
        with self.canvas.before:
            Color(0, 255, 255, 1)  # bianco
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # listen to size and position changes (aggiorno la posizione del rettangolo colorato/layout)
        self.bind(pos=update_rect, size=update_rect)

        self.orientation='vertical'
        self.size_hint = (None, None)
        self.width= 450
        self.height = 600
        self.pos_hint = {'center_x': 0.55, 'top': 0.95}
        self.spacing=0

        self.add_widget(MyImage("magic.jpg"))
        self.add_widget(Counter())


# tipo post: testo
class PostText(FloatLayout):
    def __init__(self, my_text, *args):
        super(PostText, self).__init__(*args)

        self.add_widget(MyText(my_text))
        # bottone per i like
        btn = ImageButton('heartblue.png')
        btn.size_hint = (0.022, 0.032)
        btn.pos_hint = {'center_x': 0.420, 'top': 0.685}
        btn.on_press = self.btn_pressed
        self.add_widget(btn)



        # counter per i like
        self.count = 0
        self.like_num = Label(text="0", color=(0, 0, 255, 1), halign="left", font_size='19sp', size_hint=(None, None),
                              pos_hint={'center_x': 0.405, 'top': 0.740})
        self.add_widget(self.like_num)

        # commenti
        self.txt = TextInput(text="commenta", multiline=False, size_hint=(0.1, 0.046),
                             pos_hint={'center_x': 0.490, 'top': 0.690}, font_size='14sp')
        self.txt.bind(on_text_validate=self.on_enter)
        self.add_widget(self.txt)

        self.comments = Label(text="", color=(0, 0, 255, 1), halign="left", font_size='15sp', size_hint=(None, None),
                              pos_hint={'center_x': 0.415, 'top': 0.640})
        self.add_widget(self.comments)

    # incrementa il contatore quando l'user preme il bottone "like"
    def btn_pressed(self, *args):
        self.count += 1
        self.like_num.text = str(self.count)

    # quando l'user preme "invio" da tastiera mentre scrive nel textinput, mostra il commento inserito
    def on_enter(self, *args):
        self.comments.text = (self.comments.text + "\n" + self.txt.text)

class ImageButton(ButtonBehavior, Image):
    def __init__(self, img, *args):
        super(ImageButton, self).__init__(*args)

        self.source= img





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

        self.size_hint = (None, None)
        self.width = 1000
        self.height = 3000

        #ricerca utenti
        self.searchuser=TextInput(text= "Search", multiline=False, size_hint=(None, None), width= 100 , height=25,
                                  pos_hint={'x': 0.80, 'top': 0.98}, font_size='12sp')
        self.searchuser.bind(on_text_validate=self.on_enter2)
        self.add_widget(self.searchuser)

        self.searchbtn = ImageButton("little2.jpg")
        self.searchbtn.size_hint=(None, None)
        self.searchbtn.width= 25
        self.searchbtn.height= 25
        self.searchbtn.pos_hint={'right': 0.92, 'top': 0.98}
        self.searchbtn.font_size='12sp'
        #searchbtn.on_press=self.btn2_pressed
        self.add_widget(self.searchbtn)

        #prova: aggiungo immagine o testo
        self.add_widget(PostImage("magic.jpg"))
        #self.add_widget(PostText('Text in a very long lineeeeeeeeeeeeeee\nanother line'))

    def on_enter2(self, *args):
        # DropDownMenu
        dropdown = DropDown()

        btn1 = Button(text=self.searchuser.text, size_hint_y=None, height=44)
        btn1.bind(on_release=lambda btn1: dropdown.select(btn1.text))
        dropdown.add_widget(btn1)

        self.searchbtn.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.searchbtn, 'text', x))


class MySocialApp(App):
    def build(self):
        sv = ScrollView(size_hint=(None, None), size=(1000, 500), pos_hint={'center_x': 0.5, 'top': 0.9},
                        do_scroll_x=False, do_scroll_y=True)

        sv.add_widget(MyWidget())

        return sv


if __name__ == '__main__':
    MySocialApp().run()


