from flask import *
from database import *
import uuid


staff=Blueprint('staff',__name__)

@staff.route("/staffhome")
def staffhome():
    q="select * from tbl_user where uid='%s'"%(session['uid'])
    res=select(q)
    print(res)
    name=res[0]['u_fname']+"\t"+res[0]['u_lname']
    print(name)
    return render_template("staffhome.html",name=name)

@staff.route("/about")
def about():
    return render_template("about.html")



@staff.route("/scourier",methods=['get','post'])
def scourier():
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
		return redirect(url_for('staff.scourier'))

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
		return redirect(url_for('staff.scourier'))

	if action=="active":
		q="update tbl_courier set cou_status='1' where cou_id='%s'"%(id)
		update(q)
		q="update tbl_login set login_status='1' where username='%s'"%(uid)
		update(q)
		return redirect(url_for('staff.scourier'))

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
		return redirect(url_for('staff.scourier'))

	return render_template("scourier.html",data=data)

@staff.route("/additem",methods=['get','post'])
def additem():
    uid=session['uid']
    data={}
   
    q="select * from tbl_subcategory"
    res=select(q)
    data['subdrop']=res
    
    q="select * from tbl_item inner join tbl_subcategory using(sub_id) where uid='%s'"%(uid)
    res=select(q)
    data['views']=res
    
    
    
    
    if 'submit' in request.form:
        sub=request.form['sub']
        aname=request.form['aname']
        des=request.form['des']
        price=request.form['price']
        per=(int(price)*20)/100 
        finalcost=int(per)+int(price)
        i=request.files['img']
        uid=session['uid']
        path="static/image/"+str(uuid.uuid4())+i.filename
        i.save(path)
        q="insert into tbl_item values (null,'%s','%s','%s','%s','%s','%s','pending','%s')"%(sub,uid,aname,des,price,path,finalcost)
        insert(q)
        return redirect(url_for('staff.additem'))
    
    
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
        
    else:
        action=None
        
    if action=="update":
        q="select * from tbl_item where item_id='%s'"%(id)
        res=select(q)
        data['up']=res
    
    if 'update' in request.form:
        sub=request.form['sub']
        aname=request.form['aname']
        des=request.form['des']
        price=request.form['price']
        per=(int(price)*20)/100 
        finalcost=int(per)+int(price)
        i=request.files['img']
        path="static/image/"+str(uuid.uuid4())+i.filename
        i.save(path)
        q="update tbl_item set sub_id='%s',item_name='%s',item_des='%s',item_price='%s',item_image='%s',finalcost='%s' where item_id='%s'"%(sub,aname,des,price,path,finalcost,id)
        update(q)
        return redirect(url_for('staff.additem'))
                
		
        
    return render_template("additem.html",data=data)

@staff.route('/gallery')
def gallery():
    data={}
    q="select * from tbl_item inner join tbl_subcategory using(sub_id) inner join tbl_user using(uid) where uid <> '%s'"%(session['uid'])
    res=select(q)
    if res:
        data['item']=res
        

    
    return render_template("gallery.html",data=data)

@staff.route('/single',methods=['get','post'])
def single():
    data={}
    itemid = request.args['item_id']
    q="SELECT * FROM `tbl_item`,`tbl_user`,`tbl_category`,`tbl_subcategory` WHERE `tbl_item`.uid=`tbl_user`.uid AND `tbl_item`.sub_id=`tbl_subcategory`.sub_id  AND `tbl_subcategory`.cat_id=`tbl_category`.cat_id and item_id='%s'"%(itemid)
    data['spec'] = select(q)
    
    if 'btn' in request.form:
        q="select * from tbl_cart_master where cart_status='pending' and uid='%s'"%(session['uid'])
        res=select(q)
        if res:
            cm_id=res[0]['cm_id']
        else:
            q="insert into tbl_cart_master values (null,'%s','pending',0)"%(session['uid'])
            cm_id=insert(q)
        q="select * from tbl_cart_child where cm_id='%s' and item_id='%s'"%(cm_id,itemid)
        val=select(q)
        if val:
            flash("Already in Cart")
        else:
            q="insert into tbl_cart_child values(null,'%s','%s')"%(cm_id,itemid)
            insert(q)
        q="update tbl_cart_master set c_tot_amount =c_tot_amount+(select finalcost from tbl_item where item_id='%s') where cm_id='%s'"%(itemid,cm_id)
        update(q)
        return redirect(url_for("user.cart"))
    return render_template("single.html",data=data)
    

@staff.route('/cart',methods=['get','post'])
def cart():
    data={}
    q="select * from tbl_cart_child inner join tbl_cart_master using(cm_id) inner join tbl_item using(item_id)"
    res=select(q)
    data['item']=res
    
    
    
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
        cmid=request.args['cmid']
        ccid=request.args['ccid']
        
    else:
        action=None
        
    if action =="delete":
        q="delete from tbl_cart_child where item_id='%s'and cc_id='%s'"%(id,ccid)
        delete(q)
        c="select * from tbl_item where item_id='%s'"%(id)
        res1=select(c)
        price=res1[0]['finalcost']
        p="update tbl_cart_master set c_tot_amount=c_tot_amount-'%s'where cm_id='%s'"%(price,cmid)
        update(p)
        return redirect(url_for("staff.cart"))
        
    return render_template("cart.html",data=data)





@staff.route('/payment',methods=['get','post'])
def payment():
    data={}
    uid=session['uid']
    q="select * from tbl_card where uid='%s'"%(uid)
    res=select(q)
    data['card']=res
   
    
    if 'submit' in request.form:
       cno=request.form['cno']
       cown=request.form['cown']
       exp=request.form['exp']
       uid=session['uid']
       q="insert into tbl_card values (null,'%s','%s','%s','%s','1')"%(uid,cno,cown,exp)
       insert(q)
       return redirect(url_for('staff.payment'))
       
    return render_template("payment.html",data=data)
