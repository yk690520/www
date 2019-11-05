#deploy.py

import os


if __name__=="__main__":
    #需要安装fabric3
    print('===================欢迎进入自动化服务器部署===================')
    print('')
    print('1、部署Http服务器')
    print('2、部署Python服务器')
    print('other、退出')
    print('=============================================================')
    flag=input('请输入：')
    if flag=='1':
        os.system('fab buildHttp')
        os.system('fab deployHttp')
    elif flag=='2':
        os.system('fab buildPython')
        os.system('fab deployPython')
    else:
        exit()