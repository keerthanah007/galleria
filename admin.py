from flask import *
from database import *
import datetime

admin=Blueprint('admin',__name__)

@admin.route("/adminhome")       
def adminhome():
	return render_template("adminhome.html")


@admin.route('/about')
def about():
    return render_template('about.html')


@admin.route("/addstaff",methods=['get','post'])
def addstaff():

	data={}
	q="select * from tbl_user inner join tbl_login using(username) where u_type='staff'"
	res=select(q)
	data['staff']=res
    

	if 'submit' in request.form:
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
		r="select * from tbl_login where username='%s'"%(uname)
		val=select(r)
		if val:
			flash("Username  already Exist")
			return redirect(url_for("admin.addstaff"))
		else:
			
				q="insert into tbl_login values ('%s','%s','staff',1)"%(uname,pwd)
				insert(q)
				q="insert into tbl_user values (null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',1,'staff')"%(fname,lname,gender,date,num,housename,street,district,pin,uname)
				insert(q)
				return redirect(url_for('admin.addstaff'))



	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
		uid=request.args['uid']
	

	else:
		action=None
	if action=="inactive":
		q="update tbl_user set u_status='0' where uid='%s'"%(id)
		update(q)
		q="update tbl_login set login_status='0' where username='%s'"%(uid)
		update(q)
		return redirect(url_for('admin.addstaff'))

	if action=="active":
		q="update tbl_user set u_status='1' where uid='%s'"%(id)
		update(q)
		q="update tbl_login set login_status='1' where username='%s'"%(uid)
		update(q)
		return redirect(url_for('admin.addstaff'))

	if action=="update":
		q="select * from tbl_user where uid='%s'"%(id)
		res=select(q)
		data['up']=res

	if 'update' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		gender=request.form['gender']
		dob=request.form['date']
		phone=request.form['num']
		hname=request.form['add']
		street=request.form['street']
		district=request.form['district']
		pin=request.form['pin']
		print(fname)	
        


		q="update tbl_user set u_fname='%s',u_lname='%s',u_gender='%s',u_dob='%s',u_phone='%s',u_hname='%s',u_street='%s',u_district='%s',u_pin='%s' where uid='%s'"%(fname,lname,gender,dob,phone,hname,street,district,pin,id)
		update(q)
		return redirect(url_for('admin.addstaff'))
    
	return render_template("addstaff.html",data=data)



@admin.route("/custreport",methods=['get','post'])
def custreport():
	data={}
	if 'btn' in request.form:
		search='%'+request.form['search']+'%'
		q="select * from tbl_user where u_fname like '%s' "%(search)
	else:
		q="select * from tbl_user"
	res=select(q)
	if res:
		data['cus']=res

	return render_template("custreport.html",data=data)


@admin.route("/print_cus",methods=['get','post'])
def print_cus():
    
    data={}
    q="select * from tbl_user"
    res=select(q)
    data['cus']=res
    return render_template("print_cus.html",data=data)



@admin.route("/print_staff",methods=['get','post'])
def print_staff():
    
    data={}
    q="select * from tbl_user where u_type='staff'"
    res=select(q)
    data['staff']=res
    return render_template("print_staff.html",data=data)






@admin.route('/admin_orders',methods=['post','get'])	
def admin_orders():
    data={}
    if "btn" in request.form:
        daily=request.form['daily']
        if request.form['monthly']=="":
            monthly=""
        else:
            monthly=request.form['monthly']+'%'
        print(monthly)
        
        q="SELECT * FROM `tbl_cart_master`,`tbl_cart_child`,`tbl_item`,`tbl_user` WHERE (`tbl_cart_master`.cm_id=`tbl_cart_child`.cm_id AND `tbl_cart_child`.item_id=`tbl_item`.item_id and tbl_cart_master.uid=tbl_user.uid and `order_date` like '%s'  ) or  (`tbl_cart_master`.cm_id=`tbl_cart_child`.cm_id AND `tbl_cart_child`.item_id=`tbl_item`.item_id and tbl_cart_master.uid=tbl_user.uid  and  `order_date` like '%s' ) "%(daily,monthly)
        res=select(q)
        print(q)
        data['report']=res
        session['res']=res
        r=session['res']

    else:
        q="SELECT * FROM `tbl_cart_master`,`tbl_cart_child`,`tbl_item`,`tbl_user` WHERE `tbl_cart_master`.cm_id=`tbl_cart_child`.cm_id AND `tbl_cart_child`.item_id=`tbl_item`.item_id and tbl_cart_master.uid=tbl_user.uid and tbl_cart_master.cart_status <> 'pending'"
        print(q)
        res=select(q)
        data['report']=res

        q="SELECT sum(finalcost) as cost FROM `tbl_cart_master`,`tbl_cart_child`,`tbl_item`,`tbl_user` WHERE `tbl_cart_master`.cm_id=`tbl_cart_child`.cm_id AND `tbl_cart_child`.item_id=`tbl_item`.item_id and tbl_cart_master.uid=tbl_user.uid and tbl_cart_master.cart_status <> 'pending'"
        res2=select(q)
        print("sssssssssssssssssssssssssssssssssssss",res2)
        session['cost']=res

    cmdata={}
    for i,cmrow in enumerate(data['report']):
        if cmrow['cm_id'] not in cmdata:
            cmdata[cmrow['cm_id']] = [];
        cmdata[cmrow['cm_id']].append(cmrow)

    newdata=[]
    for cm in cmdata.values(): 
        newcmdict = {}
        for row in cm: 
            newcmdict['cm_id'] = row['cm_id']
            newcmdict['c_tot_amount'] = row['c_tot_amount']
            newcmdict['order_data'] = row['order_date']
            newcmdict['u_fname'] = row['u_fname']
            newcmdict['u_lname'] = row['u_lname']
            if 'cart_children' not in newcmdict: 
                newcmdict['cart_children'] = [] 
            newcmdict['cart_children'].append(row)
        newdata.append(newcmdict)

        
    __import__('pprint').pprint(newdata)

    return render_template('admin_orders.html',data=newdata)



@admin.route("/print_sales",methods=['get','post'])
def print_sales():
    data={}

    if len(request.args.to_dict()) > 0:
        daily=request.args['daily']
        if request.args['monthly']=="":
            monthly=""
        else:
            monthly='%'+request.args['monthly']+'%'
        print(monthly)
        q="SELECT * FROM `tbl_cart_master`,`tbl_cart_child`,`tbl_item`,`tbl_user` WHERE (`tbl_cart_master`.cm_id=`tbl_cart_child`.cm_id AND `tbl_cart_child`.item_id=`tbl_item`.item_id and tbl_cart_master.uid=tbl_user.uid and tbl_cart_master.cart_status='paid'  and  `order_date` like '%s'  ) or  (`tbl_cart_master`.cm_id=`tbl_cart_child`.cm_id AND `tbl_cart_child`.item_id=`tbl_item`.item_id and tbl_cart_master.uid=tbl_user.uid and tbl_cart_master.cart_status='paid'  and  `order_date` like '%s' ) "%(daily,monthly)
        res=select(q)
        data['r']=res
        session['res']=res
        r=session['res']
        q="SELECT sum(c_tot_amount) as tot FROM `tbl_cart_master`,`tbl_cart_child`,`tbl_item`,`tbl_user` WHERE (`tbl_cart_master`.cm_id=`tbl_cart_child`.cm_id AND `tbl_cart_child`.item_id=`tbl_item`.item_id and tbl_cart_master.uid=tbl_user.uid and tbl_cart_master.cart_status='paid'  and  `order_date` like '%s'  ) or  (`tbl_cart_master`.cm_id=`tbl_cart_child`.cm_id AND `tbl_cart_child`.item_id=`tbl_item`.item_id and tbl_cart_master.uid=tbl_user.uid and tbl_cart_master.cart_status='paid'  and  `order_date` like '%s' ) "%(daily,monthly)
        data['total']=select(q)[0]['tot']
    else:
        q="SELECT * FROM `tbl_cart_master`,`tbl_cart_child`,`tbl_item`,`tbl_user` WHERE `tbl_cart_master`.cm_id=`tbl_cart_child`.cm_id AND `tbl_cart_child`.item_id=`tbl_item`.item_id and tbl_cart_master.uid=tbl_user.uid and tbl_cart_master.cart_status <> 'pending'"
        data['r']=select(q)
        q="SELECT sum(c_tot_amount) as tot FROM `tbl_cart_master`,`tbl_cart_child`,`tbl_item`,`tbl_user` WHERE `tbl_cart_master`.cm_id=`tbl_cart_child`.cm_id AND `tbl_cart_child`.item_id=`tbl_item`.item_id and tbl_cart_master.uid=tbl_user.uid and tbl_cart_master.cart_status <> 'pending'"
        data['total']=select(q)[0]['tot']

    return render_template("print_sales.html",data=data)


@admin.route("/assign_cou",methods=['get','post'])
def assign_cou():
	cm_id=request.args['cm_id']
	data={}
	q="select * from tbl_courier where cou_status='1'"
	data['cou']=select(q)

	if 'submit' in request.form:
		cou=request.form['cou']
		q="insert into tbl_delivery values (null,'%s','%s',curdate(),curtime())"%(cou,cm_id)
		insert(q)
		p="update tbl_cart_master set cart_status='assigned' where cm_id='%s'"%(cm_id)
		update(p)
		print(p)
		return redirect(url_for('admin.admin_orders'))
    
		

		


	return render_template("assign_cou.html",data=data)

































@admin.route("/addcategory",methods=['get','post'])
def addcategory():
	data={}
	q="select * from tbl_category"
	res=select(q)
	data['cat']=res

	if 'submit' in request.form:
		name=request.form['cat_name']
		r="select * from tbl_category where cat_name='%s'"%(name)
		val=select(r)
		if val:
			flash ("Category already added")
			
		else:
			q="insert into tbl_category values (null,'%s',1)"%(name)
			insert(q)	
		return redirect(url_for("admin.addcategory"))

	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']


	else:
		action=None


	if action=="inactive":
		q="update tbl_category set cat_status='0' where cat_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.addcategory'))

	if action=="active":
		q="update tbl_category set cat_status='1' where cat_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.addcategory'))

	if action=="update":
		q="select * from tbl_category where cat_id='%s'"%(id)
		res=select(q)
		data['up']=res

	if 'update' in request.form:
		name=request.form['cat_name']

		q="update tbl_category set cat_name='%s' where cat_id='%s'"%(name,id)
		update(q)
		return redirect(url_for('admin.addcategory'))

	return render_template("addcategory.html",data=data)






@admin.route("/addsubcat",methods=['get','post'])
def addsubcat():
	data={}
	q="select * from tbl_category"
	res=select(q)
	data['cat']=res
   



	if 'submit' in request.form:
		name=request.form['sub_name']
		cat=request.form['cat']
		r="select * from tbl_subcategory  where sub_name='%s'"%(name)
		val=select(r)
		if val:
			flash ("Sub-category already added")
		else:
			q="insert into tbl_subcategory values (null,'%s','%s',1)"%(cat,name)
			insert(q)
		return redirect(url_for("admin.addsubcat"))

	q="select * from tbl_subcategory inner join tbl_category using (cat_id)"
	res1=select(q)
	data['sub']=res1


	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	

	else:
		action=None


	if action=="inactive":
		q="update tbl_subcategory set sub_status='0' where sub_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.addsubcat'))

	if action=="active":
		q="update tbl_subcategory set sub_status='1' where sub_id='%s'"%(id)
		update(q)
		return redirect(url_for('admin.addsubcat'))

	if action=="update":
		q="select * from tbl_subcategory where sub_id='%s'"%(id)
		res=select(q)
		data['up']=res

	if 'Update' in request.form:
		
		sub_name=request.form['sub_name']
		q="update tbl_subcategory set sub_name='%s' where sub_id='%s'"%(sub_name,id)
		update(q)
		return redirect(url_for('admin.addsubcat'))


	return render_template("addsubcat.html",data=data)








@admin.route("/addcourier",methods=['get','post'])
def addcourier():
    data={}
    q="select * from tbl_courier inner join tbl_login using(username)"
    res=select(q)
    data['courier']=res

    if 'submit' in request.form:
        name=request.form['name']
        num=request.form['num']
        district=request.form['district']
        uname=request.form['uname']
        pwd=request.form['pwd']
        q="insert into tbl_login values ('%s','%s','courier',1)"%(uname,pwd)
        insert(q)
        q="insert into tbl_courier values(null,'%s','%s','%s','%s',1)"%(uname,name,num,district)
        insert(q)
        return redirect(url_for('admin.addcourier'))

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
        uid=request.args['uid']

    else:
        action=None


    if action=="inactive":
        
        q="update tbl_courier set cou_status='0' where cou_id='%s'"%(id)
        update(q)
        q="update tbl_login set login_status='0' where username='%s'"%(uid)
        update(q)
        q="select * from tbl_cart_master inner join tbl_delivery using(cm_id) where cou_id='%s'"%(id)
        res=select(q)
        if res:	
            for cm in res:
                q="update tbl_cart_master set cart_status='paid' where cm_id='%s' and cart_status='assigned'"%(cm['cm_id'])
                update(q)
                q="delete from tbl_delivery where cm_id='%s'"%(cm['cm_id'])
                delete(q)
        return redirect(url_for('admin.addcourier'))

    if action=="active":
        q="update tbl_courier set cou_status='1' where cou_id='%s'"%(id)
        update(q)
        q="update tbl_login set login_status='1' where username='%s'"%(uid)
        update(q)
        return redirect(url_for('admin.addcourier'))

    if action=="update":
        q="select * from tbl_courier where cou_id='%s'"%(id)
        res=select(q)
        data['up']=res

    if 'update' in request.form:
        name=request.form['name']
        num=request.form['num']
        district=request.form['district']

        q="update tbl_courier set cou_name='%s',cou_phone='%s',cou_place='%s' where cou_id='%s'"%(name,num,district,id)
        update(q)
        return redirect(url_for('admin.addcourier'))

    return render_template("addcourier.html",data=data)


@admin.route("/approve")
def approve():
    data={}
    q="SELECT *FROM tbl_item INNER JOIN tbl_subcategory USING (sub_id) INNER JOIN tbl_user USING (uid) "
    res=select(q)
    print(q)
    print(res)
    data['art']=res
    
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
        print(action,id)
        print("********")
    else:
        action=None
        
    if action=="approved":
        q="update tbl_item set item_approval='approved' where item_id='%s'"%(id)
        update(q)
        return redirect(url_for('admin.approve'))
    
    if action=="rejected":
        q="update tbl_item set item_approval='rejected' where item_id='%s'"%(id)
        update(q)
        return redirect(url_for('admin.approve'))
  
    return render_template('approve.html',data=data)

@admin.route("/approveform")
def approve_art():
    data={}
    q="SELECT *FROM tbl_item INNER JOIN tbl_subcategory USING (sub_id) INNER JOIN tbl_user USING (uid) "
    res=select(q)
    data['art']=res

    percentage = request.args['profitperc']
    item_id = request.args['item_id']

    if percentage != None:
        percentage = int(percentage)
        if percentage < 10 or percentage > 100:
            flash("invalid value")
        else:
           q="update tbl_item set item_approval='approved',finalcost=item_price+(item_price*%s) where item_id='%s'"%(percentage/100,item_id)
           update(q)
           return redirect(url_for('admin.approve'))
    else:
        flash("Profit percentage is empty")

    return render_template('approve.html',data=data)

@admin.route("/addexb",methods=['get','post'])
def addexb():
    data={}
    q="select * from tbl_exhibition where ex_date >= curdate()"
    res=select(q)
    data['views']=res
    
    # for exb in data:
    #     data['isFinished'] = data['']
    
    if 'submit' in request.form:
        name=request.form['name']
        venu=request.form['venu']
        date=request.form['date']
        
        fee=request.form['fee']
        
        if(datetime.datetime.strptime(date, '%Y-%m-%d') > datetime.datetime.today()):
            q="insert into tbl_exhibition values (null,'%s','%s','%s','%s')"%(date,venu,fee,name)
            insert(q)
            return redirect(url_for('admin.addexb'))
        else:
            flash ("Not valid date")
            
            
    
    
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    
    else:
        action=None
    
    if action=='update':
        q="select * from tbl_exhibition where ex_id='%s'"%(id)
        res=select(q)
        data['up']=res
    if 'update' in request.form:
        name=request.form['name']
        venu=request.form['venu']
        date=request.form['date']
        fee=request.form['fee']
        q="update tbl_exhibition set ex_name='%s',ex_date='%s',ticket='%s',ex_venu='%s' where ex_id='%s'"%(name,date,fee,venu,id)
        insert(q)
        return redirect(url_for('admin.addexb'))
  
  
    return render_template('addexb.html',data=data)


@admin.route("/artexb",methods=['post','get'])
def artexb():
    data={}
    id=request.args['id']
    q="SELECT * FROM `tbl_item_ex` INNER JOIN tbl_item USING (`item_id`) INNER JOIN `tbl_exhibition` USING (`ex_id`) INNER JOIN `tbl_user` USING (uid) INNER JOIN  `tbl_subcategory` USING (sub_id) where ex_id='%s'  "%(id)
    res1=select(q)
    data['views']=res1
    
    q="select * from tbl_item_ex inner join tbl_item using (item_id) inner join tbl_exhibition using (ex_id) inner join tbl_user using (uid) "
    res=select(q)
    data['exbview']=res    
    
    id=request.args['id']
    data['id']=id
    
    evenu=request.args['evenu']
    data['evenu']=evenu
    
    edate=request.args['edate']
    data['edate']=edate
    
    ticket=request.args['ticket']
    data['ticket']=ticket
    
    
    q="select * from tbl_item where item_id not in (select item_id from tbl_item_ex) and item_approval='approved'"
    res=select(q)
    data['itemdrop']=res
    
    if "action" in request.args:
        action=request.args['action']
        iid=request.args['iid']
        
    else:
        action=None
        
    if action=='remove':
        q="delete from tbl_item_ex where item_id='%s'"%(iid)
        delete(q)
        return redirect(url_for('admin.artexb',evenu=evenu,edate=edate,ticket=ticket,id=id))
    
    
    if "art" in request.form:
        item=request.form['item']
        
        q="insert into tbl_item_ex values(null,'%s','%s')"%(item,id)
        insert(q)
        return redirect(url_for('admin.artexb',evenu=evenu,edate=edate,ticket=ticket,id=id))
    
   
        
    return render_template('artexb.html',data=data)


    
    


  
