from flask import *
from database import *
import uuid

user=Blueprint('user',__name__)

@user.route("/userhome")
def userhome():
    q="select * from tbl_user where uid='%s'"%(session['uid'])
    res=select(q)
    print(res)
    name=res[0]['u_fname']+"\t"+res[0]['u_lname']
    print(name)
    return render_template("userhome.html",name=name)

@user.route("/about")
def about():
    return render_template("about.html")

@user.route("/additem",methods=['get','post'])
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
        per=(int(price)*0.20)/100 
        finalcost=0
        i=request.files['img']
        uid=session['uid']
        path="static/image/"+str(uuid.uuid4())+i.filename
        i.save(path)
        r="select * from tbl_item where item_name='%s'or item_image='%s'"%(aname,path)
        val=select(r)
        if val:
            flash("Art Already Added")
        else:
            q="insert into tbl_item values (null,'%s','%s','%s','%s','%s','%s','pending','%s')"%(sub,uid,aname,des,price,path,finalcost)
            insert(q)
        return redirect(url_for('user.additem'))
    
    
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
        return redirect(url_for('user.additem'))
                
		
        
    return render_template("additem.html",data=data)

@user.route('/gallery',methods=['get','post'])
def gallery():
    data={}
    # q="select * from tbl_item where item_id in ( select item_id from tbl_cart_master inner join tbl_cart_child using (cm_id) where cart_status='paid')"
    # val=select(q)
    # itemid = val[0]['item_id']
    if 'btn' in request.form:
        search='%'+request.form['search']+'%'
        q="select * from tbl_item inner join tbl_subcategory using(sub_id) inner join tbl_category using(cat_id) inner join tbl_user using(uid) where uid <>  '%s'and item_approval='approved' and sub_status='1'and cat_status='1' and ( item_id not in ( select item_id from tbl_cart_master inner join tbl_cart_child using (cm_id) where cart_status='paid' ) and item_name like '%s' ) or  ( item_id not in ( select item_id from tbl_cart_master inner join tbl_cart_child using (cm_id) where cart_status <> 'pending' ) and u_fname like '%s' )  "%(session['uid'],search,search)
    else:
        q="select * from tbl_item inner join tbl_subcategory using(sub_id)  inner join tbl_category using(cat_id) inner join tbl_user using(uid) where uid <>  '%s'and item_approval='approved'and sub_status='1' and cat_status='1' and item_id not in ( select item_id from tbl_cart_master inner join tbl_cart_child using (cm_id) where cart_status <> 'pending' ) "%(session['uid'])
    res=select(q)
    if res:
        data['item']=res
    
       

    
    return render_template("gallery.html",data=data)

@user.route('/single',methods=['get','post'])
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
            q="insert into tbl_cart_master values (null,'%s','pending',0,curdate())"%(session['uid'])
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
    

@user.route('/cart',methods=['get','post'])
def cart():
    data={}
    q="select * from tbl_cart_child inner join tbl_cart_master using(cm_id) inner join tbl_item using(item_id) where cart_status='pending' and tbl_cart_master.uid='%s'"%(session['uid'])
    res=select(q)
    data['item']=res
    data['len']=len(res)
    
    
    
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
        return redirect(url_for("user.cart"))
        
    return render_template("cart.html",data=data)





@user.route('/payment',methods=['get','post'])
def payment():
    data={}
    cm_id=request.args['cm_id']
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
       return redirect(url_for('user.payment',cm_id=cm_id))
   
    if 'payment' in request.form:
        cno=request.form['cno']
        
        q="insert into tbl_payment values (null,'%s',curdate(),'paid')"%(cno)
        insert(q)
        q="update tbl_cart_master set cart_status='paid' where cm_id='%s'"%(cm_id)
        update(q)

        q="select * from tbl_cart_child where cm_id='%s'"%(cm_id)
        children = select(q)
        for cc in children:
            q="update tbl_item set item_approval='paid' where item_id in (select item_id from tbl_cart_child where cc_id='%s' )"%(cc['cc_id'])
            update(q)

        flash("Payment Successfull")
        return redirect(url_for('user.userhome'))

    return render_template("payment.html",data=data)




@user.route("/user_orders")
def user_orders():
    data={}
    # q="""
        # SELECT * FROM `tbl_cart_master`,`tbl_cart_child`,`tbl_item` 
        # WHERE `tbl_cart_master`.cm_id=`tbl_cart_child`.cm_id 
            # AND `tbl_cart_child`.item_id=`tbl_item`.item_id 
            # AND tbl_cart_master.uid='%s' 
            # AND tbl_cart_master.cart_status <> 'pending'"""%(session['uid'])

    q="SELECT * FROM `tbl_cart_master` WHERE tbl_cart_master.uid='%s' AND tbl_cart_master.cart_status <> 'pending'"%(session['uid'])
    data['res']=select(q)
    for i,cm in enumerate(data['res']):
        q="SELECT * FROM `tbl_cart_child` INNER JOIN `tbl_item` USING(item_id) WHERE tbl_cart_child.cm_id='%s'"%(cm['cm_id'])
        data['res'][i]['cart_children'] = select(q)

    __import__('pprint').pprint(data)

    return render_template("user_orders.html",data=data)


@user.route("/user_bill")
def user_bill():
    data={}
    cm_id=request.args['cm_id']
    q="SELECT * FROM `tbl_cart_master`,`tbl_cart_child`,`tbl_item`,`tbl_user` WHERE `tbl_cart_master`.cm_id=`tbl_cart_child`.cm_id AND `tbl_cart_child`.item_id=`tbl_item`.item_id and tbl_cart_master.uid=tbl_user.uid and  tbl_cart_master.cm_id='%s'"%(cm_id)
    data['view']=select(q)
    return render_template("user_bill.html",data=data)  



@user.route('/profile',methods=['get','post'])
def profile():
    data={}
    uid=session['uid']
    q="select * from tbl_user where uid='%s'"%(uid)
    res=select(q)
    data['a']=res
    if 'register' in request.form:

        u_fname=request.form['u_fname']
        u_lname=request.form['u_lname'] 
        u_hname=request.form['u_hname']
        u_district=request.form['u_district']
        u_street=request.form['u_street']
        u_pin=request.form['u_pin']
        u_phone=request.form['u_phone']
        u_gender=request.form['u_gender']
        u_dob=request.form['u_dob']
		# username=request.form['username']
		# password=request.form['password']
        q1="update tbl_user set u_fname='%s', u_lname='%s', u_hname='%s', u_street='%s', u_district='%s', u_pin='%s', u_phone='%s', u_gender='%s', u_dob='%s' where uid='%s'"%(u_fname,u_lname,u_hname,u_street,u_district,u_pin,u_phone,u_gender,u_dob,uid)
        update(q1)
		# q2="update tbl_login set username='%s', password='%s' where username='%s'"%(username,password,session['uname'])
		# update(q2)
        return redirect(url_for("user.profile"))
    return render_template("profile.html",data=data)

@user.route("/artist_sales",methods=['get','post'])
def artist_sales():
    data={}
    if "btn" in request.form:
        daily=request.form['daily']
        if request.form['monthly']=="":
            monthly=""
        else:
            monthly='%'+request.form['monthly']+'%'
        print(monthly)
        q="SELECT * FROM tbl_item INNER JOIN tbl_cart_child USING (item_id) INNER JOIN tbl_cart_master USING (cm_id) WHERE (item_approval='paid' AND tbl_item.uid='%s'  AND cart_status <> 'pending' and `order_date` like '%s') or (item_approval='paid' AND tbl_item.uid='%s'  AND cart_status <> 'pending' and `order_date` like '%s') "%(session['uid'],daily,session['uid'],monthly)
        res=select(q)
        data['artist']=res
        session['res']=res
        r=session['res']
    else:
        q="SELECT * FROM tbl_item INNER JOIN tbl_cart_child USING (item_id) INNER JOIN tbl_cart_master USING (cm_id) WHERE item_approval='paid' AND tbl_item.uid='%s'  AND cart_status <> 'pending'"%(session['uid'])
        res=select(q)
        data['artist']=res
    return render_template("artist_sales.html",data=data)


@user.route("/print_artist",methods=['get','post'])
def print_artist():
    data={}
    if len(request.args.to_dict()) > 0:
        daily=request.args['daily']
        if request.args['monthly']=="":
            monthly=""
        else:
            monthly='%'+request.args['monthly']+'%'
        print(monthly)
        q="SELECT * FROM tbl_item INNER JOIN tbl_cart_child USING (item_id) INNER JOIN tbl_cart_master USING (cm_id) WHERE (item_approval='paid' AND tbl_item.uid='%s'  AND cart_status <> 'pending' and `order_date` like '%s') or (item_approval='paid' AND tbl_item.uid='%s'  AND cart_status <> 'pending' and `order_date` like '%s') "%(session['uid'],daily,session['uid'],monthly)
        res=select(q)
        data['r']=res
        session['res']=res
        r=session['res']

        q="SELECT sum(item_price) as earn FROM tbl_item INNER JOIN tbl_cart_child USING (item_id) INNER JOIN tbl_cart_master USING (cm_id) WHERE (item_approval='paid' AND tbl_item.uid='%s'  AND cart_status <> 'pending' and `order_date` like '%s') or (item_approval='paid' AND tbl_item.uid='%s'  AND cart_status <> 'pending' and `order_date` like '%s') "%(session['uid'],daily,session['uid'],monthly)
        data['earn']=select(q)[0]['earn']
    else:
        q="SELECT * FROM tbl_item INNER JOIN tbl_cart_child USING (item_id) INNER JOIN tbl_cart_master USING (cm_id) WHERE item_approval='paid' AND tbl_item.uid='%s'  AND cart_status <> 'pending'"%(session['uid'])
        res=select(q)
        data['r']=res
        q="SELECT sum(item_price) as earn FROM tbl_item INNER JOIN tbl_cart_child USING (item_id) INNER JOIN tbl_cart_master USING (cm_id) WHERE item_approval='paid' AND tbl_item.uid='%s'  AND cart_status <> 'pending'"%(session['uid'])
        data['earn']=select(q)[0]['earn']

    return render_template("print_artist.html",data=data)


@user.route("/cus_exb",methods=['get','post'])
def cus_exb():
    data={}
    q="select * from tbl_exhibition"
    res=select(q)
    data['cus_exb']=res
    return render_template("cus_exb.html",data=data)


@user.route("/cus_exb_art",methods=['get','post'])
def cus_exb_art():
    data={}
    id=request.args['id']
    q="SELECT * FROM `tbl_item` INNER JOIN `tbl_item_ex` USING (item_id) INNER JOIN `tbl_user` USING (uid) where ex_id='%s'  group by tbl_item.item_id "%(id)
    res=select(q)
    data['art_exb']=res
    return render_template("cus_exb_art.html",data=data)
