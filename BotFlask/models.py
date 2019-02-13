from BotFlask import db, loginManager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@loginManager.user_loader
def loadUser(user_id):
    return User.query.get(user_id)

#User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    profiles = db.relationship('Profile', backref = 'user')

    def getResetToken(self, expires = 1800):
        serial = Serializer(app.config['SECRET_KEY'], expires)
        return serial.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verifyResetToken(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
             user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr(self):
        return f"User('{self.username}', '{self.email}')"

#Profile Model
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    profileName = db.Column(db.String(), nullable = False)
    firstName = db.Column(db.String(20), nullable = False)
    lastName = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(), nullable = False)
    phone = db.Column(db.String(), nullable = False)
    address = db.Column(db.String(), nullable = False)
    address1 = db.Column(db.String(), nullable = True)
    city = db.Column(db.String(), nullable = False)
    state = db.Column(db.String(), nullable = False)
    zipCode = db.Column(db.String(), nullable = False)
    country = db.Column(db.String(), nullable = False)
    cc = db.Column(db.String(16), nullable = False)
    expMonth = db.Column(db.String(2), nullable = False)
    expYear = db.Column(db.String(2), nullable = False)
    cvv = db.Column(db.String(4), nullable = False)
    url = db.Column(db.String(), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr(self):
         return f"Profile('{self.profileName}', '{self.email}', '{self.address}', '{self.url}')"