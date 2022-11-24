# listmanager2

### features
	list of lists
	update
	delete
	add
	expand button which shows the items inside list when clicked
### Tables
	one list table and other items table.link it through foreign key.
	list table will have a id,list name ,created and edited on rows.
	item table will have same featuers along with a additional column which links it to list table.
### step by step instructions:
	
	First create a virtual environment.it assures that all dependencies are local to the project.
	activate venev.
	install flask,sqlalchemy,flask_sqlalchemy
	pip freeze it to requirements.txt file.
	import flask,sqlalchemy.sql,flask_sqlalchemy
	create db models
	In the terminal from application import db,class model name,.py file name.
	app.app.context().push()
	Create db tables = db.create.all()
	Now check whether your table has been created or not by opening new terminal and :
		sqlite3 instance/listmanager2.db
		.tables
	start making endpoints and checking it on postman.
### For get request:
	first declare the route and methods i.e ('GET','OPTIONS')
	OPTIONS method  adresses the promise error and cors error that will arise while making view.
	Always use try and exception handler.
	Now query all the available data by class model name.query.all().
	They are not in json format.so we need to store them in json format by appending it to an empty list.
					empty list name.append({'id':i.id,'list_name':i.list_name,'created_on':i.created_on,'edited_on':i.edited_on})

	jsonify the list and return it.

### For Post request:
	Declare the route and method i.e('POST','OPTIONS')
	Since POST request is to add new item,we need item we want to add in json format  by request.json('item name in the class model we have created').
	li = request.json['item_name']
	Then fill up in class model.class model name(item_name = variable name in which request.json has been  stored.)
	db.seesion.add(li)
	db.session.commit()
	Now to showcase whether it has been added or not start the for loop same as we did in GET request.
