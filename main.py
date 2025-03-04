import os
import traceback
import time
import mytime
import fgourl
from user import user

def get_env_variable(var_name, default_value=None):
    return os.environ.get(var_name, default_value)

def initialize_environment_variables():
    return {
        'userIds': get_env_variable('userIds', '').split(','),
        'authKeys': get_env_variable('authKeys', '').split(','),
        'secretKeys': get_env_variable('secretKeys', '').split(','),
        'verCode': get_env_variable('verCode'),
        'TGBotToken': get_env_variable('TGBotToken'),
        'TGAdminId': get_env_variable('TGAdminId'),
        'GithubToken': get_env_variable('GithubToken'),
        'GithubName': get_env_variable('GithubName'),
        'Pserver': get_env_variable('Pserver'),
        'Puser': get_env_variable('Puser'),
        'UserAgent': get_env_variable('UserAgent', 'nullvalue')
    }

def main():
    env_vars = initialize_environment_variables()
    
    userIds = env_vars['userIds']
    authKeys = env_vars['authKeys']
    secretKeys = env_vars['secretKeys']
    
    userNums = len(userIds)
    authKeyNums = len(authKeys)
    secretKeyNums = len(secretKeys)

    fgourl.ver_code_ = env_vars['verCode']
    fgourl.TelegramBotToken = env_vars['TGBotToken']
    fgourl.TelegramAdminId = env_vars['TGAdminId']
    fgourl.github_token_ = env_vars['GithubToken']
    fgourl.github_name_ = env_vars['GithubName']
    fgourl.Pserver = env_vars['Pserver']
    fgourl.Puser = env_vars['Puser']
    
    if env_vars['UserAgent'] != 'nullvalue':
        fgourl.user_agent_ = env_vars['UserAgent']

    if userNums == authKeyNums and userNums == secretKeyNums:
        fgourl.ReadConf()
        fgourl.gameData()
        print(f'待签到: {userNums}个')
        res = '【登录信息】\n'
        for i in range(userNums):
            try:
                instance = user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(3)
                res += instance.topLogin()
                time.sleep(2)
                instance.topHome()
                time.sleep(2)
            except Exception as ex:
                print(f'{i}th user login failed: {ex}')
                traceback.print_exc()

        fgourl.UploadFileToRepo(mytime.GetNowTimeFileName(), res, mytime.GetNowTimeFileName())
        fgourl.SendMessageToAdmin(res)
    else:
        print('账号密码数量不匹配')

if __name__ == '__main__':
    main()
