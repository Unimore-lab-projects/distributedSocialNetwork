from twistar.dbobject import DBObject
from twistar.registry import Registry

from twisted.spread import pb


class Known_node(DBObject, pb.Copyable):
    TABLENAME = "known_nodes"


Known_node.validatesPresenceOf('user_id')
Known_node.validatesUniquenessOf('user_id')
Known_node.validatesPresenceOf('address')
Known_node.validatesPresenceOf('port')
Known_node.validatesPresenceOf('last_update')


class Friend(DBObject):
    # BELONGSTO = [{'name': 'comment', 'class_name': 'Comment', 'foreign_key': 'user_id'}]
    pass

Friend.validatesUniquenessOf('user_id')
Friend.validatesPresenceOf('user_id')
Friend.validatesLengthOf('username', range=xrange(1, 16))


class Comment(DBObject):
    # HASONE = [{'name': 'friend', 'class_name': 'Friend', 'foreign_key': 'user_id'}]
    pass

# Registry.register(Comment, Friend)
Comment.validatesPresenceOf('comment_id')
Comment.validatesPresenceOf('post_id')
Comment.validatesPresenceOf('user_id')
Comment.validatesUniquenessOf('comment_id')
Comment.validatesLengthOf('content', range=xrange(0, 512))
Comment.validatesLengthOf('username', range=xrange(1, 16))


class Post(DBObject):
    pass


Post.validatesUniquenessOf('post_id')
Post.validatesPresenceOf('post_id')
Post.validatesLengthOf('text_content', range=xrange(0, 512))


class My_user(DBObject,pb.Copyable):
    TABLENAME = "my_user"


My_user.validatesUniquenessOf('user_id')
My_user.validatesPresenceOf('user_id')
My_user.validatesPresenceOf('username')
My_user.validatesLengthOf('username', range=xrange(1, 16))
