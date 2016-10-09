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


class MyImage(Image):
    def __init__(self, name, *args):
        super(MyImage, self).__init__(*args)
        self.source = name
        self.pos_hint = {'center_x': 0.5, 'center_y': .5}
        self.size_hint = (0.4, 0.4)


class Comments(TextInput):
    def __init__(self, *args):
        super(Comments, self).__init__(*args)
        self.text = "commenta"
        self.multiline = False
        self.size_hint = (0.1, 0.04)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.2}
        self.font_size = '12sp'


class ShowComment(Label):
    def __init__(self, string, *args):
        super(ShowComment, self).__init__(*args)
        self.text = string
        self.color =  0, 0, 255, 1
        self.size_hint=(None,None)
        self.pos_hint={'x':0.375,'y':0}
        self.font_size = '14sp'

    # quando un nuovo commento "string" viene inserito, lo aggiungo
    def add_comment(self, stringa):
        self.text = self.text + "\n" + stringa



class MyWidget(FloatLayout):
    def __init__(self, *args):
        super(MyWidget, self).__init__(*args)

        # self.ap.clear_widgets()
        with self.canvas.before:
            Color(255, 255, 255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # listen to size and position changes
        self.bind(pos=update_rect, size=update_rect)

        #self.add_widget(MainLayout())
        self.add_widget(TextInput(text='Search users', multiline=False, size_hint=(None, 0.04),
                                  pos_hint={'right': 1, 'y': 0.879}, font_size='12sp'))
        self.add_widget(MyImage("magic.jpg"))
        self.add_widget(Button(text="Like", size_hint=(0.05,0.05),  pos_hint={'x':0.345, 'y': 0.221}, font_size='12sp'))
        self.add_widget(TextInput(text="commenta", multiline=False, size_hint=(0.1, 0.046), pos_hint={'x':0.345, 'y': 0.258},font_size='14sp'))
        prova = ShowComment("comm1")
        self.add_widget(prova)
        prova.add_comment("comm2")
        prova.add_comment("comm3")
        prova.add_comment("sto scrivendo tante parole")




class MySocialApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MySocialApp().run()


