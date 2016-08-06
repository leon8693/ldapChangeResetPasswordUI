from app import app
from app import db

db.create_all()
app.run(debug=True,host='0.0.0.0')
