from app import db
from app.models import User


#create default account
user = User(username='sziyan', name='Zi Yan')
user.set_password('P@ssw0rd')
user.set_admin()
db.session.add(user)
db.session.commit()

#create test account
user2 = User(username='sziyang', name='Zi Yang', email='sziyang@hotmail.com')
user2.set_password('123456')
user2.set_admin()
user2.set_designer()
db.session.add(user2)
db.session.commit()

#Output confirmation
print("User {} created successfully".format(user.username))