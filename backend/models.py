from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    uid = db.Column(db.String, primary_key = True)
    id = db.Column(db.Integer)
    role = db.Column(db.Integer)

class Request(db.Model):
    
    id = db.Column(db.Integer, primary_key = True) 
    rservice_id = db.Column(db.Integer, db.ForeignKey("service.id"))   # db.ForeignKey(service.service_id , ondelete='CASCADE')
    rcust_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    rpro_id = db.Column(db.Integer, db.ForeignKey("professional.id"))

    date_of_request = db.Column(db.Date, nullable = True ) #F
    date_of_completion = db.Column(db.Date, nullable = True ) #F
    service_status = db.Column(db.String, nullable = True) #F complete ->0 , approved -> 1 , panding approval -> -1
    remarks = db.Column(db.String) 
    rating = db.Column(db.Integer, default = 0, nullable = True ) # Default = 0



class Professional(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.String, nullable = True ) #F
    pwd = db.Column(db.String, nullable = True ) #F
    name = db.Column(db.String, nullable = True ) #F
    phone = db.Column(db.Integer, nullable = True ) #F
    date_created = db.Column(db.Date, nullable = True ) #F
    document = db.Column(db.String, nullable = True ) #F
    pro_descrip = db.Column(db.String, nullable = True )
    experience = db.Column(db.Integer, nullable = True ) #F
    address = db.Column(db.String, nullable = True ) #F
    pincode = db.Column(db.Integer, nullable = True ) #F
    role = db.Column(db.Integer, default = 1, nullable = True) #F
    available = db.Column(db.String,default = "Waiting", nullable = True)#
    service_rating = db.Column(db.Integer,default = 0, nullable = True) #
    pserve = db.relationship("Request", backref = "pro")
    serv = db.Column(db.Integer, db.ForeignKey("service.id"))
    

class Customer(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.String, nullable = False ) #F
    pwd = db.Column(db.String, nullable = False ) #F
    name = db.Column(db.String, nullable = True ) #F
    phone = db.Column(db.Integer, nullable = True ) #F
    address = db.Column(db.String, nullable = True ) #F
    pincode = db.Column(db.Integer, nullable = True ) #F
    cserve = db.relationship("Request", backref = "cust")


class Service(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    sname = db.Column(db.String, nullable = True ) #F
    price = db.Column(db.Integer, nullable = True ) #F
    timerequired = db.Column(db.Integer, nullable = True ) #F
    description = db.Column(db.String, nullable = True ) #F
    servepro = db.relationship("Professional", backref = "sp")
    sserve = db.relationship("Request", backref = "ss")



    