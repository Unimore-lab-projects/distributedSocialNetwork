
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from  backend.Peer.node import node

from twisted.internet import reactor

from twisted.spread import pb


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


from kivy.metrics import sp
val = sp(1)
from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')


#layout actionbar
#ap=ActionPrevious(with_previous= False, title="NomeSocial", color= (0, 0, 255, 1),app_icon= 'aven.jpg')
#ab=ActionButton(icon= 'bianco.png')
#bar = ActionBar(background_color = (0, 0, 0, 0.1),pos_hint = {'top': 1})
#aw=ActionView()
#aw.add_widget(ap)
#aw.add_widget(ab)
#bar.add_widget(aw)

class Comments(GridLayout):
    def __init__(self, commentList, **kwargs):
        # make sure we aren't overriding any important functionality
        super(Comments, self).__init__(**kwargs)

        self.cols=1
        self.size_hint=(0.5,0.5)
        self.pos_hint = {'center_x': 0.6, 'center_y': 0.8}
        for comment in commentList:
            textComment = Label(text=comment.content, color=(0, 0, 255, 1), halign='left', font_size='15sp',
                                size_hint=(1.0, 1.0),
                                pos_hint={'center_x': 0.5, 'top': 0.800})
            self.add_widget(textComment)



"""classe che serve per gestire il corpo del post.
Il float layout permette di mettere i widget dove si vuole, cosa che non sarebbe possibile con il boxlayout!
La classe contiene il contatore dei like, il bottone dei like, il textinput per i commenti e i commenti inseriti nel textinput;
serve anche per gestire i posizionamentitra l'immagine e il corpo del post! 
"""
class Body(FloatLayout):
    def __init__(self, user_name, comment_list, *args):
        super(Body, self).__init__(*args)

        self.size_hint=(None, None)
        self.width= 250
        self.height=200

        #nomeutente="user_name"
        self.add_widget(Label(text=user_name, color=(0, 0, 255, 1), halign="left", font_size='15sp', size_hint=(None, None),
                               width=18, height=18, pos_hint={'x': 0.15, 'top': 3}))

        #contatore "like"
        btn=ImageButton("heartblue.png")
        btn.size_hint=(None,None)
        btn.width = 18
        btn.height= 18
        btn.pos_hint = {'center_x': 0.15, 'center_y': 1.2}
        btn.on_press = self.btn_pressed
        self.add_widget(btn)

        self.count = 0
        self.like_num = Label(text="0", color=(0, 0, 255, 1), halign="left", font_size='15sp', size_hint=(None, None),
                              width=18, height=18, pos_hint={'center_x': 0.05, 'center_y': 1.2})
        self.add_widget(self.like_num)

#        #descrizione dell'immagine/post
#
#        descrizione= "My picture! #ciao #hashtag1 #hashtag2"
#        description= Label(text=descrizione,color=(0, 0, 255, 1),
#                                halign="left", font_size='15sp', size_hint=(None, None), width=18, height=18,
#                                pos_hint={'center_x':0.55, 'center_y': 1.4})
#        self.add_widget(description)

        #inserimento commenti
        self.txt = TextInput(text="commenta", multiline=False, size_hint=(None, None), width= 90, height=27,
                             pos_hint={'center_x':0.55, 'center_y': 1.2}, font_size='13sp')
        self.txt.bind(on_text_validate=self.on_enter)
        self.add_widget(self.txt)

        """
        attenzione!!! Le prossime 2 linee di codice si sovrappongono all'inserimento commenti 
        di un vettore di label, se si inserisce un commento nel textinput (linee di codice successive).
        """
        self.comments = Label(text="", color=(0, 0, 255, 1), halign="left", font_size='15sp', size_hint=(None, None),
                              pos_hint={'center_x': 0.415, 'center_y': 1})
        self.add_widget(self.comments)

        #inserimento commenti come vettore di label

        #commentList = ["Commento!", "com mento2...", "COMMENto\ncommento3!", "Commentooooo4"]

        commenti=Comments(comment_list)
        self.add_widget(commenti)

    def btn_pressed(self, *args):
        self.count += 1
        self.like_num.text = str(self.count)

    def on_enter(self, *args):
        self.comments.text = (self.comments.text + "\n" + self.txt.text)



# caratteristiche predefinite dell'immagine di un tipo post: immagine
#ottimizzate per il BoxLayout

class MyImage(Image):
    def __init__(self, name, *args):
        super(MyImage, self).__init__(*args)
        self.source = name
        self.size_hint = (1, None)
        self.height=500
        self.pos_hint = {'center_y':0.5, 'top':1}



        # caratteristiche predefinite del testo di un tipo post: testo
#ottimizzate per il BoxLayout
class MyText(Label):
    def __init__(self, mytext, *args):
        super(MyText, self).__init__(*args)
        self.text = mytext
        self.font_size="16sp"
        self.color=(0,0,0,1)
        self.size_hint = (1, None)
        self.halign='left'

        #non valgono per il boxlayout
        #self.pos=(self.x+470, self.y+160)
        #self.pos_hint = {'center_x': 0.5, 'top': 0.8}


# tipo post: immagine
class PostImage(BoxLayout):
    def __init__(self, name_img, *args):
        super(PostImage, self).__init__(*args)

        # aggiungo uno sfondo al layout, aggiungendo un rettangolo colorato
        with self.canvas.before:
            Color(0, 0, 0, 0.1)  # grigio
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # aggiorna la posizione del rettangolo colorato/layout
        self.bind(pos=update_rect, size=update_rect)

        self.orientation='vertical'
        self.size_hint = (None, None)
        self.width= 450
        self.height = 600
        self.pos_hint = {'center_x': 0.55, 'top': 0.95}
        self.spacing=0

        self.add_widget(MyImage("magic.jpg"))
        self.add_widget(Body())


# tipo post: solo testo
class PostText(BoxLayout):
    def __init__(self, post_package, *args):
        super(PostText, self).__init__(*args)

        # aggiungo uno sfondo al layout, aggiungendo un rettangolo colorato
        with self.canvas.before:
            Color(0, 255, 255, 1)  # bianco
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # aggiorna la posizione del rettangolo colorato/layout
        self.bind(pos=update_rect, size=update_rect)

        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.width = 450
        self.height = 300
        self.pos_hint = {'center_x': 0.55, 'top': 0.95}
        self.spacing = 0

        print post_package
        self.add_widget(MyText(post_package.getPost().text_content))
        self.add_widget(Body(post_package.getPost().user_id, post_package.getComments()))

#immagini come bottoni
class ImageButton(ButtonBehavior, Image):
    def __init__(self, img, *args):
        super(ImageButton, self).__init__(*args)

        self.source= img

#Timeline: contiene tutti i post degli utenti uno sotto all'altro
class Timeline(BoxLayout):
    def __init__(self, post_package_list, *args):
        super(Timeline, self).__init__(*args)
        # self.ap.clear_widgets()

        self.orientation='vertical'
        # prova: aggiungo immagine o testo
        self.spacing=10
        self.size_hint=(None,None)
        self.pos_hint={'center_x': 0.5, 'center_y': 0.68}
        
        for post_package in post_package_list:
            self.add_widget(PostText(post_package))

#        self.add_widget(PostImage("magic.jpg"))
#        #self.add_widget(PostText('Text in a very long lineeeeeeeeeeeeeee\nanother line'))
#        self.add_widget(PostImage("magic.jpg"))

class PostCreationWidget(BoxLayout):
    def __init__(self, *args):
        super(PostCreationWidget, self).__init__(*args)
        #Campo di testo per inserire post
        self.txt = TextInput(text="Inserisci Post", multiline=True, size_hint=(None, None), width= 90, 
        height=27,pos_hint={'center_x':0.55, 'center_y': 1.2}, font_size='13sp')
        #self.txt.bind(on_text_validate=self.on_enter)
        self.add_widget(self.txt)
        
        #pulsante per confermare la pubblicazione del post
        self.publish_btn=Button(text='Pubblica')
        self.add_widget(self.publish_btn)
        self.publish_btn.onpress=self.publish_post
        
    #metodo chiamato alla pressione del pulsante pubblica
    def publish_post(self):        
        pass
#    def on_enter(self):
#        pass
    pass

class MyWidget(FloatLayout):
    def __init__(self, buildTimeline, *args):
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

        self.size_hint = (None, None)
        self.width = 1024
        self.height = 4000

        self.ap=ActionPrevious(with_previous= False, title="NomeSocial", color= (0, 0, 255, 1),app_icon= 'aven.jpg')
        self.ab=ActionButton(icon= 'bianco.png')
        self.ab2=ActionButton(icon='refresh2.png')
        self.bar = ActionBar(background_color = (0, 0, 0, 0.1),pos_hint = {'top': 1})
        self.aw=ActionView()
        self.aw.add_widget(self.ap)
        self.aw.add_widget(self.ab)
        self.aw.add_widget(self.ab2)
        self.bar.add_widget(self.aw)

        self.add_widget(self.bar)

        # layout ricerca utenti
        self.searchuser = TextInput(text="search user", multiline=False, size_hint=(None, None), width=100, height=25,
                                    pos_hint={'center_x': 0.50, 'top': 0.996}, font_size='12sp')
        self.searchuser.bind(on_text_validate=self.on_enter2)

        self.searchbtn = ImageButton("little2.jpg")
        self.searchbtn.size_hint = (None, None)
        self.searchbtn.width = 25
        self.searchbtn.height = 25
        self.searchbtn.pos_hint = {'center_x': 0.54, 'top': 0.996}
        self.searchbtn.font_size = '12sp'
        # searchbtn.on_press=self.btn2_pressed

        self.add_widget(self.searchuser)
        self.add_widget(self.searchbtn)
        
        #nuovo post
        #self.new_post=PostCreationWidget()
        #self.add_widget(self.new_post)
        #timeline
        self.buildTimeline=buildTimeline
        self.refresh_timeline()
        
        self.ab2.on_press=self.refresh_timeline
        #self.add_widget(Timeline())

        #sv = ScrollView(do_scroll_x=True, do_scroll_y=False)
        #sv.add_widget(Timeline())
        # self.add_widget(sv)
    
    def refresh_timeline(self):
        deferredList=self.buildTimeline()
        deferredList.addCallback(self.__got_timeline)
        pass
    
    def __got_timeline(self, post_package_list):
        self.current_timeline=Timeline(post_package_list)
        self.add_widget(self.current_timeline)
        pass

    def on_enter2(self, *args):
        # DropDownMenu
        dropdown = DropDown()

        btn1 = Button(text=self.searchuser.text, size_hint_y=None, height=44)
        btn1.bind(on_release=lambda btn1: dropdown.select(btn1.text))
        dropdown.add_widget(btn1)

        self.searchbtn.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.searchbtn, 'text', x))


class MySocialApp(App, pb.Root):
    
    def __init__(self, mainWidget):
        super(MySocialApp, self).__init__()
        self.mainWidget=mainWidget
        pass
    
    def build(self):
        reactor.listenTCP(8003, pb.PBServerFactory(self))
        sv = ScrollView(size_hint=(1,1),do_scroll_x=False, do_scroll_y=True)
        #sv.add_widget(MyWidget())
        sv.add_widget(mainWidget)
        
        return sv


if __name__ == '__main__':
    #MySocialApp().run()
    thisNode=node('peer4.config')
    thisNode.populateKnownNodes()
    mainWidget=MyWidget(thisNode.buildTimeline)
    app=MySocialApp(mainWidget)
    app.run()


