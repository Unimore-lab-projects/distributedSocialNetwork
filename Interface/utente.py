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
from kivy.uix.scrollview import ScrollView


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
                icon: 'home.png'


 """

Builder.load_string(kv)


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
        self.font_size = "16sp"
        self.color = (0, 0, 0, 1)
        self.size_hint = (None, None)
        self.halign = 'left'

        # self.pos=(self.x+470, self.y+160)
        self.pos_hint = {'center_x': 0.5, 'top': 0.8}

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
        self.pos_hint = {'center_x': 0.6, 'top': 0.95}
        self.spacing=0

        self.add_widget(MyImage("magic.jpg"))
        self.add_widget(Counter())


class ImageButton(ButtonBehavior, Image):
    def __init__(self, img, *args):
        super(ImageButton, self).__init__(*args)

        self.source = img


class MyWidget(FloatLayout):
    def __init__(self, *args):
        super(MyWidget, self).__init__(*args)
        # self.ap.clear_widgets()

        # aggiungo uno sfondo al layout, aggiungengo un rettangolo colorato
        with self.canvas.before:
            Color(255, 255, 255, 1)  # bianco
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size


        # listen to size and position changes (aggiorno la posizione del rettangolo colorato/layout)
        self.bind(pos=update_rect, size=update_rect)

        self.size_hint=(None,None)
        self.width=1000
        self.height=3000

        self.add_widget(Image(source='bianco.png', size_hint=(None,None), pos_hint={'left':1,'top':0.97}))
        self.add_widget(Label(text='USER NAME\nHello! These are my posts!', color=(0,0,255,1), halign= "left", size_hint=(None, None),
                              pos_hint={'x': 0.14, 'top': 0.96}))

        # prova: aggiungo immagine o testo

        self.add_widget(PostImage("magic.jpg"))
        #self.add_widget(Counter())
        # self.add_widget(PostText('Text in a very long lineeeeeeeeeeeeeee\nanother line'))




class MySocialApp(App):
    def build(self):


        sv = ScrollView(size_hint=(None,None), size=(1000, 500), pos_hint={'center_x': 0.5, 'top': 0.9},
                        do_scroll_x=False, do_scroll_y=True)

        sv.add_widget(MyWidget())


        return sv


if __name__ == '__main__':
    MySocialApp().run()
