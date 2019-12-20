from app import db
from app.models import User, Designs

designs = len(Designs.query.filter_by(user_name='sziyan').all())


print(designs)

