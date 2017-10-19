# per cambiare schermata
from subprocess import Popen
from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from twisted.spread import pb
from backend.Peer.node import node
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.actionbar import ActionPrevious, ActionButton, ActionBar, ActionView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from functools import partial

Config.set('graphics', 'fullscreen', 'auto')


# funzione per cambiare schermata
def switch_timelines_fcn():
    # execfile('/home/archeffect/PycharmProjects/distributedSocialNetwork/Interface/utente.py')
    pass


class StatusBody(FloatLayout):
    """
    classe per pubblicare i post.
    Contiene il textinput, il bottone per pubblicare,
    l'immagine utente e la bio.
    """

    def __init__(self, myNode, *args):
        super(StatusBody, self).__init__(*args)
        self.myNode = myNode
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
                              color=(0, 0.38, 0.88, 1),
                              halign="left",
                              size_hint=(None, None),
                              pos_hint={'x': 0.40, 'top': 0.98}))

        self.statusin = TextInput(text="A cosa stai pensando?",
                                  foreground_color=(0, 0, 0, 0.4),
                                  multiline=True,
                                  size_hint=(None, None),
                                  width=270, height=60,
                                  pos_hint={'x': 0.12, 'top': 0.50},
                                  font_size='13sp',
                                  background_normal='textinput2.png')

        self.statusout = Label(text="",
                               color=(0, 0, 255, 1),
                               halign="left",
                               font_size='15sp',
                               size_hint=(None, None),
                               pos_hint={'x': 0.40, 'top': 0.20})

        self.statusin.bind(on_text_validate=self.on_enter)

        self.add_widget(self.statusin)
        self.add_widget(self.statusout)
        pub_btn = Button(text="pubblica",
                         size_hint=(None, None),
                         width=80, height=25,
                         pos_hint={'x': 0.595, 'top': 0.20},
                         font_size='13sp',
                         background_normal='buttonbkgr.png')
        pub_btn.on_press = self.pubblica_post
        self.add_widget(pub_btn)

    def pubblica_post(self):
        print("bnt_pressed")
        print("statusin %s " % self.statusin.text)
        self.myNode.insertPost(text_content=self.statusin.text)
        # Post(post_content=self.statusin.text, username="username")

    # variabili globali che servono per collegare il textinput al PostText
    def on_enter(self, *args):
        self.statusout.text = (self.statusout.text + '\n' + self.statusin.text)
        pass


class ImageButton(ButtonBehavior, Image):
    """
    classe per trasformare una immagine
    in un oggetto tipo Button
    """

    def __init__(self, img, *args):
        super(ImageButton, self).__init__(*args)

        self.source = img


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
        # self.bind(minimum_height=self.setter('height'))

        self.cols = 1
        self.size_hint = (None, None)
        # self.pos_hint = {'x': 0.02, 'y': 0.02}
        self.width = 440
        self.spacing = 5
        self.height = ((20 * len(commentList)) + (self.spacing[0] * len(commentList)))
        self.padding = [5, 5]
        # self.padding=5

        for comment in commentList:
            user = comment[0]
            text = comment[1]
            textComment = Label(text=user + ': ' + text,
                                size_hint=(None, None),
                                size=(450, 20),
                                color=(0, 0, 255, 1),
                                font_size='12sp',
                                # text_size=(self.width, None),
                                halign='left',
                                # pos_hint={'x':0.6}
                                )
            # textComment = Button(text=ucomment)
            self.add_widget(textComment)


#
# class MyImage(Image):
#     """
#     caratteristiche predefinite dell'immagine di un tipo post: immagine
#     ottimizzate per il BoxLayout
#     """
#
#     def __init__(self, name, *args):
#         super(MyImage, self).__init__(*args)
#         self.source = name
#         self.size_hint = (None, None)
#         self.width = 430
#         self.height = 280
#         self.pos_hint = {'center_x': 0.5, 'center_y': 0.71}


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
            # self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # aggiorna la posizione del rettangolo/layout
        self.bind(pos=update_rect, size=update_rect)

        self.text = mytext
        self.font_size = "16sp"
        self.color = (0, 0.38, 0.88, 1)
        # self.color = (0, 0, 0, 1)
        self.size_hint = (None, None)
        self.width = 440
        self.height = 80
        self.halign = 'left'
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.71}


class Post(GridLayout):
    """
    Classe che serve per gestire il corpo del post.
    Il float layout permette di posizionare i widget a piacere, senza vincoli oltre a size_hint.
    """

    def __init__(self, post_type='posttext', post_id=0, post_content="post content", username="username", commentList=None, *args):
        super(Post, self).__init__(*args)
        self.cols = 1
        self.post_id=post_id
        with self.canvas.before:
            Color(0.96, 0.96, 0.96, 1)  # grigio exa:F7F7F7
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # aggiorna la posizione del rettangolo colorato/layout
        self.bind(pos=update_rect, size=update_rect)

        self.size_hint = (None, None)
        self.width = 450
        self.padding = [5, 5]
        self.spacing = 5
        username_widget = Label(text=username,
                                color=(0, 0, 255, 1),
                                halign="left",
                                font_size='15sp',
                                height=20,
                                size_hint=(None, None),
                                pos_hint={'x': 0, 'y': 0.89})

        my_text = MyText(post_content)

        # inserimento commenti come vettore di label

        # commentList = [("user1", "Commento!"),
        #                ("user1", "Commento!"),
        #                ("user1", "Commento!"),
        #                ("user1", "Commento!"),
        #                ("user1", "ultimo Commento!"),
        #                ]

        self.add_widget(username_widget)
        self.add_widget(my_text)
        self.height = username_widget.height + my_text.height + self.spacing[0] * 3 + self.padding[1] * 2

        if commentList:
            comments = Comments(commentList)
            self.add_widget(comments)
            self.height += comments.height



            # pubblica i commenti quando si preme invio

    # def on_enter(self, *args):
    #     self.comments.text = (self.comments.text + "\n" + self.txt.text)

    def btn_pressed(self, *args):
        self.count += 1
        self.like_num.text = str(self.count)

    # funzione che pubblica i commenti cliccando sul bottone
    def btn_pressed2(self, *args):
        self.comments.text = (self.comments.text + "\n" + self.txt.text)


class MyWidget(GridLayout):
    """
    Classe contenitore dello sfondo e contiene la timeline
    """

    def __init__(self, myNode, *args):
        super(MyWidget, self).__init__(*args)
        self.myNode = myNode

        self.size_hint = (None, None)
        self.cols = 1
        self.width = 500
        self.padding = 10
        self.spacing = 20

        self.bind(minimum_height=self.setter('height'))
        deferredList = self.myNode.buildTimeline()
        deferredList.addCallback(self.__got_timeline)

    def __got_timeline(self, all_package_list):
        my_posts=all_package_list[0][1]
        friends_posts=all_package_list[1][1]
        post_list = []
        #my posts
        for pack in my_posts:
            text = pack.result.post.text_content
            new_post = Post('posttext', post_content=text, username=pack.result.username, post_id=pack.result.post.post_id)
            post_list.append(new_post)
            # self.add_widget(new_post)
            pass
        #friends posts
        for pack in friends_posts:
            text = pack.post.text_content
            new_post = Post('posttext', post_content=text, username=pack.username, post_id=pack.post.post_id)
            post_list.append(new_post)

            # self.add_widget(new_post)
            pass


        # ordinamento in base al post_id = timestamp
        post_list.sort(key=lambda x: x.post_id, reverse=True)

        for post in post_list:
            self.add_widget(post)

        pass



class MySocialApp(App, pb.Root):
    """
    Classe container per la scrollview, contiene lo scheletro dell'interfaccia
    """

    def __init__(self, thisNode):
        super(MySocialApp, self).__init__()
        self.thisNode = thisNode
        self.myWidget = MyWidget(thisNode)
        pass

    # funzione che fa comparire il DropDownMenu per cercare la stringa che si inserisce nella "searchuser"
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

        Window.clearcolor = (1, 1, 1, 1)

        # layout actionbar
        menu_bar = ActionPrevious(with_previous=False, title="NomeSocial", color=(0, 0, 255, 1), app_icon='aven.jpg')
        # main_timeline_btn = ActionButton(icon='bianco.png')
        # refresh_btn = ActionButton(icon='refresh.png')
        # refresh_btn.on_press = myWidget.load_timeline
        # main_timeline_btn.bind(on_press=switch_timelines_fcn)

        reload_btn = ActionButton(text="RELOAD")

        action_bar = ActionBar(background_color=(0, 0, 0, 0.1), pos_hint={'top': 1})
        action_view = ActionView()
        action_view.add_widget(menu_bar)
        action_view.add_widget(reload_btn)

        # aw.add_widget(refresh_btn)
        # aw.add_widget(main_timeline_btn)
        action_bar.add_widget(action_view)
        Window.add_widget(action_bar, canvas=None)

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
        self.sv = ScrollView(size_hint=(None, None),
                        size=(500, Window.height),
                        do_scroll_x=False,
                        do_scroll_y=True,
                        pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # user_timeline = UserTimeline(self.myWidget.myNode)
        # self.myWidget.add_widget(Timeline())
        Window.add_widget(StatusBody(self.myWidget.myNode))

        self.sv.add_widget(self.myWidget)

        reload_btn.on_press = self.reload_mywidget

        return self.sv

    def get_ref_btn(self):
        return self.ab

    def reload_mywidget(self):
        print("reload mywidget")
        self.sv.clear_widgets()
        self.myWidget = MyWidget(self.thisNode)
        self.sv.add_widget(self.myWidget)

if __name__ == '__main__':
    # TODO eventualmente mostrare i propri post.
    # TODO caricare i commenti.
    # TODO postare i commenti.
    # TODO mostrare ricerca known nodes.


    thisNode = node('../peer4.config')
    thisNode.populateKnownNodes()
    port = int(thisNode.config['peer_port'])
    app = MySocialApp(thisNode)
    reactor.listenTCP(port, pb.PBServerFactory(app))

    app.run()