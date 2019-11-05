# fabfile.py
import os,re
from datetime import datetime
from fabric.api import *
env.user='root'

env.sudo_user='root'

env.hosts=['junx.ink']

db_user='user'
db_password='pwdpwdpwd'
_TAR_FILE='dist_htdocs.tar.gz'

def buildHttp():
    local('del apache\\dist\\%s' % _TAR_FILE)
    with lcd(os.path.join(os.path.abspath('.'),'apache\\www')):
        cmd = ['tar', '-czvf', '..\\dist\\%s' % _TAR_FILE]
        cmd.extend(['*'])
        local(' '.join(cmd),capture=True)

def buildPython():
    includes = ['*']
    excludes = ['.idea','test', '.*', '*.pyc', '*.pyo','.*','__pycache__','tmps']
    local('del htdocs\\dist\\%s' % _TAR_FILE)
    with lcd(os.path.join(os.path.abspath('.'),'htdocs\www')):
        cmd=['tar','-czvf','..\\dist\\%s' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd),capture=True)
        pass

_REMOTE_TMP_TAR = '/tmp/python/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/srv/awesome'
#部署python服务器
def deployPython():
    newdir = 'www-%s' % datetime.now().strftime('%y-%m-%d_%H.%M.%S')
    # 删除已有的tar文件:
    run('rm -f %s' % _REMOTE_TMP_TAR)
    # 上传新的tar文件:
    put('htdocs\\dist\\%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    # 创建新目录:
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    # 解压到新目录:
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
    # 重置软链接:
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
        sudo('ln -s %s www' % newdir)
        sudo('chown www-data:www-data www')
        sudo('chown -R www-data:www-data %s' % newdir)
    with cd('%s/%s' % (_REMOTE_BASE_DIR,'www')):
        sudo('chmod 777 app.py')
        sudo(' sed -i \'s#\\r##\' app.py')   #去除app 异常字符串

        sudo('sed -i \'s/con.*###//g\' /srv/awesome/www/tools/tool.py')
        sudo('sed -i \'s/####//g\' /srv/awesome/www/tools/tool.py')
        pass
    # 重启Python服务和nginx服务器:
    with settings(warn_only=True):
        sudo('/etc/init.d/apache2 stop')
        sudo('supervisorctl stop awesome')
        sudo('supervisorctl start awesome')
        sudo('/etc/init.d/nginx stop')
        sudo('/etc/init.d/nginx start')

_HTTP_TMP_TAR = '/tmp/http/%s' % _TAR_FILE
_HTTP_BASE_DIR='/srv/apache'
#部署http服务器
def deployHttp():
    newdir = 'www-%s' % datetime.now().strftime('%y-%m-%d_%H.%M.%S')
    run('rm -f %s' % _HTTP_TMP_TAR)
    put('apache\\dist\\%s' % _TAR_FILE,_HTTP_TMP_TAR)
    with cd(_HTTP_BASE_DIR):
        sudo('mkdir %s ' % newdir)
    with cd('%s/%s' % (_HTTP_BASE_DIR,newdir)):
        sudo('tar -xzvf %s' % _HTTP_TMP_TAR)
    with cd(_HTTP_BASE_DIR):
        sudo('rm -f www')
        sudo('ln -s %s www' % newdir)
        sudo('chown www-data:www-data www')
        sudo('chown -R www-data:www-data %s' % newdir)
    with settings(warn_only=True):
        sudo('/etc/init.d/nginx stop')
        sudo('supervisorctl stop awesome')
        sudo('/etc/init.d/apache2 stop')
        sudo('/etc/init.d/apache2 start')
    pass


















