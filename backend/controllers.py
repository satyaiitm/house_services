from flask import Flask
from flask import render_template, request, redirect, url_for

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")


from datetime import datetime
from flask import current_app as app
from backend.models import *


@app.route("/", methods = ["GET","POST"] )
def login():
    if request.method == "GET":
        return render_template("index.html")
    else:
        check = User.query.filter_by(uid = request.form.get("username")).first()
        if check:
            pro = cus = 0
            if check.role == 0 or check.role == 1:
                pro = db.session.query(Professional).filter(Professional.uid == request.form["username"],Professional.pwd == request.form["passw"], Professional.available > -1).first()
            elif check.role == 2 :
                cus = db.session.query(Customer).filter(Customer.uid == request.form["username"],Customer.pwd == request.form["passw"]).first()
            
            if pro and check.role == 0 :
                return redirect("/admin/home")
            elif pro and check.role == 1 :
                return redirect(url_for('professional', page = "home" , id = check.id))
            elif cus and check.role == 2 :
                return redirect(url_for('customer', page = "home" , id = check.id))
        else:
            return redirect("/")





@app.route("/signup/<usertype>", methods = ["GET", "POST"])
def signup(usertype):
    if request.method == "GET":
        serv = Service.query.all()
        return render_template("signup.html", serv = serv, usertype = usertype)
    else:

        check = User.query.filter_by(uid = request.form.get("username")).first()
        if not check :
            if usertype == "customer":
                cust = Customer(uid = request.form.get('username'), pwd = request.form.get('passw'),phone = request.form.get('phone'),name = request.form.get('name'),address = request.form.get('address'),pincode = request.form.get('pin'))
                db.session.add(cust)
                db.session.commit()
                user = User(uid = request.form.get('username'), id = cust.id , role = 2 )
                db.session.add(user)
                db.session.commit()
            else:
                pro = Professional(uid = request.form.get('uid'),pwd = request.form.get('pwd'),phone = request.form.get('phone'),name = request.form.get('name'),date_created = datetime.now(), document = request.form.get('document'), serv = request.form.get('service'),experience = request.form.get('exp'),address = request.form.get('address'), pincode = request.form.get('pin'), pro_descrip =request.form.get('pro_descrip') )
                db.session.add(pro)
                db.session.commit()
                user = User(uid = request.form.get('uid'), id = pro.id , role = 1 )
                db.session.add(user)
                db.session.commit()
    return redirect("/")
     



@app.route("/service/<action>/<int:id>", methods = ["GET","POST"])
def service(action,id):
    if request.method == "GET":

        if action == "new" :
            return render_template("service.html", action = action)
        elif action == "edit" :
            toedit = Service.query.filter_by(id = id).first()
            return render_template("service.html", action = action, toedit = toedit)
        elif action == "delete":
            serv = Service.query.filter_by(id = id).first()
            db.session.delete(serv)
            db.session.commit()
            return redirect("/admin/home")
        
    else:
        if action == "new" :
            if request.form.get('act') == "Add":
                ns = Service(sname = request.form.get("sname"), price = request.form.get("price"), timerequired = request.form.get("time"), description = request.form.get("des"))
                db.session.add(ns)
                db.session.commit()
                return redirect("/admin/home")
        elif action == "edit":
            toedit = Service.query.filter_by(id = id).first()
            toedit.sname = request.form.get("sname")
            toedit.price = request.form.get("price")
            toedit.timerequired = request.form.get("time")
            toedit.description = request.form.get("des")
            db.session.commit()
            return redirect("/admin/home")


# ------------------------- to generate_plot

def generate_plot(usertype, id):

    rating_count = [0,0,0,0,0]
    stars = [1,2,3,4,5]
    
    request_status=[0,0,0]
    l=["Closed","Requested","Rejected"]

    if usertype ==  "admin" :
        res = Request.query.all()

    elif usertype == "professional":
        res = Request.query.filter_by(rpro_id = id ).all()
        
    elif usertype == "customer":
        res = Request.query.filter_by(rcust_id = id ).all()
    
    for i in res:
        if i.rating > 0:
            rating_count[i.rating - 1] += 1
        if i.service_status == "Closed":
            request_status[0] += 1
        elif i.service_status == "Requested":
            request_status[1] += 1
        elif i.service_status == "Rejected":
            request_status[2] += 1
    plt.clf()
    plt.ylabel("Frequency")
    plt.xlabel("Rating")
    plt.bar(stars,rating_count)
    
    filename1 = f"static/summary_plot/1{usertype}{id}.png"
    plt.savefig(filename1)
    
    plt.clf()
    plt.ylabel("Frequency")
    plt.xlabel("Request status")
    plt.bar(l,request_status)
    
    filename2 = f"static/summary_plot/2{usertype}{id}.png"
    plt.savefig(filename2)

    return (filename1,filename2)






#   ---------------- 
#        Admin 
# ------------------     
        

@app.route("/admin/<page>")
def adminpages(page):
    if page == "home":
        all_request = Request.query.all()
        pro = Professional.query.filter_by(available = -1).all()
        all_service = Service.query.all()
        return render_template("admin.html",page = page, pro = pro, all_service = all_service, all_request = all_request)
    if page == "search":
        return render_template("admin.html",page = page)
    if page == "summary":
        rating_img,status_ing = generate_plot("admin", 0)
        print(rating_img,status_ing)
        return render_template("admin.html",page = page,rating_img=rating_img,status_ing=status_ing)
    

@app.route("/admin/<action>/<int:id>" )#, methods = ["POST"])
def admin_action(action , id):
    if action == "pro_approve":
        pro = Professional.query.filter_by(id = id).first()
        pro.available = 1
        db.session.commit()
        return redirect("/admin/home")
    elif action == "reject":
        return redirect("/admin/home")
    elif action == "delete":
        pro  = Professional.query.filter_by(id = id).first()
        user = User.query.filter_by(uid = pro.uid).first()
        db.session.delete(user)
        db.session.commit()
        db.session.delete(pro)
        db.session.commit()
        return redirect("/admin/home")
   



@app.route("/professional/<page>/<int:id>", methods = ["GET","POST"])
def professional(page, id):
          
    if page == "search":
        
        return render_template("professional.html", page = page, id = id)
    elif page == "summary":
        rating_img,status_ing = generate_plot("professional", id)
        print(rating_img,status_ing)
        # return redirect(url_for("summary", usertype = "professional", id =id))
        return render_template("professional.html", page = page, id = id,rating_img=rating_img,status_ing=status_ing)
    elif page == "home":
        allreq = Request.query.filter_by(rpro_id = id )
        newreq = Request.query.filter_by(rpro_id = id , service_status = 'Requested')
        
        return render_template("professional.html", page = page, id = id , newreq = newreq, allreq = allreq)
    elif page == "profile":
        customer_details = Professional.query.filter_by(id = id).first()
        return render_template("profile.html", id = id, details = customer_details, role = 1)
    elif page == "update_profile":
        toupdate = Professional.query.filter_by(id = id).first()
        toupdate.pwd = request.form.get("pwd")
        toupdate.name = request.form.get("name")
        toupdate.phone= request.form.get("phone")
        toupdate.address= request.form.get("address")
        toupdate.pincode= request.form.get("pincode")
        toupdate.pro_descrip= request.form.get("pro_descrip")
        db.session.commit()
        return redirect(url_for('professional', page = "home" , id = id))
    

@app.route("/customer/<page>/<int:id>", methods = ["GET","POST"])
def customer(page, id):
    
    if page == "search":
        all_service = Service.query.all()
        return render_template("customer.html", page = page, all_service = all_service, id = id)
    
    elif page == "summary":
        rating_img,status_ing = generate_plot("customer", id)
        print(rating_img,status_ing)
        return render_template("customer.html", page = page, id = id, rating_img=rating_img,status_ing=status_ing)
    
    elif page == "home":
        
        recomend = db.session.query(Professional).filter(Professional.serv == request.form.get("showserv"), Professional.available == 1).all()
        hist = Request.query.filter_by(rcust_id = id ).all()
        all_service = Service.query.all()
        
        return render_template("customer.html", page = page, all_service = all_service, id = id, hist = hist, recomend = recomend)
    
    elif page == "profile":
        customer_details = Customer.query.filter_by(id = id).first()
        return render_template("profile.html", id = id, details = customer_details, role = 0)
    
    elif page == "update_profile":
        toupdate = Customer.query.filter_by(id = id).first()
        toupdate.pwd = request.form.get("pwd")
        toupdate.name = request.form.get("name")
        toupdate.phone= request.form.get("phone")
        toupdate.address= request.form.get("address")
        toupdate.pincode= request.form.get("pincode")
        print(toupdate.pwd,toupdate.name,toupdate.phone,toupdate.address,toupdate.pincode)
        db.session.commit()
        return redirect(url_for('customer', page = "home" , id = id))
    
@app.route("/request/<action>/<int:cust>/<int:pro>/<int:job>") 
def servicereq(action,cust,pro,job):
    if action == "book":
        # srv = Service.query.filter_by(sname = job).first()
        req = Request(rservice_id = job ,rcust_id = cust, rpro_id = pro, date_of_request = datetime.now(), service_status = 'Requested')
        db.session.add(req)
        db.session.commit()
        return redirect(url_for('customer', page = "home" , id = cust))
    elif action == "accept":
        res = Request.query.filter_by(id = job).first()
        res.service_status = 'Accepted'
        db.session.commit()
        return redirect(url_for('professional', page = "home" , id = cust))
    elif action == "reject":
        res = Request.query.filter_by(id = job).first()
        res.service_status = 'Rejected'
        res.rpro_id = -1
        db.session.commit()
        return redirect(url_for('professional', page = "home" , id = cust))
    elif action == "cancell":
        res = Request.query.filter_by(id = job).first()
        res.service_status = 'Cancelled'
        res.date_of_completion = datetime.now()
        db.session.commit()
        return redirect(url_for('customer', page = "home" , id = res.cust.id))        

@app.route("/remark/<int:jobid>", methods = ["GET","POST"])
def remark(jobid):
    jobrequest = Request.query.filter_by(id = jobid).first()

    if request.method == "POST":
        jobrequest.rating = request.form.get("rating")
        jobrequest.pro.service_rating += int(request.form.get("rating"))
        print(type(request.form.get("rating")))
        jobrequest.remarks = request.form.get("remark")
        jobrequest.service_status = "Closed"
        db.session.commit()
        return redirect(url_for('customer', page = "home" , id = jobrequest.cust.id))
    else:
        return render_template("remark.html",request = jobrequest)

# @app.route("/summary/<usertype>/<int:id>")
# def summary(usertype, id):

#     rating_count = [0,0,0,0,0]
#     stars = [1,2,3,4,5]
    
#     request_status=[0,0,0]
#     l=["Closed","Requested","Rejected"]

#     if usertype ==  "admin" :
#         res = Request.query.all()

#     elif usertype == "professional":
#         res = Request.query.filter_by(rpro_id = id ).all()
        
#     elif usertype == "customer":
#         res = Request.query.filter_by(rcust_id = id ).all()
    


#     for i in res:
#         if i.rating > 0:
#             rating_count[i.rating - 1] += 1
#         if i.service_status == "Closed":
#             request_status[0] += 1
#         elif i.service_status == "Requested":
#             request_status[1] += 1
#         elif i.service_status == "Rejected":
#             request_status[2] += 1
#     plt.clf()
#     plt.ylabel("Frequency")
#     plt.xlabel("Rating")
#     plt.bar(stars,rating_count)
    
#     filename1 = f"static/summary_plot/1{usertype}{id}.png"
#     plt.savefig(filename1)

  


    
#     plt.clf()
#     plt.ylabel("Frequency")
#     plt.xlabel("Request status")
#     plt.bar(l,request_status)
    
#     filename2 = f"static/summary_plot/2{usertype}{id}.png"
#     plt.savefig(filename2)

#     return (filename1,filename2)



   
# if type == "course_id":
#                 plt.clf()
#                 plt.ylabel("Frequency")
#                 plt.xlabel("Marks")
#                 plt.hist(marks)

#                 plt.savefig("static/summary_plot/hist.png")
#                 picture = "static/summary_plot/hist.png"