from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.lang import Builder
from kivy.base import runTouchApp

from kivy.uix.scrollview import ScrollView
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton


#layout actionbar
ap=ActionPrevious(with_previous= False, title="NomeSocial", color= (0, 0, 255, 1),app_icon= 'aven.jpg')
ab=ActionButton(icon= 'home.png')
bar = ActionBar(background_color = (0, 0, 0, 0.1),pos_hint = {'top': 1})
aw=ActionView()
aw.add_widget(ap)
aw.add_widget(ab)
bar.add_widget(aw)

#immagini come bottoni
class ImageButton(ButtonBehavior, Image):
    def __init__(self, img, *args):
        super(ImageButton, self).__init__(*args)

        self.source= img


class PostImage(Image):
    def __init__(self, name, *args):
        super(PostImage, self).__init__(*args)
        self.source = name
        self.size_hint = (0.5, 0.5)
        self.height=500
        self.pos_hint = {'center_x':0.5, 'center_y': .5}


class PostText(Label):
    def __init__(self, mytext, *args):
        super(PostText, self).__init__(*args)
        self.text = mytext
        self.font_size="16sp"
        self.color=(0,0,0,1)
        self.size_hint = (1, None)
        self.pos_hint = {'center_x':0.5, 'center_y': .5}
        self.halign='left'

class Comments(GridLayout):
    def __init__(self, commentList, **kwargs):
        # make sure we aren't overriding any important functionality
        super(Comments, self).__init__(**kwargs)
        self.cols=1
        self.size_hint=(0.1,0.1)
        self.pos_hint = {'center_x':0.5, 'center_y': .1}
        for comment in commentList:
            textComment = Label(text=comment, color=(0, 0, 255, 1), halign="left", font_size='15sp',
                                size_hint=(1.0, 1.0),
                                pos_hint={'center_x': 0.5, 'top': 0.800})
            self.add_widget(textComment)


class RootWidget(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)

        # esempio di widget...bottone
        """self.add_widget(
            Button(
                text="Hello World",
                size_hint=(.5, .5),
                pos_hint={'center_x': .5, 'center_y': .5})
        )"""

        self.add_widget(bar)

        # layout ricerca utenti
        self.searchuser = TextInput(text="search user", multiline=False, size_hint=(None, None), width=100, height=25,
                               pos_hint={'center_x': 0.50, 'top': 0.98}, font_size='12sp')
        self.searchuser.bind(on_text_validate=self.on_enter2)


        self.searchbtn = ImageButton("little2.jpg")
        self.searchbtn.size_hint = (None, None)
        self.searchbtn.width = 25
        self.searchbtn.height = 25
        self.searchbtn.pos_hint = {'center_x': 0.546, 'top': 0.98}
        self.searchbtn.font_size = '12sp'

        self.add_widget(self.searchuser)
        self.add_widget(self.searchbtn)

        #contatore like
        self.btn = ImageButton("heartblue.png")
        self.btn.size_hint = (None, None)
        self.btn.width = 18
        self.btn.height = 18
        self.btn.pos_hint = {'center_x': 0.28, 'center_y': 0.2}
        self.btn.on_press = self.btn_pressed
        self.add_widget(self.btn)

        self.count = 0
        self.like_num = Label(text="0", color=(0, 0, 255, 1), halign="left", font_size='15sp', size_hint=(None, None),
                              width=18, height=18, pos_hint={'center_x': 0.255, 'center_y': 0.2})
        self.add_widget(self.like_num)


        # inserimento commenti
        self.txt = TextInput(text="commenta", multiline=False, size_hint=(None, None), width=90, height=27,
                             pos_hint={'center_x': 0.5, 'center_y': 0.2}, font_size='13sp')
        self.txt.bind(on_text_validate=self.on_enter)
        self.add_widget(self.txt)
        #self.comments = Label(text="", color=(0, 0, 255, 1), halign="left", font_size='15sp', size_hint=(None, None),
                              #pos_hint={'center_x': 0.5, 'top': 0.21})
        #self.add_widget(self.comments)

        # modifica inserimento commenti come vettore di label
        # formato del tipo "%s : %s" % (comment.user_id, comment.content)
        commentList = ["Commento!", "com mento2...", "COMMENto commento3!", "Commentooooo4"]

        commenti=Comments(commentList)
        self.add_widget(commenti)

        # prova: aggiungo immagine o testo
        self.add_widget(PostImage("magic.jpg"))
        #self.add_widget(PostText('Text in a very long lineeeeeeeeeeeeeee\nanother line'))


    def btn_pressed(self, *args):
        self.count += 1
        self.like_num.text = str(self.count)

    def on_enter(self, *args):
        self.comments.text = (self.comments.text + "\n" + self.txt.text)

    #menu a tendina per la ricerca contatti
    def on_enter2(self, *args):
        # DropDownMenu
        dropdown = DropDown()

        btn1 = Button(text=self.searchuser.text, size_hint_x=None, size_hint_y=None,height=44)
        btn1.bind(on_release=lambda btn1: dropdown.select(btn1.text))
        dropdown.add_widget(btn1)

        self.searchbtn.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.searchbtn, 'text', x))



class MainApp(App):

    def build(self):

        self.root = root = RootWidget()
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(0, 1, 0.6, 1)  # green; colors range from 0-1 not 0-255
            self.rect = Rectangle(size=root.size, pos=root.pos)
        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size



if __name__ == '__main__':
    MainApp().run()


