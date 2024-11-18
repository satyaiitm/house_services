from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    uid = db.Column(db.String, primary_key = True)
    id = db.Column(db.Integer)
    role = db.Column(db.Integer)

class Request(db.Model):
    
    id = db.Column(db.Integer, primary_key = True) 
    rservice_id = db.Column(db.Integer, db.ForeignKey("service.id"))   
    rcust_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    rpro_id = db.Column(db.Integer, db.ForeignKey("professional.id"))

    date_of_request = db.Column(db.Date, nullable = False ) 
    date_of_completion = db.Column(db.Date, nullable = True ) 
    service_status = db.Column(db.String, nullable = False) 
    remarks = db.Column(db.String) 
    rating = db.Column(db.Integer, default = 0, nullable = False ) 



class Professional(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.String, nullable = False ) 
    pwd = db.Column(db.String, nullable = False )
    name = db.Column(db.String, nullable = False ) 
    phone = db.Column(db.Integer, nullable = False ) 
    date_created = db.Column(db.Date, nullable = True ) 
    document = db.Column(db.String, nullable = True ) 
    pro_descrip = db.Column(db.String, nullable = True )
    experience = db.Column(db.Integer, nullable = True )
    address = db.Column(db.String, nullable = False )
    pincode = db.Column(db.Integer, nullable = False )
    role = db.Column(db.Integer, default = 1, nullable = False)
    available = db.Column(db.String,default = "Waiting", nullable = False)
    average_rating = db.Column(db.Float,default = 0, nullable = True)
    pserve = db.relationship("Request", backref = "pro")
    serv = db.Column(db.Integer, db.ForeignKey("service.id"))
    

class Customer(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.String, nullable = False ) 
    pwd = db.Column(db.String, nullable = False ) 
    name = db.Column(db.String, nullable = False ) 
    phone = db.Column(db.Integer, nullable = False ) 
    address = db.Column(db.String, nullable = False ) 
    pincode = db.Column(db.Integer, nullable = False ) 
    available = db.Column(db.String, default = "Available", nullable = False)
    cserve = db.relationship("Request", backref = "cust")


class Service(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    sname = db.Column(db.String, nullable = False ) 
    price = db.Column(db.Integer, nullable = True ) 
    timerequired = db.Column(db.Integer, nullable = True ) 
    description = db.Column(db.String, nullable = True ) 
    servepro = db.relationship("Professional", backref = "sp")
    sserve = db.relationship("Request", backref = "ss")



    