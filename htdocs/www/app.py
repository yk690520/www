#!/usr/bin/python3
from flask import Flask
import tools
import logging
from flask import render_template
import datetime
from flask import abort, redirect, url_for,request,session
import sql,os,json,re,ueflask
from sql.bean.allBean import City,Phone,Log
from flask import jsonify
app = Flask(__name__)
app.debug = 1
app.secret_key = os.urandom(16)
ueflask.setApp(app)
ueflask.setAcSc('BtJNCJFHJHbsBOA7YFLgZx2CqZ785adbpGj-w7zv','w2n95EOG4V3Lyj__JWGhuFGzu74gjBpUg-2eLB0D')
ueflask.setBucket('test','pcgvmcq7e.bkt.clouddn.com')
tools.set_loger(app.logger)
app.logger.setLevel(logging.WARNING)
#拦截请求，并对请求进行校验
@app.before_request
def before_request():
    path=request.path
    uacess=["/city-delate.html","/city_add.html","/city-editor.html","/wechat-editor.html"]
    if path in uacess:
        if not session.get('user'):
            jump_page=path
            jump_infor_one=["/login.html","登陆","亲爱的，您没有此页面操作权限",{"args":None,"form":None}]
            args=request.args
            form=request.form
            jump_infor_two=[jump_page,"之前的","亲爱的，已完成操作",{"args":args,"form":form}]
            jump_infor=[]
            jump_infor.append(jump_infor_two)
            jump_infor.append(jump_infor_one)
            session["jump_infor"]=jump_infor
            return redirect(url_for("jump"))
    pass
@app.route("/logout.html",methods=['GET','POST'])
def logout():
    if session.get('user'):
        del session['user']
    return redirect(url_for('home'))

@app.route('/jump.html',methods=['GET','POST'])
def jump():
    person_count = sql.getCount()
    j_i=""
    if session.get("jump_infor"):
        jump_infor=session["jump_infor"]
        if jump_infor:
            j_i=jump_infor.pop()
            session['jump_infor']=jump_infor
            request.form=j_i[3]['form']
            request.args=j_i[3]['args']
    return render_template('jump.html',person_count=person_count,jump_infor=j_i)
    pass
#主页
@app.route('/index.html',methods=['GET','POST'])
def home():
    person_count=sql.getCount()
    return render_template('index.html',person_count=person_count)

#网站访问人数计数器
@app.route('/', methods=['GET', 'POST'])
def count():
    #更新网站访问计数器
    sql.updateCounter()
    return redirect(url_for('home'))

#sway网页
@app.route('/sway.html',methods=['GET','POST'])
def sway():
    person_count = sql.getCount()
    return render_template('sway.html',person_count=person_count)

#访问link主页
@app.route('/link.html',methods=['GET','POST'])
def links():
    if request.method=='POST':
        links=request.form['links']
        groups=re.findall(r"http:[./a-zA-Z?0-9]*",links)
        cleanLinks=""
        for link in groups:
            cleanLinks+=link+","
        resault=sql.upLinks(cleanLinks[:len(cleanLinks)-1])
        if resault==False:
            return json.dumps({"message":"error","error":"error"})  #由于是使用ajax调用，可以仅仅返回一个成功值，以加快保存速度
        else:
            return json.dumps({"message":"ok","error":"ok","infor":cleanLinks[:len(cleanLinks)-1]})  #由于是使用ajax调用，可以仅仅返回一个成功值，以加快保存速度
    else:
        links = sql.getLinks()
        person_count = sql.getCount()
        return render_template('link.html',person_count=person_count,links=links)

#404网页错误重定向
@app.errorhandler(404)
def error(e):
    return render_template("error.html"),404

#统计人数展示页面
@app.route("/counter.html",methods=['GET','POST'])
def counter():
    counters=sql.getCounters()
    person_count = sql.getCount()
    return render_template("counter.html",counters=counters,person_count=person_count)

#登陆页面展示
@app.route("/login.html",methods=['GET','POST'])
def login():
    if request.method=="POST":
        #进入登陆验证
        user=request.form['user']
        password=request.form['password']
        user=sql.checkLogin(user,password)
        if user:
            #登陆成功
            session['user']=user
            return redirect(url_for("jump"))
        else:
            return render_template("login.html",error="登陆错误，检查密码和用户名")
    else:
        if session.get("user"):
            return redirect(url_for('home'))
        else:
            return render_template("login.html")
#ue测试页面
@app.route("/ue.html",methods=['GET','POST'])
def uetest():
    return render_template("ue.html")

#城市展示页面
@app.route("/city.html",methods=['GET','POST'])
def city():
    infor=''
    id=''
    name=''
    if request.method=='POST':
        name=request.form['name']
        id=request.form['id']
        citys=sql.getCityInforByCity(City(id=id,name=name))
    else:
        citys=sql.getAllCityInfor() or []
    if not citys:
        infor = "信息不存在"
    person_count = sql.getCount()
    return render_template("city.html",person_count=person_count,citys=citys,infor=infor,id=id,name=name)

@app.route("/city-delate.html",methods=['GET','POST'])
def city_delate():
    id=request.args.get('id')
    sql.delCity(City(id=id))
    return redirect(url_for('city'))

@app.route("/city-editor.html",methods=['GET','POST'])
def city_editor():
    person_count = sql.getCount()
    if request.method=='GET':
        id=request.args.get('id')
        city=sql.getCityInforByCity(City(id=id))
        city=city[0] if city else City()
        return render_template("city-editor.html",person_count=person_count,city=city)
    else:
        return render_template('city-editor.html',person_count=person_count)
    pass
@app.route("/wechat.html",methods=['GET','POST'])
def wechat():
    if not session.get('user'):
        count=sql.getWechatSelectCount()
        if count>1:
            infor='今日还有【%s次】查询机会，请谨慎使用' % (int(count)-1,)
        else:
            infor='今日查询次数已用完，请君明日再来。'
        wechat_id=""
        wechat_pwd=""
        if request.method=='POST':
            wechat_id=request.form['wechat_id'].strip()
            wechat_pwd=sql.getWechatPwdByWechatId(wechat_id)
            if not wechat_pwd:
                infor='信息不存在'
        person_count = sql.getCount()
    else:
        infor="亲，您是我们最萌的用户，查询【不受限制】"
        wechat_pwd=""
        wechat_id=""
        if request.method=='POST':
            wechat_id = request.form['wechat_id'].strip()
            wechat_pwd = sql.getWechatPwdByWechatId(wechat_id,True)
            if not wechat_pwd:
                infor='信息不存在'
        person_count = sql.getCount()
    return render_template("wechat.html",person_count=person_count,wechat_id=wechat_id,infor=infor,wechat_pwd=wechat_pwd)
@app.route("/code.html",methods=["GET","POST"])
def code():
    person_count = sql.getCount()
    phones=sql.getPhones()
    infor=None
    if session.get("infor"):
        infor=session.get("infor")
    return render_template("code.html",person_count=person_count,phones=phones,infor=infor)
@app.route("/add_code.html",methods=["POST"])
def add_phone():
    phone=request.form["phone"]
    if not phone:
        infor="新增的号码不能为空"
    else:
        phone=Phone(phone=phone)
        if sql.add_phone(phone):
            infor="添加号码成功"
        else:
            infor = "号码已存在"
    session["infor"]=infor
    return redirect(url_for('code'))



@app.route("/add_check_code.html",methods=["POST"])
def add_check_code():
    check_code=request.form["check_code"]
    id=request.form["id"]
    if not check_code and not id:
        infor="所提供的验证码不能为空"
    else:
        phone=Phone(id=id,check_code=check_code)
        if sql.update_check_code(phone):
            infor="更新验证码成功"
        else:
            infor="未找到对应的号码，可能此号码已被使用"
    session["infor"] = infor
    return redirect(url_for('code'))
@app.route("/del_phone.html",methods=["GET"])
def del_phone():
    phone = request.args.get("phone")
    if not phone:
        infor="请勿键入空的号码"
    else:
        re=sql.delate_phone(phone)
        if re:
            infor="删除成功"
        else:
            infor="此号码已被删除"
    session["infor"] = infor
    return redirect(url_for("code"))
@app.route("/reset_phone.html",methods=["GET"])
def reset_phone():
    phone = request.args.get("phone")
    if not phone:
        infor = "请勿键入空的号码"
    else:
        re=sql.set_phone_status(phone)
        if re:
            infor="重置成功，可重复使用"
        else:
            infor="此号码已不存在"
    session["infor"] = infor
    return redirect(url_for("code"))

@app.route("/get_phone.html",methods=["GET"])
def get_phone():
    #www.junx.ink/get_phone.html
    re=sql.get_phone()
    if re:
        return jsonify({"state":"success","phone":re})
    else:
        return jsonify({"state": "error", "phone": "error"})
    pass
@app.route("/get_check_code.html",methods=["GET"])
def get_check_code():
    #www.junx.ink/get_check_code.html?phone=
    phone = request.args.get("phone")
    if not phone:
        return jsonify({"state": "error", "msg": "empty input"})
    re=sql.get_code(phone)
    if re:
        return jsonify({"state":"success","code":re})
    else:
        return jsonify({"state":"error","code":"error"})

@app.route("/set_check_able.html",methods=["GET"])
def set_check_able():
    #www.junx.ink/set_check_able.html?phone=123&able=1
    phone=request.args.get("phone")
    check_able=request.args.get("able")
    if not phone or not check_able:
        return jsonify({"state": "error", "msg": "empty input"})
    re=sql.set_check_able(phone,int(check_able))
    if re:
        return jsonify({"state":"success","msg":"success"})
    else:
        return jsonify({"state":"error","msg":"error"})

@app.route("/add_log.html",methods=['GET','POST'])
def add_log():
    #www.junx.ink/add_log.html?foot_name=你好&log_infor=我好
    foot_name=request.args.get("foot_name")
    log_infor=request.args.get("log_infor")
    if not foot_name or not log_infor:
        return jsonify({"state": "error", "msg": "empty input"})
    re=sql.add_log(Log(foot_name=foot_name,log_infor=log_infor))
    if re:
        return jsonify({"state": "success", "msg": "success"})
    else:
        return jsonify({"state": "error", "msg": "error"})
@app.route("/write_bf_log.html",methods=['GET','POST'])
def write_bf_log():
    #www.junx.ink/write_bf_log.html?asserts=YF-A-01&wechat=fs690520&fans=112&task=1211
    if request.method == "POST" and request.is_json:
        asserts=request.json['asserts']
        wechat=request.json['wechat']
        fans=request.json['fans']
        task=request.json['task']
        if (not asserts) or (not wechat) or (not fans) or (not task):
            return jsonify({"state":"error","msg":"empty input"})
        re=sql.write_bf_log(asserts,wechat,fans,task)
        if re:
            return jsonify({"state": "success", "msg": "success"})
        else:
            return jsonify({"state": "error", "msg": "error"})
@app.route("/console.html",methods=['GET','POST'])
def console():
    resault=[]
    infor = ""
    before_data=""
    after_data=""
    if request.method=="POST":
        before_data=request.form["before_task_id"]
        after_data=request.form["after_task_id"] or "-1"
        if (not before_data) or (not after_data):
            infor = "请输入查询数据"
        else:
            resault=sql.get_bf_cha_zhi(before_data,after_data)
            if not resault:
                #无数据
                infor="暂无数据，请稍后..."
                resault=[]
            else:
                resault.sort(key=lambda value: value[0])
    person_count = sql.getCount()
    return render_template("console.html",person_count=person_count,before_task_id=before_data,after_task_id=after_data,infor=infor,output_data=resault)

@app.route("/write_group_infor.html",methods=['GET','POST'])
def write_group_infor():
    # www.junx.ink/write_group_infor.html?chatname=133432@&group=dfdf&wechat=fs690520&asserts=YC-A-01&count=1211&join_date=2017-12-11 23:33:33
    reqst=request
    if request.method=="POST" and request.is_json:
        chatrooms=request.json['chatrooms']
        if not chatrooms:
            return jsonify({"state": "error", "msg": "empty input"})
        for chatroom in chatrooms:
            chatname = chatroom['chatname']
            group_name = chatroom['group']
            wechat = chatroom['wechat']
            asserts = chatroom['asserts']
            count=chatroom['count']
            join_date=datetime.datetime.strptime(chatroom['join_date'],"%Y-%m-%d %H:%M:%S")
            sql.write_groupname(chatname,group_name,wechat,asserts,count,join_date)
        return jsonify({"state": "success", "msg": "success"})

@app.route("/push_bf.html",methods=["GET","POST"])
def push_bf():
    if request.method == "POST" and request.is_json:
        asserts=request.json['asserts']
        wechat=request.json['wechat']
        fans_wxid=request.json['fans_wxid']
        bf_flag=int(request.json['bf_flag'])
        fans_sex=int(request.json['fans_sex'])
        push_card=request.json['push_card']
        if (not wechat) or (not fans_wxid) or (not bf_flag) or (not fans_sex) or (not push_card):
            return jsonify({"state":"error","msg":"empty input"})
        re=sql.insert_push_card(asserts=asserts,wechat=wechat,fans_wxid=fans_wxid,bf_flag=bf_flag,fans_sex=fans_sex,push_card=push_card)
        if re:
            return jsonify({"state": "success", "msg": "success"})
        else:
            return jsonify({"state": "error", "msg": "error"})
    return jsonify({"state": "error", "msg": "error request"})
@app.route("/about-me.html",methods=["GET","POST"])
def about_me():
    person_count = sql.getCount()
    return render_template('about-me.html', person_count=person_count)

if __name__ == '__main__':
    app.run()
