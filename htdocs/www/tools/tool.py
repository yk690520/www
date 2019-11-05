from mysql import connector
import functools
import tools
def mysql(DatabaseName='test'):
    '''
    一个装饰器，用来处理sql连接，
    :param func:
    :return:
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tools.logger().info("args：【%s】,kwargs：【%s】" % (args, kwargs))
            #test用
            con = connector.connect(host='localhost', user='user', password='pwdpwdpwd', database=DatabaseName,charset="utf8mb4")###
            #线上使用(请勿修改此方法内的任意字符，包括注释，否则可能将导致服务器出现不可预估的错误）
            ####con=connector.connect(user='user', password='pwdpwdpwd', database=DatabaseName,charset="utf8mb4")
            cursor = con.cursor()
            try:
                resault = func(cursor, *args, **kwargs)
            except BaseException as e:
                tools.logger().error("args：【%s】,kwargs：【%s】" % (args, kwargs),e)
                tools.logger().exception(e)
                con.rollback()
                return None
            else:
                con.commit()
                return resault
            finally:
                cursor.close()
                con.close()
        return wrapper
    return decorator

def uid2xy(Uid):
    if type(Uid)==str:
        Uid=int(Uid)
    Z = Uid >> 32
    X = (Uid >> 16) - (Uid >> 32 << 16 )
    Y = Uid - ((Z << 32) | (X << 16))
    return X,Y

def xy2uid(x,y):
    return x<<16|y

def progeress_json(value):
    value=value.replace("\\","")
    value=value.replace("\'","")
    if value[-1:]==",":
        return value[:-1]
    return value

if __name__=="__main__":
    print(uid2xy("3670144"))
