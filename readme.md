[commands]
pip install -r requirements.txt

[flask migrate]
flask db init 
flask db migrate -m "initial commit"
flask db upgrade
