from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from application.model import *
from application.api import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gs.sqlite3'
db.init_app(app)
app.app_context().push()
api = Api(app)
# CORS(app)



from application.login import *
from application.manager import *
from application.customer import *



# Adding the resources to the API
api.add_resource(ItemAPI, "/api/item/<string:item_id>", "/api/item")
api.add_resource(CategoryAPI, "/api/category/<string:cat_id>", "/api/category")



if __name__ == '__main__':
    app.run()
    # app.run(debug=True)

