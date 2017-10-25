from kivy.uix.gridlayout import GridLayout

class FriendsFinderLayout(GridLayout):
    def __init__(self, myNode, *args):
        super(FriendsFinderLayout, self).__init__(*args)
        self.myNode = myNode
        myNode.getMyNode().addCallback(self.__got_my_user)
        self.size_hint = (None, None)
        self.cols = 1
        self.width = 200
        self.padding = 10
        self.spacing = 20

        self.bind(minimum_height=self.setter('height'))
        self.myNode.populateKnownNodes()

    def __got_friends(self, result):
        print("FRIENDS FINDER RESULTS")
        print(result)
        print("######################")


    def __got_my_user(self, my_user_info):
        self.myNode.remote_getKnownNodes(my_user_info).addCallback(self.__got_friends)
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