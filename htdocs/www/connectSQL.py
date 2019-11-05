from mysql import connector



#通过名称查SID
def sid_select(town_name):
    cursor.execute("SELECT sid FROM `town` WHERE name=%s",(town_name,))
    result = cursor.fetchall()
    return '城池SID:'+result[0][0]


#通过名称查新服势力值
def new_inluence_select(town_name):
    cursor.execute("SELECT new_influence FROM `town` WHERE name=%s",(town_name,))
    result = cursor.fetchall()
    return '新服势力值:'+result[0][0]

#通过名称查老服势力值
def old_inluence_select(town_name):
    cursor.execute("SELECT old_influence FROM `town` WHERE name=%s", (town_name,))
    result = cursor.fetchall()
    return '老服势力值:'+result[0][0]

#坐标位运算
def int2xy(Uid):
    Z = Uid >> 32
    X = (Uid >> 16) - (Uid >> 32 << 16 )
    Y = Uid - ((Z << 32) | (X << 16))
    print('坐标为：'+str(X)+','+str(Y))


#逆运算（暂时未完成）
def int1xy(located):
    Uid = (located >> 16 << 32) + (located << 16)
    print(Uid)

    return Uid


#读取坐标
def located_select(town_name):
    #X = int1xy(town_name)
    cursor.execute("SELECT located FROM `town` WHERE name=%s", (town_name,))
    #cursor.execute("SELECT name FROM `town` WHERE located=%s", (X,))
    result = cursor.fetchall()
    int2xy(result[0][0])

#添加城池信息
def city_insert(sid,name,new,old,located):
    if len(sid) > 5:
        print('sid格式错误，不能超过五位数字')
    elif len(located) >= 11:
        print('二进制坐标位数长度错误')
    elif not( sid and name and new and old and located):
        print('被填选项不能为空')
    else:
        cursor.execute("INSERT INTO town(sid,name,old_influence,new_influence,located) VALUES(%s,%s,%s,%s,%s)",
                       (sid, name, old, new, located))
        con.commit()
        print('添加成功')



#删除城池信息
def city_delet(name):
    cursor.execute("SELECT sid FROM `town` WHERE name=%s",(name,))
    result = cursor.fetchall()
    if result:
        cursor.execute("DELETE FROM town WHERE name=%s", (name,))
        con.commit()
        print('删除成功')
    else:
        print('暂无城池信息，无法删除')

#更新城池数据
def cityinfo_update():
    option = input('1、sid 2、name 3、old_influence 4、new_influence 5、located\n')
    name = input('input name for update\n')
    try:
        if option == '1':
            sid = input('input sid\n')
            cursor.execute("UPDATE town SET sid=%s WHERE name=%s", (sid, name))
        elif option == '2':
            new_name = input('input your new name\n')
            cursor.execute("UPDATE town SET name=%s WHERE name=%s", (new_name, name))
        elif option == '3':
            old = input('input old_influence\n')
            cursor.execute("UPDATE town SET old_influence=%s WHERE name=%s", (old, name))
        elif option == '4':
            new = input('input new_influence\n')
            cursor.execute("UPDATE town SET new_influence=%s WHERE name=%s", (new, name))
        elif option == '5':
            located = input('input located(before int2xy)\n')
            cursor.execute("UPDATE town SET located=%s WHERE name=%s", (located, name))
        con.commit()
        print('更新成功')
    except Exception:
        print('Error:更新失败')











if __name__=="__main__":
    #数据库的连接在于拿到一个数据库的连接对象，这个就是数据库的连接对象
    con=connector.connect(host='junx.ink',user='root', password='yingke520', database='town_info')
    #然后通过连接对象拿到游标
    cursor = con.cursor()
    #通过游标对象我们就可以进行数据库的增删改查
    #查询
    while True:
        #try:
            type_select = input('1、city_select 2、city_insert 3、city_delet 4、update_info 5、exit\n')
            if type_select == '1':
                town_name = input('city select from town_name\n')
                try:
                    print(sid_select(town_name))
                    print(new_inluence_select(town_name))
                    print(old_inluence_select(town_name))
                    located_select(town_name)
                except IndexError:
                    print('暂无对应城池信息')
                continue
            elif type_select == '2':
                sid = input('input sid\n')
                name = input('input name\n')
                old = input('input old_influence\n')
                new = input('input new_influence\n')
                located = input('input located(before int2xy)\n')
                try:
                    city_insert(sid, name, old, new, located)
                except Exception:
                    print('添加失败')
                continue
            elif type_select == '3':
                name = input('input name for delet\n')
                city_delet(name)
            elif type_select == '4':
                cityinfo_update()
            elif type_select == '5':
                # 提交事务
                # con.commit()
                # 关闭游标
                cursor.close()
                # 关闭数据库连接
                con.close()
                print('数据库已关闭连接')
                break
        #except:
            #print('暂无城池记录')
            #continue









