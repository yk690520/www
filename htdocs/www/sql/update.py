from mysql import connector
from datetime import datetime
import tools
from sql.bean.allBean import City,Phone,Log

@tools.mysql()
def updateCounter(cursor):
    today=datetime.now().strftime("%Y-%m-%d")+"%"
    cursor.execute("select member from counter where record_time like %s",[today])
    resault=cursor.fetchall()
    value=len(resault) and len(resault[0]) and resault[0][0]
    if int(value)>0:
        value+=1
        cursor.execute("UPDATE counter SET member=%s WHERE record_time like %s ",[value,today])
    else:
        today=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("insert into counter(member,record_time) values(1,%s)",[today])
    return True
    pass

@tools.mysql()
def clearLinks(cursor):
    cursor.execute("UPDATE other SET link='' WHERE id=1")
    return True

@tools.mysql()
def upLinks(cursor,links):
    cursor.execute("UPDATE other SET link=%s WHERE id=1",[links])
    return True

@tools.mysql("town_info")
def delCity(cursor,city:City):
    '''
    通过id删除城市信息
    :param cursor:
    :param id:
    :return:
    '''
    cursor.execute('DELETE FROM town WHERE id=%s',(city.id,))
    return True
    pass
@tools.mysql("town_info")
def updateCity(cursor,city:City):
    cursor.execute('UPDATE town SET name=%s,sid=%s,old_influence=%s,new_influence=%s,located=%s WHERE id=%s',(city.name,city.sid,city.old_influence,city.new_influence,city.located,city.id))
    return True

@tools.mysql("town_info")
def addCity(cursor,city:City):
    cursor.execute('INSERT INTO town(name,sid,old_influence,new_influence,located) VALUES (%s,%s,%s,%s,%s)',(city.name,city.sid,city.old_influence,city.new_influence,city.located))
    return True

@tools.mysql()
def write_code(cursor,code:int):
    cursor.execute('UPDATE other SET link=%s WHERE id=3',(code,))
    return True

@tools.mysql()
def add_phone(cursor,phone:Phone):
    '''
    :param cursor:
    :return: False：已存在相同的号码
            True:增加成功
    '''
    cursor.execute("SELECT id FROM phone WHERE phone=%s",(phone.phone,))
    if cursor.fetchall():
        return False
    cursor.execute("INSERT INTO phone(phone,use_able,check_able) VALUES (%s,1,0)",(phone.phone,))
    return True
@tools.mysql()
def update_check_code(cursor,phone:Phone):
    '''
    :param cursor:
    :param phone:
    :return: False:表示此id对应的手机号已找不到
            True:表示更新成功
    '''
    cursor.execute("SELECT id FROM phone WHERE id=%s",(phone.id,))
    if not cursor.fetchall():
        return False
    cursor.execute("UPDATE phone SET check_code=%s,check_able=0 WHERE id=%s",(phone.check_code,phone.id))
    return True

@tools.mysql()
def get_phone(cursor):
    '''
    取一个可用的手机号,取成功后将可用状态至为否
    :param cursor:
    :return:False:未找到任何可用的手机号
            str:返回手机号
    '''
    cursor.execute("SELECT phone FROM phone WHERE use_able=1")
    resault=cursor.fetchall()
    if not resault:
        return False
    phone=resault[0][0]
    cursor.execute("UPDATE phone SET use_able=0 WHERE phone=%s",(phone,))
    return phone

@tools.mysql()
def delate_phone(cursor,phone):
    '''
    删除手机号
    :param cursor:
    :param phone:
    :return:
    False:此手机号不存在
    True:删除成功
    '''
    cursor.execute("SELECT phone FROM phone WHERE phone=%s",(phone,))
    if not cursor.fetchall():
        return False
    cursor.execute("DELETE FROM phone WHERE phone=%s ",(phone,))
    return True
@tools.mysql()
def get_code(cursor,phone):
    '''
    :param cursor:
    :param phone:
    :return:
    False:此手机号或者验证码不存在
    '''
    cursor.execute("SELECT check_code,check_able FROM phone WHERE phone=%s", (phone,))
    resault = cursor.fetchall()
    if not resault:
        return False
    check_code = resault[0][0]
    check_able=int(resault[0][1])
    if not check_code:
        return False
    if check_able!=0:
        return False
    return check_code

@tools.mysql()
def set_check_able(cursor,phone,check_able):
    '''
    更新验证码的状态
    :param cursor:
    :param phone:
    :param check_able:
    :return:
    '''
    cursor.execute("SELECT phone FROM phone WHERE phone=%s", (phone,))
    if not cursor.fetchall():
        return False
    if check_able==1:
        cursor.execute("DELETE FROM phone WHERE phone=%s ", (phone,))
        return True
    elif check_able==2:
        cursor.execute("UPDATE phone SET check_able=%s WHERE phone=%s",(check_able,phone))
        return True
    else:
        return False
@tools.mysql()
def set_phone_able(cursor,phone):
    cursor.execute("SELECT phone FROM phone WHERE phone=%s", (phone,))
    if not cursor.fetchall():
        return False
    cursor.execute("UPDATE phone SET check_code='',check_able=0,use_able=1 WHERE phone=%s",(phone,))
    return True

@tools.mysql()
def add_log(cursor,log:Log):
    cursor.execute("INSERT INTO log(foot_name,log_infor,log_datetime) VALUES(%s,%s,%s)",(log.foot_name,log.log_infor,log.log_datetime))
    return True
@tools.mysql("fans_data")
def write_bf_log(cursor,asserts,wechat,fans,task):
    now=datetime.now()
    cursor.execute("INSERT INTO bf(asserts,wechat,fans_count,record_datetime,task_id) VALUES(%s,%s,%s,%s,%s)",(asserts,wechat,fans,now,task))
    return True

@tools.mysql("fans_data")
def write_groupname(cursor,chatname:str,group_name:str,wechat:str,asserts:str,group_count:int,join_date:datetime):
    #查询此群是否存在之前同一设备上
    cursor.execute("SELECT count(*) FROM group_table WHERE wechat=%s AND chatname=%s",(wechat,chatname))
    resault=cursor.fetchall()
    if resault and resault[0] and resault[0][0] :
        if resault[0][0]!=0:
            #同一设备之前的如果存在这个群则不记录
            cursor.execute("UPDATE group_table SET withdraw_groups=0 WHERE wechat=%s AND chatname=%s",(wechat,chatname))
            return -1
    cursor.execute("SELECT join_date,useable,bfing,use_date,use_count FROM group_table WHERE chatname=%s AND flag=1",(chatname,))
    resault=cursor.fetchall()
    if resault and resault[0] and resault[0][0]:
        if resault[0][0]:
            #之前其它设备进入过此群,比较其日期，将先进入的标志位设置为1
            before_date=resault[0][0]
            useable=resault[0][1]
            bfing=resault[0][2]
            use_date=resault[0][3]
            use_count=resault[0][4]
            if join_date<before_date:
                #更新新的标志位
                cursor.execute("UPDATE group_table SET flag=0,useable=0,bfing=0,withdraw_groups=0 WHERE chatname=%s AND flag=1", (chatname,))
                cursor.execute("INSERT INTO group_table(chatname,group_name,wechat,asserts,group_count,join_date,useable,bfing,flag,use_date,use_count,withdraw_groups) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                   (chatname,group_name,wechat,asserts,group_count,join_date,int(useable),int(bfing),1,use_date,use_count,0))
            else:
                #不更新其标志位，直接插入
                cursor.execute(
                    "INSERT INTO group_table(chatname,group_name,wechat,asserts,group_count,join_date,useable,bfing,flag,use_count,withdraw_groups) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (chatname, group_name, wechat, asserts, group_count, join_date, 0, 0, 0,0,0))
    else:
        # 之前未有新的设备进入
        cursor.execute(
            "INSERT INTO group_table(chatname,group_name,wechat,asserts,group_count,join_date,useable,bfing,flag,use_count,withdraw_groups) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (chatname, group_name, wechat, asserts, group_count, join_date, 1, 0, 1,0,0))
    return True
@tools.mysql("fans_data")
def insert_push_card(cursor,asserts:str,wechat:str,fans_wxid:str,bf_flag:int,fans_sex:int,push_card:str):
    now = datetime.now()
    cursor.execute("INSERT INTO bf_push(asserts,wechat,fans_wxid,bf_flag,fans_sex,push_card,push_date) values(%s,%s,%s,%s,%s,%s,%s)",
                   (asserts,wechat,fans_wxid,bf_flag,fans_sex,push_card,now))
    return True

if __name__=="__main__":
    print(write_groupname("323","3423","22d536337","22","3334",datetime.strptime("2017-12-11 11:35:00","%Y-%m-%d %H:%M:%S")))