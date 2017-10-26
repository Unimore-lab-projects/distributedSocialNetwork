from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


class ImageButton(ButtonBehavior, Image):
    """
    classe per trasformare una immagine
    in un oggetto tipo Button
    """

    def __init__(self, img, *args):
        super(ImageButton, self).__init__(*args)

        self.source = img


class FriendsFinderLayout(GridLayout):
    def __init__(self, myNode, *args):
        super(FriendsFinderLayout, self).__init__(*args)
        self.myNode = myNode
        self.myNode.populateKnownNodes()
        myNode.getMyNode().addCallback(self.__got_my_user)
        self.size_hint = (None, None)
        self.cols = 1
        self.width = 90
        self.padding = 0
        self.spacing = 0
        self.pos_hint = {'center_x': 0.9, 'top': 0.9}

        self.bind(minimum_height=self.setter('height'))

        with self.canvas.before:
            Color(0.96, 0.96, 0.96, 1)  # grigio exa:F7F7F7
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.searchbtn = ImageButton("srch.png")
        self.searchbtn.size_hint = (None, None)
        self.searchbtn.width = 80
        self.searchbtn.height = 25
        self.searchbtn.pos_hint = {'center_x': 0.545, 'top': 0.98}
        self.searchbtn.font_size = '12sp'

        self.searchbtn.on_press = self.reload_layout

        self.height += self.searchbtn.height
        self.add_widget(self.searchbtn)

        # aggiorna la posizione del rettangolo colorato/layout
        self.bind(pos=self.update_rect, size=self.update_rect)

    def reload_layout(self):
        self.clear_widgets()
        self.add_widget(self.searchbtn)
        self.height+=self.searchbtn.height
        self.myNode.getMyNode().addCallback(self.__got_my_user)


    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def __got_friends(self, result):
        for r in result:
            self.myNode.requestUserInfo(result[r]).addCallback(self.__got_remote_user)

    def __got_my_user(self, my_user_info):
        def printerr(e):
            print(e)

        self.myNode.remote_getKnownNodes(my_user_info).addCallback(self.__got_friends).addErrback(printerr)

    def __got_remote_user(self, result):
        add_friend_btn = Button(text="add Friend",
                                height=30,
                                )
        node_name_lbl = Label(text=result.username,
                              height=add_friend_btn.height,
                              color=(0, 0.38, 0.88, 1),
                              )
        nodeLayout = GridLayout(cols=2,
                                rows=1,
                                size_hint=(None, None),
                                width=add_friend_btn.width + node_name_lbl.width,
                                height=add_friend_btn.height
                                )

        nodeLayout.add_widget(node_name_lbl)
        nodeLayout.add_widget(add_friend_btn)

        self.height += nodeLayout.height
        self.width = nodeLayout.width
        self.add_widget(nodeLayout)
        self.bind(pos=self.update_rect, size=self.update_rect)

        print("nodeLayout added for user %s" % result.username)


        #
        # self.friends_sv = ScrollView(
        #     size_hint=(None, None),
        #     size=(200, Window.height / 2),
        #     do_scroll_x=False,
        #     do_scroll_y=True,
        #     pos_hint={'left': 0.3, 'center_y': 0.5}
        # )
        #
        # # self.friends_sv.add_widget(self.friendsFinderLayout)
