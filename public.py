from flask import *
from database import *

public=Blueprint('public',__name__)

@public.route('/',methods=['get','post'])
def home():
	if 'submit' in request.form:
		a=request.form['email']
		b=request.form['pasd']
		
		q="select * from tbl_login  where username='%s' and password='%s' and login_status=1"%(a,b)
		res=select(q)
		if res:
				session['username']=res[0]['username']
				uid=session['username']
				if res[0]['type'] == "admin":
					# flash("Logged in as admin")
					return redirect(url_for("admin.adminhome"))
				elif res[0]['type']=="user":
        
            
					Q="select * from tbl_user inner join tbl_login using(username) where username='%s'"%(uid) 
					res=select(Q)
					if res:
							session['uid']=res[0]['uid']
							uid=session['uid']
                
					return redirect(url_for("user.userhome"))
				elif res[0]['type']=="staff":
        
            
					Q="select * from tbl_user inner join tbl_login using(username) where username='%s' and u_type='staff'"%(uid) 
					res=select(Q)
					if res:
							session['uid']=res[0]['uid']
							uid=session['uid']
       

					return redirect(url_for("staff.staffhome"))
				
				elif res[0]['type']=="courier":
        
            
					Q="select * from tbl_courier inner join tbl_login using(username) where username='%s' "%(uid) 
					res2=select(Q)
					if res2:
							session['cor_id']=res2[0]['cou_id']
							cou_id=session['cor_id']
       

					return redirect(url_for("courier.cou_home"))
				
 
				else:
					flash("invalid username or password.")
		else:
			flash("invalid credentials")
                
				
                

	return render_template('home.html')



@public.route('/register',methods=['get','post'])
def register():
	if 'register' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		gender=request.form['gender']
		num=request.form['num']
		housename=request.form['add']
		street=request.form['street']
		district=request.form['district']
		pin=request.form['pin']
		date=request.form['date']
		uname=request.form['uname']
		pwd=request.form['pwd']
		r="select * from tbl_user where username='%s' or u_phone='%s'"%(uname,num)
		val=select(r)
		if val:
			flash("Username or Phonenumber already Exist")
			return redirect(url_for("public.register"))
		else:
			

			q="insert into tbl_login values ('%s','%s','user',1)"%(uname,pwd)
			insert(q)
			q="insert into tbl_user values (null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',1,'user')"%(fname,lname,gender,date,num,housename,street,district,pin,uname)
			insert(q)
			return redirect(url_for("public.register"))


	return render_template('register.html')

@public.route('/about')
def about():
    return render_template('about.html')