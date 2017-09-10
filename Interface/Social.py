from kivy.app import App
from kivy.uix.actionbar import ActionPrevious, ActionButton, ActionBar, ActionView

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from functools import partial

#per cambiare schermata
from subprocess import Popen

from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

#funzione per cambiare schermata
def ab_press():
    Popen('python utente.py')



class ImageButton(ButtonBehavior, Image):
    """
    classe per trasformare una immagine
    in un oggetto tipo Button
    """
    def __init__(self, img, *args):
        super(ImageButton, self).__init__(*args)

        self.source= img


class Comments(GridLayout):
    """
    serve per gestire il layout dei commenti 
    nella forma user: commento
    """

    def __init__(self, commentList, **kwargs):
        # make sure we aren't overriding any important functionality
        super(Comments, self).__init__(**kwargs)

        # aggiungo uno sfondo al layout, aggiungendo un rettangolo colorato
        with self.canvas.before:
            Color(1, 1, 1, 1)  # grigio
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # aggiorna la posizione del rettangolo colorato/layout
        self.bind(pos=update_rect, size=update_rect)

        self.cols=1
        self.size_hint=(None,None)
        self.pos_hint = {'x':0.02, 'y': 0.02}
        self.width=430
        self.height=210
        #self.spacing=10

        for comment in commentList:
            ucomment=comment[0]
            comm=comment[1]
            textComment = Label(text=ucomment+': '+comm,
                                color=(0, 0, 255, 1),
                                font_size='12sp',
                                text_size= (self.width,None),
                                halign='left',
                                #pos_hint={'x':0.6}
                                )
            self.add_widget(textComment)


class MyImage(Image):
    """
    caratteristiche predefinite dell'immagine di un tipo post: immagine
    ottimizzate per il BoxLayout
    """
    def __init__(self, name, *args):
        super(MyImage, self).__init__(*args)
        self.source = name
        self.size_hint = (None, None)
        self.width = 430
        self.height=280
        self.pos_hint = {'center_x':0.5, 'center_y':0.71}


class MyText(Label):
    """
    caratteristiche predefinite del testo 
    di un tipo post: testo
    """

    def __init__(self, mytext, *args):
        super(MyText, self).__init__(*args)

        # aggiungo uno sfondo al layout, aggiungendo un rettangolo colorato
        with self.canvas.before:
            Color(0.937, 0.937, 0.937, 0.3)  # grigio 10%
            self.rect = Rectangle(source='verythin.png', size=self.size, pos=self.pos)
            # se non vi piace la cornice mettere a 1 l'indice 'a' del color e scommentare la riga sotto
            #self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # aggiorna la posizione del rettangolo/layout
        self.bind(pos=update_rect, size=update_rect)

        self.text = mytext
        self.font_size="16sp"
        self.color=(0,0.38,0.88,1)
        #self.color = (0, 0, 0, 1)
        self.size_hint = (None, None)
        self.width = 430
        self.height = 280
        self.halign='left'
        self.pos_hint = {'center_x':0.5, 'center_y':0.71}


        #non valgono per il boxlayout
        #self.pos=(self.x+470, self.y+160)
        #self.pos_hint = {'center_x': 0.5, 'top': 0.8}


class Post(FloatLayout):
    """
    Classe che serve per gestire il corpo del post.
    Il float layout permette di posizionare i widget a piacere, senza vincoli oltre a size_hint.        
    """

    def __init__(self, post_type, post_content, *args):
        super(Post, self).__init__(*args)

        with self.canvas.before:
            Color(0.96, 0.96, 0.96, 1)  # grigio exa:F7F7F7
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # aggiorna la posizione del rettangolo colorato/layout
        self.bind(pos=update_rect, size=update_rect)

        self.size_hint=(None, None)
        self.width= 450
        self.height=600


        nomeutente="user_name"
        self.add_widget(Label(text=nomeutente,
                              color=(0, 0, 255, 1),
                              halign="left",
                              font_size='15sp',
                              size_hint=(None, None),
                              pos_hint={'x': 0, 'y': 0.89}))

        if post_type == 'posttext':
            self.add_widget(MyText(post_content))
        elif post_type == 'postimage':
            self.add_widget(MyImage(post_content))

        # contatore "like"
        btn = ImageButton("heartblue.png")
        btn.size_hint = (None, None)
        btn.width = 18
        btn.height = 18
        btn.pos_hint = {'x': 0.07, 'y': 0.38}
        btn.on_press = self.btn_pressed
        self.add_widget(btn)

        self.count = 0
        self.like_num = Label(text="0",
                              color=(0, 0, 255, 1),
                              halign="left",
                              font_size='15sp',
                              size_hint=(None, None),
                              width=18, height=18,
                              pos_hint={'x': 0.03, 'y': 0.38})
        self.add_widget(self.like_num)

        #descrizione dell'immagine/post

        descrizione= "My picture! #ciao #hashtag1 #hashtag2"
        description= Label(text=descrizione,
                           color=(0,0,0.68,1),
                           font_size='11pt',
                           halign="left",
                           pos_hint={'x':-0.19, 'y': -0.055})
        self.add_widget(description)

        #inserimento commenti
        self.txt = TextInput(text="commenta",
                             foreground_color=(0, 0, 0, 0.4),
                             multiline=True,
                             size_hint=(None, None),
                             font_size='11sp',
                             width= 95, height=25,
                             pos_hint={'x':0.13, 'y': 0.375},
                             background_normal = 'textinput2.png')
        #validare con enter
        #self.txt.bind(on_text_validate=self.on_enter)
        self.add_widget(self.txt)

        self.btn_cmm=Button(text="ok",
                            color=(0, 0, 0, 0.4),
                            size_hint=(None, None),
                            width=25, height=25,
                            pos_hint={'x':0.34, 'y': 0.375},
                            font_size='13sp',
                            background_normal='buttonbkgr.png')
        self.btn_cmm.on_press = self.btn_pressed2
        self.add_widget(self.btn_cmm)

        """
        attenzione!!! Le prossime 2 linee di codice si sovrappongono all'inserimento commenti 
        di un vettore di label, se si inserisce un commento nel textinput (linee di codice successive).
        """
        self.comments = Label(text="",
                              color=(0,0,0.68,1),
                              halign="left",
                              size_hint=(None, None),
                              pos_hint={'x': 0.05, 'y': 0.05})
        self.add_widget(self.comments)

        #inserimento commenti come vettore di label

        commentList = [("user1","Commento!"), ("user2","com mento2..."), ("user3", "COMMENto\ncommento3!"),
                       ("user4","Commentooooo4 lunghissimoooooooooooooooooooooo"),
                       ("user5", "Commento!"), ("user6", "com mento2..."),
                       ("user7", "Commento!"), ("user8", "com mento2...")
                       ]

        commenti=Comments(commentList)
        self.add_widget(commenti)


    #pubblica i commenti quando si preme invio
    # def on_enter(self, *args):
    #     self.comments.text = (self.comments.text + "\n" + self.txt.text)

    def btn_pressed(self, *args):
        self.count += 1
        self.like_num.text = str(self.count)

    # funzione che pubblica i commenti cliccando sul bottone
    def btn_pressed2(self, *args):
        self.comments.text = (self.comments.text + "\n" + self.txt.text)


class Timeline(GridLayout):
    """
    Timeline del social
    contiene tutti i post degli utenti uno sotto all'altro.
    """

    def __init__(self, *args):
        super(Timeline, self).__init__(*args)
        # self.ap.clear_widgets()

        #self.orientation='vertical'
        # prova: aggiungo immagine o testo
        self.cols=1
        self.spacing=10
        #self.size_hint=(1,1)
        #self.pos_hint={'center_x': 0.5, 'center_y': 0.68}

        """
        Il primo parametro della funzione post indica il tipo di post che si intende pubblicare:
        'posttext', per tipo testo, 'postimage' per il tipo immagine;
        il secondo parametro indica il contenuto del post.
        """
        self.add_widget(Post('posttext', 'Text in a very long lineeeeeeeeeeeeeee\nanother line'))
        self.add_widget(Post('posttext', 'dsfjskdjfkdsf sdkfjksdjf sdkfjkldfj sdkf\nwelkkdjewfld efljwefod oejfwld\nlsdfjlakjd sldkfjs\nlwadjlawdkjlkdfjesklf'))
        self.add_widget(Post('posttext', 'last text-----\nwhere\nare\nyou?'))
        self.add_widget(Post('postimage', "magic.jpg"))


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

        # aggiorna la posizione del rettangolo colorato/layout
        self.bind(pos=update_rect, size=update_rect)

        self.size_hint = (1, None)
        #self.width = 1024
        self.height = self.height+2700

        self.add_widget(Timeline())



class MySocialApp(App):

    #funzione che fa comparire il DropDownMenu per cercare la stringa che si inserisce nella "searchuser"
    def build(self):

        def on_enter2(self, *args):
            # DropDownMenu
            dropdown = DropDown()

            btn1 = Button(text=searchuser.text,
                          color=(0, 0, 255, 0.8),
                          font_size='13sp',
                          size_hint_y=None,
                          height=22,
                          background_color=(0, 0, 0, 0))
            btn1.bind(on_release=lambda btn1: dropdown.select(btn1.text))
            dropdown.add_widget(btn1)

            # for index in range(10):
            #     #text=self.searchuser.text
            #     btn1 = Button(text='Value %d' % index, color= (0,0,255,0.8), font_size='13sp',
            #                   size_hint_y=None, height=22, background_color= (0, 0, 0, 0))
            #     btn1.bind(on_release=lambda btn1: dropdown.select(btn1.text))
            #     dropdown.add_widget(btn1)

            mainbutton = searchbtn
            mainbutton.bind(on_release=dropdown.open)
            dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        Window.clearcolor = (1,1,1,1)

        # layout actionbar
        ap = ActionPrevious(with_previous=False, title="NomeSocial", color=(0, 0, 255, 1), app_icon='aven.jpg')
        ab = ActionButton(icon='bianco.png')
        ab2 = ActionButton(icon='refresh.png')

        ab.on_press = ab_press

        bar = ActionBar(background_color=(0, 0, 0, 0.1), pos_hint={'top': 1})
        aw = ActionView()
        aw.add_widget(ap)
        aw.add_widget(ab2)
        aw.add_widget(ab)
        bar.add_widget(aw)

        Window.add_widget(bar, canvas=None)

        # layout ricerca utenti
        searchuser = TextInput(text="search user",
                               foreground_color=(0, 0, 0, 0.4),
                               multiline=False,
                               size_hint=(None, None),
                               width=100, height=25,
                               pos_hint={'center_x': 0.50, 'top': 0.98},
                               font_size='12sp',
                               background_normal='textinput2.png')
        searchuser.bind(on_text_validate=on_enter2)

        searchbtn = ImageButton("srch.png")
        searchbtn.size_hint = (None, None)
        searchbtn.width = 80
        searchbtn.height = 25
        searchbtn.pos_hint = {'center_x': 0.545, 'top': 0.98}
        searchbtn.font_size = '12sp'
        # searchbtn.on_press=self.btn2_pressed

        Window.add_widget(searchuser)
        Window.add_widget(searchbtn)

        sv = ScrollView(size_hint=(0.332, 1),
                        do_scroll_x=False,
                        do_scroll_y=True,
                        pos_hint={'center_x': 0.5, 'top': 0.9})

        sv.add_widget(MyWidget())
        return sv


if __name__ == '__main__':
    MySocialApp().run()


