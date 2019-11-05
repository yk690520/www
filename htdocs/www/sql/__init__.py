import sql.select
import sql.update





#返回网站计数器
getCount=sql.select.getCount
#修改网址计数，每调用一次将增加一次访问量
updateCounter=sql.update.updateCounter
#获得数据库links数据
getLinks=sql.select.getLinks
#清除数据库links数据
clearLinks=sql.update.clearLinks
#上传数据
upLinks=sql.update.upLinks
#获取网站的统计数
getCounters=sql.select.getCounters
#检查用户名和密码
checkLogin=sql.select.checkLogin

#通过id删除城市信息
delCity=sql.update.delCity
#更新城市信息
updateCity=sql.update.updateCity
#新增城市信息
addCity=sql.update.addCity

#获取城市信息
getCityInforByCity_id=sql.select.getCityInforByCity_id
#获取所有
getAllCityInfor=sql.select.getAllCityInfor
#通过城市名获取
getCityInforByCityName=sql.select.getCityInforByCityName
#通过城市对象获取
getCityInforByCity=sql.select.getCityInforByCity

#通过微信id查看密码
getWechatPwdByWechatId=sql.select.getWechatPwdByWechatId

#获取剩余查询次数
getWechatSelectCount=sql.select.getWechatSelectCount

#获取验证码
write_code=sql.update.write_code

#设置验证码
get_code=sql.update.get_code
#增加一个新的手机
add_phone=sql.update.add_phone
#更新验证码
update_check_code=sql.update.update_check_code
#得到所有的手机
getPhones=sql.select.getPhones
#得到一个可用的手机
get_phone=sql.update.get_phone
#删除一个手机号
delate_phone=sql.update.delate_phone
#设置验证码状态和删除成功的验证码
set_check_able=sql.update.set_check_able
#设置手机号可用状态
set_phone_status=sql.update.set_phone_able
#增加日志
add_log=sql.update.add_log
#写入爆粉日志
write_bf_log=sql.update.write_bf_log
#输出爆粉数据
get_bf_cha_zhi=sql.select.get_bf_cha_zhi
#写入新的群
write_groupname=sql.update.write_groupname
#写入新的推名片数据
insert_push_card=sql.update.insert_push_card