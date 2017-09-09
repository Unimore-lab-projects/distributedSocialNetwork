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
from kivy.core.window import Window
from functools import partial

#per cambiare schermata
from subprocess import Popen

from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')



#funzione per cambiare schermata
def ab_press():
    Popen('python social.py')


#variabili globali che servono per collegare il textinput al PostText
def on_enter(self, *args):
    # self.statusout.text = (self.statusout.text + '\n' + self.statusin.text)
    pass


statusin = TextInput(text="A cosa stai pensando?",
                     foreground_color=(0, 0, 0, 0.4),
                     multiline=True,
                     size_hint=(None, None),
                     width=270, height=60,
                     pos_hint={'x': 0.12, 'top': 0.50},
                     font_size='13sp',
                     background_normal='textinput2.png')

statusout = Label(text="",
                  color=(0, 0, 255, 1),
                  halign="left",
                  font_size='15sp',
                  size_hint=(None, None),
                  pos_hint={'x': 0.40, 'top': 0.20})

statusin.bind(on_text_validate=on_enter)

btn_pub = Button(text="pubblica",
                 size_hint=(None, None),
                 width=80, height=25,
                 pos_hint={'x': 0.595, 'top': 0.20},
                 font_size='13sp',
                 background_normal='buttonbkgr.png')


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
        self.pos_hint = {'x':0.05, 'y': 0.05}
        self.width=430
        self.height=210
        #self.spacing=10

        for comment in commentList:
            ucomment=comment[0]
            comm=comment[1]
            textComment = Label(text=ucomment+': '+comm, color=(0, 0, 255, 1),
                                font_size='12sp',
                                text_size= (self.width,None),
                                halign='left',
                                #pos_hint={'x':0.6}
                                )
            self.add_widget(textComment)


class StatusBody(FloatLayout):
    """
    classe per pubblicare i post. 
    Contiene il textinput, il bottone per pubblicare,
    l'immagine utente e la bio.
    """
    def __init__(self, *args):
        super(StatusBody, self).__init__(*args)

        # aggiungo uno sfondo al layout, aggiungendo un rettangolo colorato
        with self.canvas.before:
            Color(255, 255, 255, 1)  # bianco
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # aggiorna la posizione del rettangolo/layout
        self.bind(pos=update_rect, size=update_rect)

        self.size_hint = (None, None)
        self.width = 400
        self.height = 220
        self.pos_hint = {'left': 1, 'top': 0.88}

        self.add_widget(Image(source='bianco.png',
                              size_hint=(None, None),
                              pos_hint={'left': 0.5, 'top': 0.98}))

        nomeutente = "user_name" + "\n"
        bio = "Hello! These are my posts!"

        self.add_widget(Label(text=nomeutente + bio,
                              color=(0,0.38,0.88,1),
                              halign="left",
                              size_hint=(None, None),
                              pos_hint={'x': 0.40, 'top': 0.98}))

        self.add_widget(statusin)
        self.add_widget(statusout)

        self.add_widget(btn_pub)


class Body(FloatLayout):
    """
    classe che serve per gestire il corpo del post.
    Il float layout permette di mettere i widget dove si vuole, cosa che non sarebbe possibile con il boxlayout!
    La classe contiene il contatore dei like, il bottone dei like, il textinput per i commenti e i commenti inseriti nel textinput;
    serve anche per gestire i posizionamentitra l'immagine e il corpo del post! 
    """
    def __init__(self, *args):
        super(Body, self).__init__(*args)

        self.size_hint=(None, None)
        self.width= 250
        self.height=200

        nomeutente="user_name"
        self.add_widget(Label(text=nomeutente,
                              color=(0,0.38,0.88,1),
                              halign="left",
                              font_size='15sp',
                              size_hint=(None, None),
                               width=18, height=18,
                              pos_hint={'x': 0.15, 'top': 3}))

        #contatore "like"
        btn=ImageButton("heartblue.png")
        btn.size_hint=(None,None)
        btn.width = 18
        btn.height= 18
        btn.pos_hint = {'center_x': 0.15, 'center_y': 1.2}
        btn.on_press = self.btn_pressed
        self.add_widget(btn)

        self.count = 0
        self.like_num = Label(text="0",
                              color=(0, 0, 255, 1),
                              halign="left",
                              font_size='15sp',
                              size_hint=(None, None),
                              width=18, height=18,
                              pos_hint={'center_x': 0.05, 'center_y': 1.2})
        self.add_widget(self.like_num)

        #descrizione dell'immagine/post

        descrizione= "My picture! #ciao #hashtag1 #hashtag2"
        description= Label(text=descrizione,
                           color=(0,0,0.68,1),
                           halign="left",
                           size_hint=(None, None),
                           width=18, height=18,
                           pos_hint={'center_x':0.55, 'center_y': 1.4})
        self.add_widget(description)

        #inserimento commenti
        self.txt = TextInput(text="commenta",
                             foreground_color=(0, 0, 0, 0.4),
                             multiline=True,
                             size_hint=(None, None),
                             font_size='11sp',
                             width= 95, height=25,
                             pos_hint={'center_x':0.55, 'center_y': 1.2},
                             background_normal = 'textinput2.png')
        #validare con enter
        #self.txt.bind(on_text_validate=self.on_enter)
        self.add_widget(self.txt)

        self.btn_cmm=Button(text="ok",
                            size_hint=(None, None),
                            color=(0, 0, 0, 0.4),
                            width=25, height=25,
                            pos_hint={'center_x':0.78, 'center_y': 1.2},
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
                              pos_hint={'center_x': 0.415, 'center_y': 1})
        self.add_widget(self.comments)

        #inserimento commenti come vettore di label

        commentList = [("user1", "Commento!"), ("user2", "com mento2..."), ("user3", "COMMENto\ncommento3!"),
                       ("user4", "Commentooooo4 lunghissimoooooooooooooooo"),
                       ("user1", "Commento!"), ("user2", "com mento2...")]

        commenti=Comments(commentList)
        self.add_widget(commenti)

    def btn_pressed(self, *args):
        self.count += 1
        self.like_num.text = str(self.count)

    #pubblica i commenti quando si preme invio
    # def on_enter(self, *args):
    #     self.comments.text = (self.comments.text + "\n" + self.txt.text)

    # funzione che pubblica i commenti cliccando sul bottone
    def btn_pressed2(self, *args):
        self.comments.text = (self.comments.text + "\n" + self.txt.text)


class MyImage(Image):
    """
    caratteristiche predefinite dell'immagine di un tipo post: immagine
    ottimizzata per il BoxLayout
    """
    def __init__(self, name, *args):
        super(MyImage, self).__init__(*args)
        self.source = name
        self.size_hint = (1, None)
        self.height=500
        self.pos_hint = {'center_y':0.5, 'top':1}


class MyText(Label):
    """
    caratteristiche predefinite del testo di un tipo post: testo
    ottimizzate per il BoxLayout
    """
    def __init__(self, mytext, *args):
        super(MyText, self).__init__(*args)

        self.text = mytext
        self.font_size = "16sp"
        self.color = (0,0.38,0.88,1) # blu scuro
        self.size_hint = (1, 1)
        self.halign = 'left'
        self.pos_hint = {'center_y': 0.5, 'top': 1}

        # non valgono per il boxlayout
        # self.pos=(self.x+470, self.y+160)
        # self.pos_hint = {'center_x': 0.5, 'top': 0.8}


class PostImage(BoxLayout):
    """
    ottimizzata per la classe Body
    pubblica un post di tipo immagine
    """
    def __init__(self, name_img, *args):
        super(PostImage, self).__init__(*args)

        # aggiungo uno sfondo al layout, aggiungendo un rettangolo colorato
        with self.canvas.before:
            Color(0.96, 0.96, 0.96, 1)  # grigio exa:F7F7F7
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

        self.add_widget(MyImage(name_img))
        self.add_widget(Body())


class PostText(BoxLayout):
    """
    ottimizzata per la classe Body
    pubblica un post di tipo immagine
    """
    def __init__(self, my_text, *args):
        super(PostText, self).__init__(*args)

        # aggiungo uno sfondo al layout, aggiungendo un rettangolo colorato
        with self.canvas.before:
            Color(0.96,0.96,0.96,1)  # grigio exa:F7F7F7
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # aggiorna la posizione del rettangolo colorato/layout
        self.bind(pos=update_rect, size=update_rect)

        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.width = 450
        self.height = 600
        self.pos_hint = {'center_x': 0.55, 'top': 0.95}
        self.spacing = 0

        self.add_widget(MyText(my_text))
        self.add_widget(Body())


class ImageButton(ButtonBehavior, Image):
    """
    classe per trasformare una immagine
    in un oggetto tipo Button
    """
    def __init__(self, img, *args):
        super(ImageButton, self).__init__(*args)

        self.source = img


class Timeline(GridLayout):
    """
        Timeline dell'utente
        contiene tutti i post degll'utente uno sotto all'altro
        parametro i serve per invertire l'ordine di inserimento
        nel caso di BoxLayout
    """

    i=0

    def __init__(self, *args):
        super(Timeline, self).__init__(*args)
        # self.ap.clear_widgets()

        #self.orientation='vertical'

        self.cols=1
        self.spacing = 10
        #self.size_hint = (1, None)
        #self.pos_hint={'center_x': 0.5, 'center_y':0.5}
        #self.width = 1024
        #self.height = self.height + 3000

        #prova:aggiungo immagine o testo
        #self.add_widget(PostText('Text in a very long lineeeeeeeeeeeeeee\nanother line'))
        #self.add_widget(PostImage("magic.jpg"))

        #evento legato alla variabile globale btn_pub
        btn_pub.on_press=partial(self.btn_pressed)


    #funzione che pubblica sottoforma di testo cio che e' scritto nel textinput (statusin)
    #i post vengono inseriti uno sopra l'altro (default: uno sotto l'altro)
    def btn_pressed(self):
        self.add_widget(PostText(statusin.text), index=self.i+1)
        self.i=self.i+1
        return self.i

        #statusout.text = (statusout.text + '\n' + statusin.text)


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

        # aggiorna la posizione del rettangolo colorato/layout
        self.bind(pos=update_rect, size=update_rect)

        self.size_hint = (1, None)
        # self.width = 1024
        self.height = self.height + 2700

        #self.add_widget(StatusBody())

        # aggiungo la timeline
        self.add_widget(Timeline())


class MySocialApp(App, FloatLayout):

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)

        # layout actionbar
        ap = ActionPrevious(with_previous=False,
                            title="NomeSocial",
                            color=(0, 0, 255, 1),
                            app_icon='aven.jpg')

        ab = ActionButton(icon='home.png')

        ab.on_press = ab_press

        bar = ActionBar(background_color=(0, 0, 0, 0.1),
                        pos_hint={'top': 1})

        aw = ActionView()
        aw.add_widget(ap)
        aw.add_widget(ab)
        bar.add_widget(aw)

        Window.add_widget(bar, canvas=None)
        Window.add_widget(StatusBody(), canvas=None)

        sv = ScrollView(size_hint=(0.332, 1),
                        do_scroll_x=False,
                        do_scroll_y=True,
                        pos_hint={'center_x': 0.5, 'top': 0.9})

        sv.add_widget(MyWidget())
        return sv


if __name__ == '__main__':
    MySocialApp().run()



