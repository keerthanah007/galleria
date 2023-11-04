from flask import Flask
from public import public
from admin import admin
from user import user
from staff import staff
from courier import courier

app=Flask(__name__)



app.secret_key="bhsxeduiiotys"
app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(staff)
app.register_blueprint(courier)




app.run(debug=True,port=5067)
