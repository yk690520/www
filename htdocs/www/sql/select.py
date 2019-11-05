import tools
from sql.bean.allBean import City,Phone
from datetime import datetime



@tools.mysql()
def getCount(cursor):
    cursor.execute("SELECT sum(member) FROM `counter`")
    value=cursor.fetchall()
    tuple= (0,) if len(value)<1 else value[0]
    for value in tuple:
        return value

@tools.mysql()
def getLinks(cursor):
    cursor.execute("SELECT link FROM `other` WHERE id=1")
    resault=cursor.fetchall()
    value = len(resault) and len(resault[0]) and resault[0][0]
    return value

@tools.mysql()
def getCounters(cursor):
    cursor.execute("SELECT DATE_FORMAT(record_time,'%Y-%m-%d'),member FROM `counter`")
    value=cursor.fetchall()
    return value

@tools.mysql()
def checkLogin(cursor,user,password):
    cursor.execute("SELECT name,user FROM `user` where user=%s and password=%s",[user,password])
    resault=cursor.fetchall()
    name=len(resault) and len(resault[0]) and resault[0][0]
    if name==0:
        return False
    else:
        user=resault[0][1]
        return name,user

@tools.mysql("town_info")
def getCityInforByCity_id(cursor,city:City):
    '''
    用来返回查询出来的城市信息
    :param cusor:
    :param city_id:
    :return: [{id:123,sid:"13",new_influence:"2200",old_influence:"2000",x:"1000",y:"1000",name:"北京"}]
    '''
    resault=[]


    cursor.execute("SELECT id,sid,new_influence,old_influence,name,located FROM `town` WHERE id=%s", (city.id,))
    select_resaults =cursor.fetchall()
    for select_resault in select_resaults:
        id = select_resault[0]
        sid = select_resault[1]
        new_influence = select_resault[2]
        old_influence = select_resault[3]
        name = select_resault[4]
        located = select_resault[5]
        city = City(sid, new_influence, old_influence, name, id=id, located=located)
        resault.append(city)
    return resault

@tools.mysql("town_info")
def getAllCityInfor(cursor):
    '''
    获取所有的都城信息
    :param cursor:
    :return:
    '''
    cursor.execute("SELECT id,sid,new_influence,old_influence,name,located FROM `town`")
    select_resaults=cursor.fetchall()
    resault=[]
    for select_resault in select_resaults:
        id = select_resault[0]
        sid = select_resault[1]
        new_influence = select_resault[2]
        old_influence = select_resault[3]
        name = select_resault[4]
        located = select_resault[5]
        city = City(sid, new_influence, old_influence, name, id=id, located=located)

        resault.append(city)
    return resault
@tools.mysql("town_info")
def getCityInforByCityName(cursor,city_name):
    '''
    通过城市名查出城市信息
    :param cursor:
    :param city_name:
    :return:
    '''
    cursor.execute("SELECT id,sid,new_influence,old_influence,name,located FROM `town` WHERE name=%s", (city_name,))
    select_resaults=cursor.fetchall()
    resault=[]
    for select_resault in select_resaults:
        id = select_resault[0]
        sid = select_resault[1]
        new_influence = select_resault[2]
        old_influence = select_resault[3]
        name = select_resault[4]
        located = select_resault[5]
        city = City(sid, new_influence, old_influence, name, id=id, located=located)
        resault.append(city)
    return resault
@tools.mysql("town_info")
def getCityInforByCity(cursor,city:City):
    sql="SELECT id,sid,new_influence,old_influence,name,located FROM town "
    after_sql=""
    args=[]
    after_sql+="id=%s and " if city.id else ""
    after_sql+="sid=%s and " if city.sid else ""
    after_sql+="new_influence=%s and " if city.new_influence else ""
    after_sql+="old_influence=%s and " if city.old_influence else ""
    after_sql+="name=%s and " if city.name else ""
    after_sql+="located=%s and " if city.located else ""
    if after_sql:
        after_sql=after_sql[0:-4]
        sql+="where "+after_sql
    if city.id:
        args.append(city.id)
    if city.sid:
        args.append(city.sid)
    if city.new_influence:
        args.append(city.new_influence)
    if city.old_influence:
        args.append(city.old_influence)
    if city.name:
        args.append(city.name)
    if city.located:
        args.append(city.located)
    cursor.execute(sql,args)
    select_resaults = cursor.fetchall()
    resault = []
    for select_resault in select_resaults:
        id = select_resault[0]
        sid = select_resault[1]
        new_influence = select_resault[2]
        old_influence = select_resault[3]
        name = select_resault[4]
        located = select_resault[5]
        city = City(sid, new_influence, old_influence, name, id=id, located=located)
        resault.append(city)
    return resault

@tools.mysql()
def getWechatPwdByWechatId(cursor,wechat_id,if_login:bool=False):
    '''
    根据微信号查询微信密码
    :param cursor:
    :param wechat_id:
    :return: 如果存在返回密码，不存在返回False
    '''
    infor=""
    if if_login:
        cursor.execute('SELECT wechat_pwd From wechat WHERE wechat_id=%s', (wechat_id,))
        resault = cursor.fetchall()
        infor = resault[0][0] if resault and resault[0] else False
    else:
        cursor.execute('SELECT record_date FROM other WHERE id=2')
        resault=cursor.fetchall()
        resault=resault and resault[0] and resault[0][0]
        record_date=resault.strftime("%Y-%m-%d")
        now=datetime.now().strftime("%Y-%m-%d")
        count=-1
        infor="亲，您今日的查询次数已使用完，请明日再来。"
        if record_date!=now:
            cursor.execute('UPDATE other SET link=0 WHERE id=2')
            cursor.execute('UPDATE other SET record_date=now() where id=2')
            count=0
        else:
            cursor.execute('SELECT link FROM other WHERE id=2')
            resault=cursor.fetchall()
            count=int(resault and resault[0] and resault[0][0])
        if count>=0 and count<10:
            cursor.execute('SELECT wechat_pwd From wechat WHERE wechat_id=%s',(wechat_id,))
            resault=cursor.fetchall()
            infor=resault[0][0] if resault and resault[0] else False
            count+=1
            cursor.execute('UPDATE other SET link=%s WHERE id=2',(count,))
    return infor
@tools.mysql()
def getWechatSelectCount(cursor):
    cursor.execute('SELECT record_date FROM other WHERE id=2')
    resault = cursor.fetchall()
    resault = resault and resault[0] and resault[0][0]
    record_date = resault.strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d")
    count=0
    if record_date!=now:
        count=10
    else:
        cursor.execute('SELECT link FROM other WHERE id=2')
        resault = cursor.fetchall()
        count = 10-int(resault and resault[0] and resault[0][0])
    return count
@tools.mysql()
def getPhones(cursor):
    cursor.execute("SELECT id,phone,check_code,use_able,check_able FROM phone")
    resault=[]
    select_resaults=cursor.fetchall()
    for select_resault in select_resaults:
        id=select_resault[0]
        phone=select_resault[1]
        check_code=select_resault[2]
        use_able=int(select_resault[3])
        check_able=int(select_resault[4])
        phone=Phone(id,phone,check_code,use_able,check_able)
        resault.append(phone)
    return resault

@tools.mysql("fans_data")
def get_bf_cha_zhi(cursor,before_task_id,after_task_id):
    '''

    :param cursor:
    :param before_task_id:
    :param after_task_id:
    :return: [
        [资产编号，微信号，爆粉前人数，爆粉后人数，爆粉数]
    ]
    '''
    cursor.execute("SELECT asserts,wechat,fans_count FROM bf WHERE task_id=%s",(before_task_id,))
    before_data=cursor.fetchall()
    if not(before_data and before_data[0]):
        return
    before_data_map={}
    for row in before_data:
        before_data_map[row[0]]=[row[1],row[2]]
    #获取后续任务id人数
    cursor.execute("SELECT asserts,wechat,fans_count FROM bf WHERE task_id=%s", (after_task_id,))
    after_data = cursor.fetchall()
    after_data_map = {}
    if (after_data and after_data[0]):
        for row in after_data:
            after_data_map[row[0]] = [row[1], row[2]]
    #依据前序任务数据进行处理
    output_data=[]
    for key,value in before_data_map.items():
        after_value=after_data_map.get(key)
        if after_value:
            #如果后续任务存在
            temp=[key,value[0],value[1],after_value[1],after_value[1]-value[1]]
        else:
            temp=[key,value[0],value[1],"请稍后","请稍后"]
        output_data.append(temp)
    return output_data

if __name__=="__main__":
    get_bf_cha_zhi(390819,390819)