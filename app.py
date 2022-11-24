from flask import Flask,jsonify,make_response,request
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///listmanager2.db"
db = SQLAlchemy(app)


class list_names(db.Model):
    id = Column(Integer, primary_key=True)
    list_name = Column(String(40), nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    edited_on = Column(DateTime(timezone=True),
                       server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'{self.id} -> {self.list_name}'


class list_items(db.Model):
    id = Column(Integer, primary_key=True)
    list_item_name = Column(String(40), nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    edited_on = Column(DateTime(timezone=True),
                       server_default=func.now(), onupdate=func.now())
    list_id = Column(Integer, ForeignKey(list_names.id,onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'{self.id} ->{self.list_item_name}'
def get_cors_response_headers(response = None):
	if response is None:
		response = make_response()
	response.headers.add('access-control-allow-headers','*')
	response.headers.add('access-control-allow-origin','*')
	response.headers.add('access-control-allow-methods','*')
	return response
	

@app.route("/")
def appStatus():
    return 'app is working'
@app.route("/lists/<id>")
@app.route("/lists",methods=["GET","OPTIONS"])
def get_list(id = None):
	if id is None:
		try:
			if request.method == 'OPTIONS':
				get_cors_response_headers()
					
			names_of_list = list_names.query.all()
			list_json_form = []
			for i in names_of_list:
				list_json_form.append({'id':i.id,'list_name':i.list_name,'created_on':i.created_on,'edited_on':i.edited_on})
			response = jsonify(list_json_form)
			return response
		except Exception as err:
			print(f"Unexpected {err=}, {type(err)=}")
			raise

@app.route("/lists/add", methods = ["OPTIONS","POST"])
def add_to_list():
	try:
		if request.method == "OPTIONS":
			response = get_cors_response_headers()
			return response
		jsonrequest_list_name = request.json['list_name']
		li = list_names(list_name=jsonrequest_list_name)
		db.session.add(li)
		db.session.commit()
		names_of_list = list_names.query.all()
		list_json_form = []
		for i in names_of_list:
			list_json_form.append({'id': i.id, 'list_name': i.list_name,
			                      'created_on': i.created_on, 'edited_on': i.edited_on})
		response = jsonify(list_json_form)
		return response
	except Exception as err:
		print(f"Unexpected {err=}, {type(err)=}")
		raise

@app.route("/delete/<id>",methods = ['DELETE','OPTIONS'])
def delete(id):
	try:
		if request.method == 'OPTIONS':
			response = get_cors_response_headers()
			return response
		item_to_delete = list_names.query.get(id)
		names_of_list = list_names.query.all()
		name = ''
		for i in names_of_list:
			if int(i.id) == int(id):
				name += i.list_name
		db.session.delete(item_to_delete)
		db.session.commit()
		return f"List -'{name}' of ID- {id} was successfully deleted."

	except Exception as err:
		print(f'unexpected{err = }, {type(err) = }')
	

@app.route("/update", methods = ['PUT','OPTIONS'])
def update_list():
	if request.method == 'OPTIONS':
		response = get_cors_response_headers()
		return response




if __name__ == '__main__':   
	app.run(debug=True,port=8081)
