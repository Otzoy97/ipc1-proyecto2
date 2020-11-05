from database.db import db

class Review(db.Document):
    user = db.ReferenceField('User')
    app = db.ReferenceField('Application')
    txt = db.StringField()
    rating = db.IntField()

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
    reviews = db.ListField(db.ReferenceField('Review', reverse_delete_rule=db.PULL))
    downloads = db.IntField(default = 0)
    des = db.StringField()
    price = db.DecimalField(default = 0.00)
    likes = db.IntField(default = 0)
    auth = db.BooleanField(default = True) # indica si la aplicación ya fue autorizada por un admin

class Category(db.Document):
    name = db.StringField(unique = True)
    apps = db.ListField(db.ReferenceField('Application', reverse_delete_rule=db.PULL))


Category.register_delete_rule(Application, 'cat', db.CASCADE)
User.register_delete_rule(Review, 'user', db.CASCADE)
Application.register_delete_rule(Review, 'app', db.CASCADE)