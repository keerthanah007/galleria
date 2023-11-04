from flask import *
from database import *

courier=Blueprint('courier',__name__)

@courier.route("/cou_homr")       
def cou_home():
	return render_template("cou_home.html")




@courier.route("/cou_orders")
def cou_orders():
    data={}
    q="    SELECT * FROM `tbl_cart_master`,`tbl_cart_child`,`tbl_delivery`,`tbl_user`,`tbl_item` WHERE `tbl_cart_master`.cm_id=`tbl_cart_child`.cm_id AND `tbl_cart_master`.cm_id=`tbl_delivery`.cm_id AND `tbl_cart_master`.uid=`tbl_user`.uid  AND tbl_cart_child.item_id= tbl_item.item_id AND tbl_delivery.cou_id='%s'  AND cart_status <> 'delivered'"%(session['cor_id'])
    data['res']=select(q)
    
    if 'action' in request.args:
        action=request.args['action']
        cm_id=request.args['cm_id']
    else:
        action=None
    # print("test")  
    if action == "falooda":
        print("test")
        q="update tbl_cart_master set cart_status='delivered' where cm_id='%s' "%(cm_id)
        print(q)
        update(q)
        flash("Delivery Completed")
        return redirect(url_for("courier.cou_orders"))
    return render_template("cou_orders.html",data=data)
