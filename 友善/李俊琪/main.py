import requests
import os
import pickle

import lookup_auto


WELCOME='Welcome！\nThis script is designed for checking the availability of domain names based on Godaddy API\nTry "?" for Help.\n'
function_list={
    'l':'lookup_one',
    'ml':'multi_inquiry',
    'f':'favorite_names',
    'auto':'lookup_auto.auto_lookup_short_domain_name',
    '?':'help_page'
}

def lookup_one(name):   #单个域名可用性查询
    RESET=False         #当出现timeout，ConnectionError时，不执行下面一系列操作

    baseurl="https://api.godaddy.com/v1/domains/available"
    header={'accept':'application/json','Authorization':'sso-key e42s1CST1356_Bp5jvuAH2iU5CJeyGWZCiA:Bp7TvXYeCk6YR2XZuAFXzn'}
    parameter_diction={}
    parameter_diction['domain']=name
    try:
        r=requests.get(baseurl,headers=header,params=parameter_diction,timeout=3)
    except requests.exceptions.Timeout:
        print('Timeout. Please try it again.')
        RESET=True
    except requests.exceptions.ConnectionError:
        print('Connection error. Please check your network')
        RESET=True

    if not RESET:
        #print(r.status_code)
        #print(r.url)
        r_obj=r.json()
        #print(r_obj)
        if 'available' in r_obj.keys():
            try:
                print('\n{} availability:{}\n'.format(r_obj['domain'],r_obj['available']))
            except KeyError as e:
                print(e)
        else:
            try:
                print('\n{}:{}\n'.format(name[-1],r_obj['code']))#查询失败的json不包含域名，所以从name中调取域名来输出
            except:
                print('\nfailed somehow\n')



def multi_inquiry(*args): #多个域名可用性查询
    RESET=False

    baseurl="https://api.godaddy.com/v1/domains/available"
    header={'accept':'application/json','Authorization':'sso-key e42s1CST1356_Bp5jvuAH2iU5CJeyGWZCiA:Bp7TvXYeCk6YR2XZuAFXzn'}
    try:
        r=requests.post(baseurl,headers=header,json=args[0],timeout=3)  #args是tuple args[0]是list
    except requests.exceptions.Timeout:
        print('Timeout. Please try it again.')
        RESET=True
    except requests.exceptions.ConnectionError:
        print('Connection error. Please check your network')
        RESET=True
    
    if not RESET:
        #print(args)
        #print(r.status_code)
        #print(r.url)
        r_obj=r.json()
        #print(r_obj)
        
        print("\n")#这个看起来很SB的语句是用来美化输出结果的

        if 'domains' in r_obj and r_obj['domains'] !=None:
            for item0 in r_obj['domains']:
                print("{:18} availability: {}".format(item0['domain'],item0['available']))
        
        if 'errors' in r_obj:
            for item1 in r_obj['errors']:
                print('{:18} {:12}: {}'.format(item1['domain'],'ErrorMessage',item1['message']))
        
        print("\n")#美化输出结果

def favorite_names(INPUT):  #保存一些想要的域名，然后查询 下面一行的对其懒得用format再改。直接用的空格。。。
    F_TIP='Please use "see" to check your list \n"add <name(s)>" to append the list of your favorite domain names\n"del <name>"    to delete one(only one!) name that stored in the list.\n"lookup"        to check if they are available.\n"x"             to exit this mode\n'
    print(F_TIP)

    if os.path.exists('favorite_list'): #检查保存的pickle是否存在 存在则调用保存的域名列表，不存在则新建
        with open('favorite_list','rb') as f:
            favorite_list=pickle.load(f)
    else:
        favorite_list=[]
    
    while 1:
        f_input=input('>>:').strip()
        if not f_input:  #用来排除什么都不输入直接按回车,和只输入空格的报错
            continue
        f_token=f_input.split()

        if f_token[0]=='x':
            with open('favorite_list','wb') as f:   #保存列表到文件
                pickle.dump(favorite_list,f)
            print('Return to main page')
            break

        elif f_token[0]=='see':
            print(favorite_list,"\n")

        elif f_token[0]=='add':
            favorite_list +=f_token[1:]
            print('now:',favorite_list,"\n")

        elif f_token[0]=='lookup':
            multi_inquiry(favorite_list)
            print('complete!\n')

        elif f_token[0]=='del':
            try:
                favorite_list.remove(f_token[1])
                print('now:',favorite_list,"\n")
                print('success!\n')
            except ValueError:
                print('Error. {} not in your list\n'.format(f_token[1]))

        else:
            print('bad usage.\n',F_TIP,"\n")

def help_page(INPUT):
    H_TIP='\n{:12}Look up one domain name\n{:12}Look up several domain names\n{:12}Automatically check if ".gs"short domain names are available\n{:12}Enter "favorite mode". In this mode, you can create a list of domain names and check their availability.\n\t    The list of domain names will be stored to help you check their availability next time\n'.format('l <name>','ml <names>','auto','f',)
    print(H_TIP)




def main():
    print(WELCOME)
    while 1:
        commands=input('Command(? for help):').strip()
        if not commands: #排除输入空格 空输入的错误
            continue
        token=commands.split()  
        
        if token[0] in function_list:
            if len(token)==1 and token[0] != 'f' and token[0] != '?' and token[0] != 'auto': #排除不给参数导致的错误
                print('\nError: missing parameter\nTry "?" for help.\n')
                continue
            try:
                eval(function_list[token[0]])(token[1:])
            except IndexError:  #用来捕捉其他函数中需要输入的错误，比如f
                print('\nFailed somehow. Please check your input\n')

        elif token[0]=='q':
            print('\nThanks for using!\n')
            break
        else:
            print('\n{}: Unknown command.\nEnter "?" for help.\n'.format(token[0]))

if __name__ == "__main__":
    main()