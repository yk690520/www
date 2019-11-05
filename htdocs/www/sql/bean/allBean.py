import tools,datetime
class City():
    def __init__(self,sid:str=None,new_influence:str=None,old_influence:str=None,name:str=None,id:int=None,x:int=None,y:int=None,located:int=None):
        self._id=id
        self._sid=sid
        self._new_influence=new_influence
        self._old_influence=old_influence
        self._name=name
        self._located=None
        if x:
            self._x=x
            self._y=y
            self._located=tools.xy2uid(x,y)
        if located:
            self._located=located
            xAndY = tools.uid2xy(located)
            self._x = xAndY[0] if xAndY else -1
            self._y = xAndY[1] if xAndY else -1


    @property
    def id(self):
        return self._id

    @property
    def sid(self):
        return self._sid

    @property
    def new_influence(self):
        return self._new_influence

    @property
    def old_influence(self):
        return self._old_influence

    @property
    def name(self):
        return self._name

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def located(self):
        return self._located

class Phone():
    def __init__(self,id=None,phone:str=None,check_code=None,use_able:int=1,check_able:int=0):
        '''

        :param id:
        :param phone:
        :param check_code: 验证码
        :param use_able: 是否已被使用
        ：param check_able:验证码是否正确
        '''
        self._id=id
        self._phone=phone
        self._check_code=check_code
        if use_able==1:
            self._use_able=True
        else:
            self._use_able=False
        self._check_able=check_able
    @property
    def id(self):
        return self._id

    @property
    def phone(self):
        return self._phone

    @property
    def check_code(self):
        return self._check_code

    def getStatus(self):
        if self._use_able==0:
            #被使用
            if self._check_code:
                if self._check_able==0:
                    return "验证码等待使用"
                elif self._check_able==1:
                    return "验证码正确"
                else:
                    return "验证码不正确，请更新"
            else:
                return "手机号已被使用"
        else:
            return ""
class Log():
    def __init__(self,foot_name:str,log_infor:str,id:int=None,log_datetime=None):
        self._id=id
        self._foot_name=foot_name
        self._log_infor=log_infor
        if log_datetime==None:
            self._log_datetime=datetime.datetime.now()
        else:
            self._log_datetime=log_datetime
    @property
    def id(self):
        return self._id

    @property
    def foot_name(self):
        return self._foot_name

    @property
    def log_infor(self):
        return self._log_infor

    @property
    def log_datetime(self):
        return self._log_datetime