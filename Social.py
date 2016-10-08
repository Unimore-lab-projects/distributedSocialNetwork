from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button

kv = """
<MyWidget>:
    ap: ap

    ActionBar:
        background_color:0,191,255,0.5
        pos_hint: {'top':1}


        ActionView:
            ActionPrevious:
                id: ap
                with_previous: False
                title:"NomeSocial"

               # markup:True
               # font_size:"16dp"

            ActionButton:
                icon: 'bianco.png'

            ActionOverflow:
                ActionGroup:
                ActionButton:
                    text: 'Search'






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
        # quando un nuovo commento "string" viene inserito, lo aggiungo
        self.text = string
        self.size_hint = (None, None)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.1}
        self.font_size = '14sp'

    def add_comment(self, stringa):
        self.text = self.text + "\n" + stringa


class MainLayout(BoxLayout):
    def __init__(self, *args):
        super(MainLayout, self).__init__(*args)


class MyWidget(FloatLayout):
    def __init__(self, *args):
        super(MyWidget, self).__init__(*args)

        # self.ap.clear_widgets()


        self.orientation = 'vertical'
        self.add_widget(MyImage("xxx.jpg"))
        self.add_widget(Comments())
        prova = ShowComment("comm1")
        self.add_widget(prova)
        prova.add_comment("comm2")
        prova.add_comment("comm3")
        prova.add_comment("comm4")
        self.add_widget(Label(text="search", pos_hint={'center_x': 0.5, 'center_y': 0.9}))
        self.add_widget(TextInput(text='Search', multiline=False, size_hint=(0.1, 0.04),
                                  pos_hint={'center_x': 0.5, 'center_y': 0.9}, font_size='12sp'))


class MySocialApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MySocialApp().run()


