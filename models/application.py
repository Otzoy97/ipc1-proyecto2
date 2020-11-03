from database.db import db

class User(db.Document):
    name = db.StringField(required=True, max_length=50)
    surname = db.StringField(required=True, max_length=50)
    usr = db.StringField(required=True, unique=True, max_length=50)
    pwd = db.StringField(required=True)
    reviews = db.ListField(db.ReferenceField('Review'), reverse_delete_rule=db.PULL)
    type_= db.IntField(required=True, default=0) # 0 - normal, 1 - admin

class Application(db.Document):
    title = db.StringField()
    url = db.URLField()
    cat = db.ReferenceField('Category')
    downloads = db.IntField(default = 0)
    des = db.StringField()
    price = db.DecimalField(default = 0.00)
    likes = db.IntField(default = 0)

class Category(db.Document):
    name = db.StringField(unique = True)
    apps = db.ListField(db.ReferenceField('Application', reverse_delete_rule=db.PULL))

class Review(db.Document):
    user = db.ReferenceField('User')
    txt = db.StringField()

Category.register_delete_rule(Application, 'cat', db.CASCADE)
User.register_delete_rule(Review, 'user', db.CASCADE)