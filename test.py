from app import db
from app.models import User, Designs

designs = Designs.query()


print(designs)

