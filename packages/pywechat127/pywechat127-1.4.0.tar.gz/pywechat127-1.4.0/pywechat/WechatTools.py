'''
WechatTools
---------------
该模块中封装了一系列关于PC微信的工具,主要包括:检测微信运行状态;\n
打开微信主界面内绝大多数界面\n
模块:\n
---------------
Tools:一些关于PC微信的工具,以及13个open方法用于打开微信主界面内所有能打开的界面\n
API:打开指定公众号与微信小程序以及视频号,可为微信内部小程序公众号自动化操作提供便利\n
------------------------------------
函数:\n
函数为上述模块内的所有方法\n
--------------------------------------
使用该模块的方法时,你可以:\n
from pywechat.WechatTools import API \n
API.open_wechat_miniprogram(program_name='问卷星')\n
或者:\n
from pywechat import WechatTools as wt\n
wt.open_wechat_miniprogram(program='问卷星')\n
'''
############################依赖环境###########################
import os
import time
import psutil
import win32api
import pyautogui
import win32gui
import win32con
import subprocess
from win32gui import FindWindow,IsIconic
from pywinauto import mouse
from pywinauto import Desktop
from pywechat.Errors import PathNotFoundError
from pywechat.Errors import NetWorkNotConnectError
from pywechat.Errors import NoSuchFriendError
from pywechat.Errors import TimeNotCorrectError
from pywechat.Errors import ScanCodeToLogInError
from pywechat.Errors import WeChatNotStartError
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError
from pywechat.Uielements import Login_window,Main_window,ToolBar,Independent_window
from pywechat.WinSettings import Systemsettings
from pywinauto.timings import TimeoutError,Timings
Timings.fast()
##########################################################################################
pyautogui.FAILSAFE = False#防止鼠标在屏幕边缘处造成的误触
class Tools():
    '''该模块中封装了关于PC微信的工具\n
    以及13个open方法用于打开微信主界面内所有能打开的界面\n
    ''' 
    def is_wechat_running():
        '''这个函数通过检测当前windows进程中\n
        是否有WeChat.exe该项进程来判断微信是否在运行'''
        flag=0
        for process in psutil.process_iter(['name']):
            if 'WeChat.exe' in process.info['name']:
                    flag=1
                    break
        if flag:#count不为0，表明微信在运行，即微信已登录
            return True
        else:#count为0,表明微信不在运行，即微信未登录
            return False

    def find_wechat_path(copy_to_clipboard:bool=True):
        '''该方法用来查找正在运行的微信的路径'''
        wechat_path=None
        for process in psutil.process_iter(['name','exe']):
            if 'WeChat.exe' in process.info['name']:
                wechat_path=process.info['exe']
                break
        if wechat_path:
            if copy_to_clipboard:
                Systemsettings.copy_text_to_windowsclipboard(wechat_path)
                print("已将微信程序路径复制到剪贴板")
            return wechat_path
        else:
            raise WeChatNotStartError(f'微信未启动,请启动后再调用此函数！')

    def find_wechat_pid():
        '''该方法用来查找正在运行的微信进程的PID'''
        wechat_pids=[]
        for process in psutil.process_iter(['name','pid']):
            if 'WeChat.exe' in process.info['name']:
                wechat_pid=process.info['pid']
                wechat_pids.append(wechat_pid)
            if 'Wechat.exe' in process.info['name']:
                wechat_pids.append(wechat_pid)
        if wechat_pids[0]:
            return wechat_pid
        else:
            print('微信未启动,请启动后再调用此函数！')
            return None

    
    def set_wechat_as_environ_path():
        '''该函数用来自动打开系统环境变量设置界面,将微信路径自动添加至其中'''
        subprocess.Popen(["SystemPropertiesAdvanced.exe"])
        os.environ.update({"__COMPAT_LAYER":"RUnAsInvoker"})#添加管理员权限
        time.sleep(3)
        systemwindow=win32gui.FindWindow(None,u'系统属性')
        if win32gui.IsWindow(systemwindow):#将系统变量窗口置于桌面最前端
            win32gui.ShowWindow(systemwindow,win32con.SW_SHOW)
            win32gui.SetForegroundWindow(systemwindow)     
        pyautogui.hotkey('alt','n',interval=0.5)#添加管理员权限后使用一系列快捷键来填写微信刻路径为环境变量
        pyautogui.hotkey('alt','n',interval=0.5)
        pyautogui.press('shift')
        pyautogui.typewrite('wechatpath')
        try:
            Tools.find_wechat_path()
            pyautogui.hotkey('Tab',interval=0.5)
            pyautogui.hotkey('ctrl','v')
            pyautogui.press('enter')
            pyautogui.press('enter')
            pyautogui.press('esc')
        except WeChatNotStartError:
            pyautogui.press('esc')
            pyautogui.hotkey('alt','f4')
            pyautogui.hotkey('alt','f4')
            raise WeChatNotStartError(f'微信未启动,请启动后再调用此函数！')
 
    
    def judge_wechat_state():
        '''该函数用来判断微信运行状态'''
        time.sleep(1.5)
        if Tools.is_wechat_running():
            window=win32gui.FindWindow('WeChatMainWndForPC','微信')
            if IsIconic(window):
                return '主界面最小化'
            elif win32gui.IsWindowVisible(window):
                win32gui.SetForegroundWindow(window)
                return '主界面可见'
            else:
                return '主界面不可见'
        else:
            return "微信未打开"
    
    
    def move_window_to_center(Window:dict=Main_window.MainWindow,Window_handle:int=0):
        '''该函数用来将已打开的界面移动到屏幕中央,使用时需注意传入参数为窗口的字典形式\n
        需要包括class_name与title两个键值对,任意一个没有值可以使用None代替\n
        '''
        desktop=Desktop(**Independent_window.Desktop)
        class_name=Window['class_name']
        title=Window['title']
        if Window_handle==0:
            handle=win32gui.FindWindow(class_name,title)
        else:
            handle=Window_handle
        screen_width,screen_height=win32api.GetSystemMetrics(win32con.SM_CXSCREEN),win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        move_window=desktop.window(handle=handle)
        window_width,window_height=move_window.rectangle().width(),move_window.rectangle().height()
        new_left=(screen_width-window_width)//2
        new_top=(screen_height-window_height)//2
        if screen_width!=window_width:
            win32gui.SetForegroundWindow(handle)
            win32gui.MoveWindow(handle,new_left,new_top,window_width,window_height,True)
    
    def connect_to_wechat(wechat_path): 
        '''该方法用于更高效的连接到微信主界面\n
        尽量避免同时使用pywinauto applications中的start与connect方法,使用subprocess.Popen代替start\n
        并且先使用win32GUI查找到窗口句柄后再传入pywinauto的connect方法,相较于直接传入窗口的信息更快'''
        #微信未打开，有登录选项
        max_retry_times=20
        retry_interval=0.4
        counter=0
        if not Tools.is_wechat_running():
            subprocess.Popen(wechat_path)
            time.sleep(1)
            login_window_handle=FindWindow(Login_window.LoginWindow['class_name'],Login_window.LoginWindow['title'])
            login_window=Application(backend='uia').connect(handle=login_window_handle)
            Tools.move_window_to_center(Login_window.LoginWindow,Window_handle=login_window_handle)
            try:
                login_window=login_window.window(**Login_window.LoginWindow)
                login_button=login_window.child_window(**Login_window.LoginButton).wait(wait_for='visible',retry_interval=0.1,timeout=3)
                login_button.set_focus()
                login_button.click_input()
                main_window_handle=0
                while not main_window_handle:
                    main_window_handle=FindWindow(Main_window.MainWindow['class_name'],Main_window.MainWindow['title'])
                    if main_window_handle:
                        break
                    counter+=1
                    time.sleep(retry_interval)
                    if counter>=max_retry_times:
                        raise NetWorkNotConnectError(f'网络可能未连接,暂时无法进入微信!请尝试连接wifi扫码进入微信')
                if main_window_handle:
                    wechat=Application(backend='uia').connect(handle=main_window_handle)
                    main_window=wechat.window(**Main_window.MainWindow)
                    Tools.move_window_to_center(Window_handle=main_window_handle)
                    return main_window#主界面
            except  TimeoutError:
                #有登录界面但是没找到进去微信按钮，只能扫码登录了
                raise ScanCodeToLogInError(f'你还未在手机端开启PC端微信自动登录,可在本次手动进入微信后在顶部登录选项勾选')
        else:
            #微信已经打开过，可能是登录界面，也可能是主界面，
            subprocess.Popen(wechat_path)
            time.sleep(1)
            login_window_handle=FindWindow(Login_window.LoginWindow['class_name'],Login_window.LoginWindow['title'])
            if login_window_handle:
                login_window=Application(backend='uia').connect(handle=login_window_handle)
                Tools.move_window_to_center(Login_window.LoginWindow,login_window_handle)
                try:
                    login_window=login_window.window(**Login_window.LoginWindow)
                    login_button=login_window.child_window(**Login_window.LoginButton).wait(wait_for='visible',retry_interval=0.1,timeout=3)
                    login_button.set_focus()
                    login_button.click_input()
                    main_window_handle=0
                    while not main_window_handle:
                        main_window_handle=FindWindow(Main_window.MainWindow['class_name'],Main_window.MainWindow['title'])
                        if main_window_handle:
                            break
                        counter+=1
                        time.sleep(retry_interval)
                        if counter>=max_retry_times:
                            raise NetWorkNotConnectError(f'网络可能未连接,暂时无法进入微信!请尝试连接wifi扫码进入微信')
                    if main_window_handle:
                        wechat=Application(backend='uia').connect(handle=main_window_handle)
                        main_window=wechat.window(**Main_window.MainWindow)
                        Tools.move_window_to_center(Window_handle=main_window_handle)
                        return main_window#主界面
                except  TimeoutError:
                    raise ScanCodeToLogInError(f'你还未在手机端开启PC端微信自动登录,可在本次手动进入微信后在顶部登录选项勾选')
            else:
                main_window_handle=FindWindow(Main_window.MainWindow['class_name'],Main_window.MainWindow['title'])
                wechat=Application(backend='uia').connect(handle=main_window_handle)
                Tools.move_window_to_center() 
                main_window=wechat.window(**Main_window.MainWindow)
                return main_window
     
    def open_wechat(wechat_path:str=None,is_maximize:bool=True):
        '''
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        微信的打开分为四种情况:\n
        1.未登录,此时调用该函数会启动wechat_path路径下的wechat.exe,在弹出的登录界面中点击进入微信打开微信主界面\n
        启动并点击登录进入微信(注:需勾选自动登录按钮,否则启动后为扫码登录)\n
        2.未登录但已弹出微信的登录界面,此时会自动点击进入微信打开微信\n
        注意:未登录的情况下打开微信需要在手机端第一次扫码登录后勾选自动登入的选项,否则启动微信后\n
        聊天界面没有进入微信按钮,将会触发异常提示扫码登录\n
        3.已登录，主界面最小化在状态栏，此时调用该函数会直接打开后台中的微信。\n
        4.已登录，主界面关闭，此时调用该函数会打开已经关闭的微信界面。
        '''
        wechat_environ_path=[path for path in dict(os.environ).values() if 'WeChat.exe' in path]#windows环境变量中查找WeChat.exe路径
        if  wechat_environ_path:#已将WeChat.exe设置为windows环境变量
            main_window=Tools.connect_to_wechat(wechat_path=wechat_environ_path[0])
            if is_maximize:
                    main_window.maximize()
            return main_window
        else:
                if not wechat_path:
                    raise PathNotFoundError(f'未检测到微信文件路径!请输入微信文件路径或将其添加至环境变量中')
                main_window=Tools.connect_to_wechat(wechat_path=wechat_path)
                if is_maximize:
                    main_window.maximize()
                return main_window
                        
    
    def open_settings(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
        该方法用来打开微信设置界面。\n
        '''   
        main_window=None
        result=Tools.judge_wechat_state()
        if result=='主界面可见':
            wechat=Application(backend='uia').connect(**Main_window.MainWindow)
            main_window=wechat.window(**Main_window.MainWindow)
            Tools.move_window_to_center()
            if is_maximize:
                main_window.maximize()
        else:
            main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        Toolbar=main_window.child_window(**Main_window.Toolbar)
        setting=Toolbar.children(control_type='Pane',title='')[3].children(control_type='Button',title="设置及其他")[0]
        setting.click_input()
        settings_menu=main_window.child_window(**Main_window.SettingsMenu)
        settings_button=settings_menu.child_window(control_type='Button',title="设置")
        settings_button.click_input() 
        time.sleep(2)
        desktop=Desktop(**Independent_window.Desktop)
        settings_window=desktop.window(**Independent_window.SettingWindow)
        if close_wechat:
            main_window.close()
        return settings_window
    
                        
    def open_dialog_window(friend:str,wechat_path:str=None,is_maximize:bool=True,search_pages:int=10): 
        '''
        friend:好友或群聊备注名称,需提供完整名称\n
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        search_pages:在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏法搜索好友信息打开聊天界面\n
        该方法用于打开某个好友的聊天窗口
        '''
        chat=None
        def is_in_searh_result(friend,search_result):
            listitem=search_result.children(control_type="ListItem")
            names=[item.window_text() for item in listitem]
            if names[0]==friend:
                return True
            else:
                return False
        #如果search_pages不为0,即需要在会话列表中滚动查找时，使用find_friend_in_Messagelist方法找到好友,并点击打开对话框
        if search_pages:
            chat,main_window=Tools.find_friend_in_MessageList(friend=friend,wechat_path=wechat_path,is_maximize=False,search_pages=search_pages)
            if is_maximize:
                main_window.maximize()
            if chat:#chat不为None,即说明find_friend_in_MessageKist找到了聊天窗口chat,直接返回结果
                return chat,main_window
            else:  #chat为None没有在会话列表中找到好友,直接在顶部搜索栏中搜索好友
                #先点击侧边栏的聊天按钮切回到聊天主界面
                Toolbar=main_window.child_window(**Main_window.Toolbar)
                chat_button=Toolbar.children(control_type="Button",title='聊天')[0]
                chat_button.click_input()
                time.sleep(1)
                #顶部搜索按钮搜索好友
                search=main_window.child_window(**Main_window.Search).wait(wait_for='visible',retry_interval=0.1,timeout=10)
                search.click_input()
                search.type_keys(friend,with_spaces=True)
                time.sleep(2)
                search_result=main_window.child_window(**Main_window.SearchResult)
                if is_in_searh_result(friend=friend,search_result=search_result):
                    pyautogui.hotkey('enter')
                    chat=main_window.child_window(title=friend,control_type='Edit').wait(wait_for='visible',retry_interval=0.1,timeout=10)
                    return chat,main_window #同时返回搜索到的该好友的聊天窗口与主界面！若只需要其中一个需要使用元祖索引获取。
                else:#搜索结果栏中没有关于传入参数friend好友昵称或备注的搜索结果，关闭主界面,引发异常
                    main_window.close()
                    raise NoSuchFriendError(f"好友或群聊备注有误！查无此人！")
        else: #searchpages为0，不再会话列表查找
            #这部分代码先判断微信主界面是否可见,如果可见不需要重新打开,这在多个close_wechat为False需要进行来连续操作的方式使用时要用到
            main_window=None
            
            result=Tools.judge_wechat_state()
            if result=='主界面可见':
                wechat=Application(backend='uia').connect(**Main_window.MainWindow)
                main_window=wechat.window(**Main_window.MainWindow)
                Tools.move_window_to_center()
                if is_maximize:
                    main_window.maximize()
            else:
                main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
                if is_maximize:
                    main_window.maximize()
            #先看看当前聊天界面是不是好友的聊天界面
            current_chat=main_window.child_window(**Main_window.CurrentChatWindow)
            #如果当前主界面是某个好友的聊天界面且聊天界面顶部的名称为好友名称，直接返回结果
            if current_chat.exists() and friend in current_chat.window_text():
                chat=current_chat
                chat.click_input()
                return chat,main_window
            else:#否则直接从顶部搜索栏出搜索结果
                Toolbar=main_window.child_window(**Main_window.Toolbar)
                chat_button=Toolbar.children(control_type="Button",title='聊天')[0]
                chat_button.click_input()
                time.sleep(1)
                search=main_window.child_window(**Main_window.Search).wait(wait_for='visible',retry_interval=0.1,timeout=10)
                search.click_input()
                search.type_keys(friend,with_spaces=True)
                time.sleep(2)
                search_result=main_window.child_window(**Main_window.SearchResult)
                if is_in_searh_result(friend=friend,search_result=search_result):
                    pyautogui.hotkey('enter')
                    chat=main_window.child_window(title=friend,control_type='Edit').wait(wait_for='visible',retry_interval=0.1,timeout=10)
                    return chat,main_window #同时返回该好友的聊天窗口与主界面！若只需要其中一个需要使用元祖索引获取。
                else:
                    main_window.close()
                    raise NoSuchFriendError(f"好友或群聊备注有误！查无此人！")

    
    def find_friend_in_MessageList(friend:str,wechat_path:str=None,is_maximize:bool=False,search_pages:int=10):
        '''
        friend:好友或群聊备注名称,需提供完整名称\n
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        该函数用于在会话列表中查询是否存在待查询好友。\n
        若存在:返回值为 (chat,main_window) 同时返回好友聊天界面与主界面\n
        否则:返回值为 (None,main_window)只返回主界面\n
        search_pages:在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏法搜索好友信息打开聊天界面\n
        该方法用于在会话列表中寻找好友
        '''
        def get_window(friend):
            message_list=message_list_pane.children(control_type='ListItem')
            buttons=[friend.children()[0].children()[0] for friend in message_list]
            friend_button=None
            for i in range(len(buttons)):
                if friend == buttons[i].texts()[0]:
                    friend_button=buttons[i]
                    break
            if i==len(buttons)-1:
                return friend_button,i
            else:
                return friend_button,None
        main_window=None
        chat=None
         #这部分代码先判断微信主界面是否可见,如果可见不需要重新打开,这在多个close_wechat为False需要进行来连续操作的方式使用时要用到
        
        result=Tools.judge_wechat_state()
        if result=='主界面可见':
            wechat=Application(backend='uia').connect(**Main_window.MainWindow)
            main_window=wechat.window(**Main_window.MainWindow)
            Tools.move_window_to_center()
            if is_maximize:
                main_window.maximize()
        else:
            main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        ####################################################################
        #先看看当前聊天界面是不是好友的聊天界面
        current_chat=main_window.child_window(**Main_window.CurrentChatWindow)
        if current_chat.exists() and friend in current_chat.window_text():
            #如果当前主界面是某个好友的聊天界面且聊天界面顶部的名称为好友名称，直接返回结果
            chat=current_chat
            chat.click_input()
            return chat,main_window
        else:#否则直接从顶部搜索栏出搜索结果
            Toolbar=main_window.child_window(**Main_window.Toolbar)
            chat_button=Toolbar.children(control_type="Button",title='聊天')[0]
            chat_button.click_input()
            time.sleep(1)
            message_list_pane=main_window.child_window(**Main_window.MessageList)
            message_list_pane.set_focus()
            message_list=message_list_pane.children(control_type='ListItem')
            if len(message_list)==0:
                return None,main_window
            rectangle=message_list_pane.rectangle()
            mouse.wheel_click(coords=(rectangle.right-5, rectangle.top+20))
            pyautogui.press('Home')
            for _ in range(search_pages):
                friend_button,index=get_window(friend)
                if friend_button:
                    if index:
                        rec=friend_button.rectangle()
                        mouse.click(coords=(int(rec.left+rec.right)//2,rec.top-12))
                        chat=main_window.child_window(title=friend,control_type='Edit').wait(wait_for='visible',retry_interval=0.1,timeout=10)
                        chat.click_input()
                    else:
                        friend_button.click_input()
                        chat=main_window.child_window(title=friend,control_type='Edit').wait(wait_for='visible',retry_interval=0.1,timeout=10)
                        chat.click_input()
                    break
                else:
                    pyautogui.press("pagedown")
                    time.sleep(1)
            mouse.wheel_click(coords=(rectangle.right-5, rectangle.top+20))
            pyautogui.press('Home')
            return chat,main_window 
    
    
    def open_friend_settings(friend:str,wechat_path:str=None,is_maximize:bool=True):
        '''
        friend:好友备注名称,需提供完整名称\n
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        该方法用于打开好友设置界面\n
        '''
        main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize)[1]
        ChatMessage=main_window.child_window(**Main_window.ChatMessage)
        ChatMessage.click_input()
        friend_settings_window=main_window.child_window(**Main_window.FriendSettingsWindow)
        return friend_settings_window,main_window
 
    
    def open_contacts_settings(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
        该方法用于打开通讯录设置界面
        '''
        desktop=Desktop(**Independent_window.Desktop)
        main_window=None
        
        result=Tools.judge_wechat_state()
        if result=='主界面可见':
            wechat=Application(backend='uia').connect(**Main_window.MainWindow)
            main_window=wechat.window(**Main_window.MainWindow)
            Tools.move_window_to_center()
            if is_maximize:
                main_window.maximize()
        else:
            main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        toolbar=main_window.child_window(control_type='ToolBar',title='导航')
        contacts=toolbar.child_window(**ToolBar.Contacts)
        contacts.set_focus()
        contacts.click_input()
        ContactsLists=main_window.child_window(title='联系人',control_type='List')
        #############################
        rec=ContactsLists.rectangle()
        mouse.click(coords=(rec.right-5,rec.top))
        pyautogui.press('Home')
        pyautogui.press('pageup')
        contacts_settings=main_window.child_window(**Main_window.ContactsManage)#通讯录管理窗口按钮 
        contacts_settings.set_focus()
        contacts_settings.click_input()
        contacts_settings_window=desktop.window(**Independent_window.ContactManagerWindow)
        if close_wechat:
            main_window.close()
        return contacts_settings_window,main_window
    
    
    def open_friend_settings_menu(friend:str,wechat_path:str=None,is_maximize:bool=True):
        '''
        friend:好友备注名称,需提供完整名称\n
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        该方法用于打开好友设置界面
        '''
        friend_settings_window,main_window=Tools.open_friend_settings(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize)
        friend_button=friend_settings_window.child_window(title=friend,control_type="Button",found_index=0)
        friend_button.click_input()
        profile_window=friend_settings_window.child_window(class_name="ContactProfileWnd",control_type="Pane",framework_id='Win32')
        more_button=profile_window.child_window(title='更多',control_type='Button')
        more_button.click_input()
        friend_menu=profile_window.child_window(control_type="Menu",title="",class_name='CMenuWnd',framework_id='Win32')
        return friend_menu,friend_settings_window,main_window
         
    
    def open_collections(wechat_path:str=None,is_maximize:bool=True):
        '''
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        该方法用于打开收藏
        '''
        main_window=None
        
        result=Tools.judge_wechat_state()
        if result=='主界面可见':
            wechat=Application(backend='uia').connect(**Main_window.MainWindow)
            main_window=wechat.window(**Main_window.MainWindow)
            Tools.move_window_to_center()
            if is_maximize:
                main_window.maximize()
        else:
            main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        Toolbar=main_window.child_window(**Main_window.Toolbar)
        collections_button=Toolbar.child_window(**ToolBar.Collections)
        collections_button.click_input()
        return main_window
    
    
    def open_group_settings(group:str,wechat_path:str=None,is_maximize:bool=True):
        '''
        group:群聊备注名称,需提供完整名称\n
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        '''
        main_window=Tools.open_dialog_window(friend=group,wechat_path=wechat_path,is_maximize=False)[1]
        if is_maximize:
            main_window.maximize()
        ChatMessage=main_window.child_window(**Main_window.ChatMessage)
        ChatMessage.click_input()
        group_settings_window=main_window.child_window(**Main_window.GroupSettingsWindow)
        group_settings_window.child_window(title="群聊名称",control_type="Text").click_input()
        pyautogui.press('pagedown')
        return group_settings_window,main_window

    
    def open_wechat_moments(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
        该方法用于打开微信朋友圈
        '''
        main_window=None
        
        result=Tools.judge_wechat_state()
        if result=='主界面可见':
            wechat=Application(backend='uia').connect(**Main_window.MainWindow)
            main_window=wechat.window(**Main_window.MainWindow)
            Tools.move_window_to_center()
            if is_maximize:
                main_window.maximize()
        else:
            main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        Toolbar=main_window.child_window(**Main_window.Toolbar)
        moments_button=Toolbar.child_window(**ToolBar.Moments)
        moments_button.click_input()
        desktop=Desktop(**Independent_window.Desktop)
        moments_window=desktop.window(**Independent_window.MomentsWindow)
        if close_wechat:
            main_window.close()
        return moments_window
    
    
    def open_chat_files(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
        该方法用于打开聊天文件
        '''
        main_window=None
              
        result=Tools.judge_wechat_state()
        if result=='主界面可见':          
            wechat=Application(backend='uia').connect(**Main_window.MainWindow)
            main_window=wechat.window(**Main_window.MainWindow)
            Tools.move_window_to_center()
            if is_maximize:
                main_window.maximize()
        else:
            main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        Toolbar=main_window.child_window(**Main_window.Toolbar)
        moments_button=Toolbar.child_window(**ToolBar.ChatFiles)
        moments_button.click_input()
        desktop=Desktop(**Independent_window.Desktop)
        chat_files_window=desktop.window(**Independent_window.ChatFilesWindow)
        if close_wechat:
            main_window.close()
        return chat_files_window
    
    
    def open_friend_profile(friend:str,wechat_path:str=None,is_maximize:bool=True):
        '''
        friend:好友备注名称,需提供完整名称\n
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        该方法用于打开好友个人简介界面
        '''
        friend_settings_window,main_window=Tools.open_friend_settings(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize)
        friend_button=friend_settings_window.child_window(title=friend,control_type="Button",found_index=0)
        friend_button.click_input()
        profile_window=friend_settings_window.child_window(class_name="ContactProfileWnd",control_type="Pane",framework_id='Win32')
        return profile_window,main_window
    
    
    def open_contacts(wechat_path:str=None,is_maximize:bool=True):
        '''
        friend:好友或群聊备注名称,需提供完整名称\n
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        该方法用于打开微信通信录界面
        '''
        main_window=None
        result=Tools.judge_wechat_state()
        if result=='主界面可见':
            wechat=Application(backend='uia').connect(**Main_window.MainWindow)
            main_window=wechat.window(**Main_window.MainWindow)
            Tools.move_window_to_center()
            if is_maximize:
                main_window.maximize()
        else:
            main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        toolbar=main_window.child_window(**Main_window.Toolbar)
        contacts=toolbar.child_window(**ToolBar.Contacts)
        contacts.set_focus()
        contacts.click_input()
        ContactsLists=main_window.child_window(**Main_window.ContactsList)
        rec=ContactsLists.rectangle()
        mouse.click(coords=(rec.right-5,rec.top))
        pyautogui.press('Home')
        pyautogui.press('pageup')
        return main_window

    
    def open_chat_history(friend:str,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        friend:好友备注名称,需提供完整名称\n
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        该方法用于打开好友聊天记录界面\n
        '''
        main_window=None
        friend_settings_window,main_window=Tools.open_friend_settings(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize)
        chat_history_button=friend_settings_window.child_window(title='聊天记录',control_type='Button')
        chat_history_button.click_input()
        desktop=Desktop(**Independent_window.Desktop)
        chat_history_window=desktop.window(**Independent_window.ChatHistoryWindow)
        if close_wechat:
            main_window.close()
        return chat_history_window,main_window

class API():
    '''这个模块包括打开小程序,打开微信公众号,打开微信朋友圈,打开视频号并返回其主界面(pywinauto--window)的三个功能\n
    若有其他开发者需要使用到微信内的这三个功能进行自动化操作可调用此模块\n
    '''
    
    def open_wechat_miniprogram(program_name:str,load_delay:int=3,wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        program_name:微信小程序名字\n
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
        '''
        main_window=None
        
        result=Tools.judge_wechat_state()
        if result=='主界面可见':
            wechat=Application(backend='uia').connect(**Main_window.MainWindow)
            main_window=wechat.window(**Main_window.MainWindow)
            Tools.move_window_to_center()
            if is_maximize:
                main_window.maximize()
        else:
            main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        Toolbar=main_window.child_window(**Main_window.Toolbar)
        program_button=Toolbar.children(control_type="Pane",title="")[1].children(control_type="Pane",title="")[0].children(control_type="Button",title='小程序面板')[0]
        program_button.click_input()
        if close_wechat:
            main_window.close()
        desktop=Desktop(**Independent_window.Desktop)
        program_window=desktop.window(**Independent_window.MiniProgramWindow)
        time.sleep(load_delay)
        search=program_window.child_window(control_type="Pane",title="",found_index=1).child_window(title="",control_type="Tab").children(title="",control_type="Pane")[1]
        search.click_input()
        search.type_keys(program_name,with_spaces=True)
        pyautogui.press("enter")
        time.sleep(load_delay)
        search_result=program_window.child_window(control_type="Document",class_name="Chrome_RenderWidgetHostHWND")
        program_button=search_result.child_window(control_type="ListItem",found_index=4)
        program_button.click_input()
        main=search_result.child_window(control_type="Button",title_re=program_name,found_index=0,framework_id="Chrome")
        time.sleep(load_delay)
        main.click_input()
        time.sleep(load_delay)
        program_window=desktop.window(title=program_name,framework_id="Win32",control_type="Pane",class_name="Chrome_WidgetWin_0")
        return program_window
    
    
    def open_wechat_official_account(official_acount_name:str,load_delay:int=3,wechat_path:str=None,is_maximize:bool=True):
        '''
        official_acount_name:微信公众号名称\n
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        该方法用于打开微信公众号
        '''
        main_window=None
        
        result=Tools.judge_wechat_state()
        if result=='主界面可见':
            wechat=Application(backend='uia').connect(**Main_window.MainWindow)
            main_window=wechat.window(**Main_window.MainWindow)
            Tools.move_window_to_center()
            if is_maximize:
                main_window.maximize()
        else:
            main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        Toolbar=main_window.child_window(**Main_window.Toolbar)
        program_button=Toolbar.children(control_type="Pane",title="")[1].children(control_type="Pane",title="")[0].children(control_type="Button",title='小程序面板')[0]
        program_button.click_input()
        desktop=Desktop(**Independent_window.Desktop)
        program_window=desktop.window(**Independent_window.MiniProgramWindow)
        main_window.close()
        time.sleep(load_delay)
        search=program_window.child_window(control_type="Pane",title="",found_index=1).child_window(title="",control_type="Tab").children(title="",control_type="Pane")[1]
        search.click_input()
        search.type_keys(official_acount_name,with_spaces=True)
        pyautogui.press("enter")
        time.sleep(load_delay)
        search_result=program_window.child_window(control_type="Document",class_name="Chrome_RenderWidgetHostHWND")
        official_acount_button=search_result.child_window(control_type="ListItem",found_index=3)
        official_acount_button.click_input()
        try:
            result=search_result.child_window(control_type="Button",found_index=1,framework_id="Chrome")
            time.sleep(load_delay)
            result.click_input()
            time.sleep(load_delay)
        except ElementNotFoundError:
            print("查无此公众号！")
    
    
    def open_search(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
        该方法用于打开搜一搜
        '''
        main_window=None
        
        result=Tools.judge_wechat_state()
        if result=='主界面可见':
            wechat=Application(backend='uia').connect(**Main_window.MainWindow)
            main_window=wechat.window(**Main_window.MainWindow)
            Tools.move_window_to_center()
            if is_maximize:
                main_window.maximize()
        else:
            main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        Toolbar=main_window.child_window(**Main_window.Toolbar)
        search_button=Toolbar.child_window(**ToolBar.Search)
        search_button.click_input()
        desktop=Desktop(**Independent_window.Desktop)
        search_window=desktop.window(**Independent_window.SearchWindow)
        if close_wechat:
            main_window.close()
        return search_window    

    
    def open_channel(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
        该方法用于打开视频号\n        
        '''
        main_window=None
        
        result=Tools.judge_wechat_state()
        if result=='主界面可见':
            wechat=Application(backend='uia').connect(**Main_window.MainWindow)
            main_window=wechat.window(**Main_window.MainWindow)
            Tools.move_window_to_center()
            if is_maximize:
                main_window.maximize()

                
        else:
            main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        Toolbar=main_window.child_window(**Main_window.Toolbar)
        channel_button=Toolbar.child_window(**ToolBar.Channel)
        channel_button.click_input()
        desktop=Desktop(**Independent_window.Desktop)
        channel_window=desktop.window(**Independent_window.ChannelWindow)
        if close_wechat:
            main_window.close()
        return channel_window

    
    def open_top_stories(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
        '''
        wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
        这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
        若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
        is_maximize:微信界面是否全屏,默认全屏。\n
        close_wechat:任务结束后是否关闭微信,默认关闭\n
        该方法用于打开看一看
        '''
        main_window=None
        
        result=Tools.judge_wechat_state()
        if result=='主界面可见':
            wechat=Application(backend='uia').connect(**Main_window.MainWindow)
            main_window=wechat.window(**Main_window.MainWindow)
            Tools.move_window_to_center()
            if is_maximize:
                main_window.maximize()
        else:
            main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        Toolbar=main_window.child_window(**Main_window.Toolbar)
        top_stories_button=Toolbar.child_window(**ToolBar.Topstories)
        top_stories_button.click_input()
        desktop=Desktop(backend="uia")
        top_stories_window=desktop.window(**Independent_window.TopStoriesWindow)
        if close_wechat:
            main_window.close()
        return top_stories_window

def is_wechat_running():
    '''这个函数通过检测当前windows进程中\n
    是否有wechatappex该项进程来判断微信是否在运行'''
    flag=0
    for process in psutil.process_iter(['name']):
        if 'WeChat.exe' in process.info['name']:
            flag=1
            break
    if flag:#flag不为0，表明微信在运行，即微信已登录
         return True
    else:#flag为0,表明微信不在运行，即微信未登录
         return False

def connect_to_wechat(wechat_path): 
    '''该方法用于更高效的连接到微信主界面\n
    尽量避免同时使用pywinauto applications中的start与connect方法,使用subprocess.Popen代替start\n
    并且先使用win32GUI查找到窗口句柄后再传入pywinauto的connect方法,相较于直接传入窗口的信息更快'''
    #微信未打开，有登录选项
    max_retry_times=20
    retry_interval=0.4
    counter=0
    if not Tools.is_wechat_running():
        subprocess.Popen(wechat_path)
        time.sleep(2)
        login_window_handle=FindWindow(Login_window.LoginWindow['class_name'],Login_window.LoginWindow['title'])
        login_window=Application(backend='uia').connect(handle=login_window_handle)
        Tools.move_window_to_center(Login_window.LoginWindow,Window_handle=login_window_handle)
        try:
            login_window=login_window.window(**Login_window.LoginWindow)
            login_button=login_window.child_window(**Login_window.LoginButton).wait(wait_for='visible',retry_interval=0.1,timeout=3)
            login_button.set_focus()
            login_button.click_input()
            main_window_handle=0
            while not main_window_handle:
                main_window_handle=FindWindow(Main_window.MainWindow['class_name'],Main_window.MainWindow['title'])
                if main_window_handle:
                    break
                counter+=1
                time.sleep(retry_interval)
                if counter>=max_retry_times:
                    raise NetWorkNotConnectError(f'网络可能未连接,暂时无法进入微信!请尝试连接wifi扫码进入微信')
            if main_window_handle:
                wechat=Application(backend='uia').connect(handle=main_window_handle)
                main_window=wechat.window(**Main_window.MainWindow)
                Tools.move_window_to_center(Window_handle=main_window_handle)
                return main_window#主界面
        except  TimeoutError:
            #有登录界面但是没找到登录按钮，只能扫码登录了
            raise ScanCodeToLogInError(f'你还未在手机端开启PC端微信自动登录,可在本次扫码进入微信后在顶部登录选项勾选')
    else:
        #微信已经打开过，可能是登录界面，也可能是主界面，
        subprocess.Popen(wechat_path)
        time.sleep(2)
        login_window_handle=FindWindow(Login_window.LoginWindow['class_name'],Login_window.LoginWindow['title'])
        if login_window_handle:
            login_window=Application(backend='uia').connect(handle=login_window_handle)
            Tools.move_window_to_center(Login_window.LoginWindow,login_window_handle)
            try:
                login_window=login_window.window(**Login_window.LoginWindow)
                login_button=login_window.child_window(**Login_window.LoginButton).wait(wait_for='visible',retry_interval=0.1,timeout=3)
                login_button.set_focus()
                login_button.click_input()
                main_window_handle=0
                while not main_window_handle:
                    main_window_handle=FindWindow(Main_window.MainWindow['class_name'],Main_window.MainWindow['title'])
                    if main_window_handle:
                        break
                    counter+=1
                    time.sleep(retry_interval)
                    if counter>=max_retry_times:
                        raise NetWorkNotConnectError(f'网络可能未连接,暂时无法进入微信!请尝试连接wifi扫码进入微信')
                if main_window_handle:
                    wechat=Application(backend='uia').connect(handle=main_window_handle)
                    main_window=wechat.window(**Main_window.MainWindow)
                    Tools.move_window_to_center(Window_handle=main_window_handle)
                    return main_window#主界面
            except  TimeoutError:
                raise ScanCodeToLogInError(f'你还未在手机端开启PC端微信自动登录,可在本次扫码进入微信后在顶部登录选项勾选')
        else:
            main_window_handle=FindWindow(Main_window.MainWindow['class_name'],Main_window.MainWindow['title'])
            wechat=Application(backend='uia').connect(handle=main_window_handle)
            Tools.move_window_to_center() 
            main_window=wechat.window(**Main_window.MainWindow)
            return main_window

def open_wechat(wechat_path:str=None,is_maximize:bool=True):
    '''
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    微信的打开分为四种情况:\n
    1.未登录,此时调用该函数会启动wechat_path路径下的wechat.exe,在弹出的登录界面中点击进入微信打开微信主界面\n
    启动并点击登录进入微信(注:需勾选自动登录按钮,否则启动后为扫码登录)\n
    2.未登录但已弹出微信的登录界面,此时会自动点击进入微信打开微信\n
    注意:未登录的情况下打开微信需要在手机端第一次扫码登录后勾选自动登入的选项,否则启动微信后\n
    聊天界面没有进入微信按钮,将会触发异常提示扫码登录\n
    3.已登录，主界面最小化在状态栏，此时调用该函数会直接打开后台中的微信。\n
    4.已登录，主界面关闭，此时调用该函数会打开已经关闭的微信界面。
    '''
    wechat_environ_path=[path for path in dict(os.environ).values() if 'WeChat.exe' in path]#windows环境变量中查找WeChat.exe路径
    if  wechat_environ_path:#已将WeChat.exe设置为windows环境变量
        main_window=Tools.connect_to_wechat(wechat_path=wechat_environ_path[0])
        if is_maximize:
                main_window.maximize()
        return main_window
    else:
            if not wechat_path:
                raise PathNotFoundError(f'未检测到微信文件路径!请输入微信文件路径或将其添加至环境变量中')
            main_window=Tools.connect_to_wechat(wechat_path=wechat_path)
            if is_maximize:
                main_window.maximize()
            return main_window
                    

def find_friend_in_MessageList(friend:str,wechat_path:str=None,is_maximize:bool=False,search_pages:int=10):
    '''
    friend:好友或群聊备注名称,需提供完整名称\n
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于在会话列表中查询是否存在待查询好友。\n
    若存在:返回值为 (chat,main_window) 同时返回好友聊天界面与主界面\n
    否则:返回值为 (None,main_window)只返回主界面\n
    search_pages:在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏法搜索好友信息打开聊天界面\n
    该函数用于在会话列表中寻找好友,属于较为底层的函数不建议调用\n
    '''
    def get_window(friend):
        message_list=message_list_pane.children(control_type='ListItem')
        buttons=[friend.children()[0].children()[0] for friend in message_list]
        friend_button=None
        for i in range(len(buttons)):
            if friend == buttons[i].texts()[0]:
                friend_button=buttons[i]
                break
        if i==len(buttons)-1:
            return friend_button,i
        else:
            return friend_button,None
    chat=None
    main_window=None
    result=Tools.judge_wechat_state()
    if result=='主界面可见':
        wechat=Application(backend='uia').connect(**Main_window.MainWindow)
        main_window=wechat.window(**Main_window.MainWindow)
        Tools.move_window_to_center()
        if is_maximize:
            main_window.maximize()
    else:
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    current_chat=main_window.child_window(**Main_window.CurrentChatWindow)
    if current_chat.exists() and friend in current_chat.window_text():
        chat=current_chat
        chat.click_input()
        return chat,main_window
    else:
        Toolbar=main_window.child_window(**Main_window.Toolbar)
        chat_button=Toolbar.children(control_type="Button",title='聊天')[0]
        chat_button.click_input()
        time.sleep(1)
        message_list_pane=main_window.child_window(**Main_window.MessageList)
        message_list_pane.set_focus()
        message_list=message_list_pane.children(control_type='ListItem')
        if len(message_list)==0:
            return None,main_window
        rectangle=message_list_pane.rectangle()
        mouse.wheel_click(coords=(rectangle.right-5, rectangle.top+20))
        pyautogui.press('Home')
        for _ in range(search_pages):
            friend_button,index=get_window(friend)
            if friend_button:
                if index:
                    rec=friend_button.rectangle()
                    mouse.click(coords=(int(rec.left+rec.right)//2,rec.top-12))
                    chat=main_window.child_window(title=friend,control_type='Edit').wait(wait_for='visible',retry_interval=0.1,timeout=10)
                    chat.click_input()
                else:
                    friend_button.click_input()
                    chat=main_window.child_window(title=friend,control_type='Edit').wait(wait_for='visible',retry_interval=0.1,timeout=10)
                    chat.click_input()
                break
            else:
                pyautogui.press("pagedown")
                time.sleep(1)
        mouse.wheel_click(coords=(rectangle.right-5, rectangle.top+20))
        pyautogui.press('Home')
        return chat,main_window 
    
def open_dialog_window(friend:str,wechat_path:str=None,is_maximize:bool=True,search_pages:int=10): 
    '''
    friend:好友或群聊备注名称,需提供完整名称\n
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    search_pages:在会话列表中查询查找好友时滚动列表的次数,默认为10,一次可查询5-12人,当search_pages为0时,直接从顶部搜索栏法搜索好友信息打开聊天界面\n
    该函数用于打开某个好友的聊天窗口\n
    '''
    chat=None
    def is_in_searh_result(friend,search_result):
        listitem=search_result.children(control_type="ListItem")
        names=[item.window_text() for item in listitem]
        if names[0]==friend:
            return True
        else:
            return False
    if search_pages:
        chat,main_window=Tools.find_friend_in_MessageList(friend=friend,wechat_path=wechat_path,is_maximize=False,search_pages=search_pages)
        if is_maximize:
            main_window.maximize()
        if chat:
            return chat,main_window
        else:  
            Toolbar=main_window.child_window(**Main_window.Toolbar)
            chat_button=Toolbar.children(control_type="Button",title='聊天')[0]
            chat_button.click_input()
            time.sleep(1)
            search=main_window.child_window(**Main_window.Search).wait(wait_for='visible',retry_interval=0.1,timeout=10)
            search.click_input()
            search.type_keys(friend,with_spaces=True)
            time.sleep(2)
            search_result=main_window.child_window(**Main_window.SearchResult)
            if is_in_searh_result(friend=friend,search_result=search_result):
                pyautogui.hotkey('enter')
                chat=main_window.child_window(title=friend,control_type='Edit').wait(wait_for='visible',retry_interval=0.1,timeout=10)
                return chat,main_window #同时返回该好友的聊天窗口与主界面！若只需要其中一个需要使用元祖索引获取。
            else:
                main_window.close()
                raise NoSuchFriendError(f"好友或群聊备注有误！查无此人！")
    else: 
        main_window=None
        
        result=Tools.judge_wechat_state()
        if result=='主界面可见':
            wechat=Application(backend='uia').connect(**Main_window.MainWindow)
            main_window=wechat.window(**Main_window.MainWindow)
            Tools.move_window_to_center()
            if is_maximize:
                main_window.maximize()
        else:
            main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
        if is_maximize:
            main_window.maximize()
        current_chat=main_window.child_window(**Main_window.CurrentChatWindow)
        if current_chat.exists() and friend in current_chat.window_text():
            chat=current_chat
            chat.click_input()
            return chat,main_window
        else:
            Toolbar=main_window.child_window(**Main_window.Toolbar)
            chat_button=Toolbar.children(control_type="Button",title='聊天')[0]
            chat_button.click_input()
            time.sleep(1)
            search=main_window.child_window(**Main_window.Search).wait(wait_for='visible',retry_interval=0.1,timeout=10)
            search.click_input()
            search.type_keys(friend,with_spaces=True)
            time.sleep(2)
            search_result=main_window.child_window(**Main_window.SearchResult)
            if is_in_searh_result(friend=friend,search_result=search_result):
                pyautogui.hotkey('enter')
                chat=main_window.child_window(title=friend,control_type='Edit').wait(wait_for='visible',retry_interval=0.1,timeout=10)
                return chat,main_window #同时返回该好友的聊天窗口与主界面！若只需要其中一个需要使用元祖索引获取。
            else:
                main_window.close()
                raise NoSuchFriendError(f"好友或群聊备注有误！查无此人！")

def open_wechat_settings(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=False):
    '''
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    close_wechat:任务结束后是否关闭微信,默认关闭\n
    该函数用于打开微信设置界面\n
    '''
    main_window=None
    
    result=Tools.judge_wechat_state()
    if result=='主界面可见':
        wechat=Application(backend='uia').connect(**Main_window.MainWindow)
        main_window=wechat.window(**Main_window.MainWindow)
        Tools.move_window_to_center()
        if is_maximize:
            main_window.maximize()
    else:
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    Toolbar=main_window.child_window(**Main_window.Toolbar)
    setting=Toolbar.children(control_type='Pane',title='')[3].children(control_type='Button',title="设置及其他")[0]
    setting.click_input()
    settings_menu=main_window.child_window(**Main_window.SettingsMenu)
    settings_button=settings_menu.child_window(**Main_window.SettingsButton)
    settings_button.click_input() 
    time.sleep(2)
    desktop=Desktop(**Independent_window.Desktop)
    setting_window=desktop.window(**Independent_window.SettingWindow)
    main_window.close()
    return setting_window

def open_wechat_moments(wechat_path:str=None,is_maximize:bool=True):
    '''
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开微信朋友圈
    '''
    main_window=None
    
    result=Tools.judge_wechat_state()
    if result=='主界面可见':
        wechat=Application(backend='uia').connect(**Main_window.MainWindow)
        main_window=wechat.window(**Main_window.MainWindow)
        Tools.move_window_to_center()
        if is_maximize:
            main_window.maximize()
    else:
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    Toolbar=main_window.child_window(**Main_window.Toolbar)
    moments_button=Toolbar.children(control_type="Button",title='朋友圈')[0]
    moments_button.click_input()
    desktop=Desktop(**Independent_window.Desktop)
    moments_window=desktop.window(**Independent_window.MomentsWindow)
    main_window.close()
    return moments_window
   
def open_wechat_miniprogram(program_name:str,load_delay:int=3,wechat_path:str=None,is_maximize:bool=True):
    '''
    program_name:小程序名称\n
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开微信小程序
    '''
    main_window=None
    
    result=Tools.judge_wechat_state()
    if result=='主界面可见':
        wechat=Application(backend='uia').connect(**Main_window.MainWindow)
        main_window=wechat.window(**Main_window.MainWindow)
        Tools.move_window_to_center()
        if is_maximize:
            main_window.maximize()
    else:
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    Toolbar=main_window.child_window(**Main_window.Toolbar)
    program_button=Toolbar.child_window(**ToolBar.Miniprogram_pane)
    program_button.click_input()
    desktop=Desktop(**Independent_window.Desktop)
    program_window=desktop.window(**Independent_window.MiniProgramWindow)
    main_window.close()
    time.sleep(load_delay)
    search=program_window.child_window(control_type="Pane",title="",found_index=1).child_window(title="",control_type="Tab").children(title="",control_type="Pane")[1]
    search.click_input()
    search.type_keys(program_name,with_spaces=True)
    pyautogui.press("enter")
    time.sleep(load_delay)
    search_result=program_window.child_window(control_type="Document",class_name="Chrome_RenderWidgetHostHWND")
    program_button=search_result.child_window(control_type="ListItem",found_index=4)
    program_button.click_input()
    main=search_result.child_window(control_type="Button",title_re=program_name,found_index=0,framework_id="Chrome")
    time.sleep(load_delay)
    main.click_input()
    time.sleep(load_delay)
    program_window=desktop.window(title=program_name,framework_id="Win32",control_type="Pane",class_name="Chrome_WidgetWin_0")
    return program_window

def open_wechat_official_account(official_acount_name:str,load_delay:int=3,wechat_path:str=None,is_maximize:bool=True):
    '''
    official_account__name:公众号名称\n
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开公众号
    '''
    main_window=None
    
    result=Tools.judge_wechat_state()
    if result=='主界面可见':
        wechat=Application(backend='uia').connect(**Main_window.MainWindow)
        main_window=wechat.window(**Main_window.MainWindow)
        Tools.move_window_to_center()
        if is_maximize:
            main_window.maximize()
    else:
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    Toolbar=main_window.child_window(**Main_window.Toolbar)
    program_button=Toolbar.child_window(**ToolBar.Miniprogram_pane)
    program_button.click_input()
    desktop=Desktop(**Independent_window.Desktop)
    program_window=desktop.window(**Independent_window.MiniProgramWindow)
    main_window.close()
    time.sleep(load_delay)
    search=program_window.child_window(control_type="Pane",title="",found_index=1).child_window(title="",control_type="Tab").children(title="",control_type="Pane")[1]
    search.click_input()
    search.type_keys(official_acount_name,with_spaces=True)
    pyautogui.press("enter")
    time.sleep(load_delay)
    search_result=program_window.child_window(control_type="Document",class_name="Chrome_RenderWidgetHostHWND")
    official_acount_button=search_result.child_window(control_type="ListItem",found_index=3)
    official_acount_button.click_input()
    try:
        result=search_result.child_window(control_type="Button",found_index=1,framework_id="Chrome")
        time.sleep(2)
        result.click_input()
        time.sleep(2)
    except ElementNotFoundError:
        print("查无此公众号！")

def open_contacts_settings(wechat_path:str=None,is_maximize:bool=True,close_wechat:bool=True):
    '''
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    close_wechat:任务结束后是否关闭微信,默认关闭\n
    该函数用于打开通讯录设置界面
    '''
    desktop=Desktop(**Independent_window.Desktop)
    main_window=None
    
    result=Tools.judge_wechat_state()
    if result=='主界面可见':
        wechat=Application(backend='uia').connect(**Main_window.MainWindow)
        main_window=wechat.window(**Main_window.MainWindow)
        Tools.move_window_to_center()
        if is_maximize:
            main_window.maximize()
    else:
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    toolbar=main_window.child_window(control_type='ToolBar',title='导航')
    contacts=toolbar.child_window(**ToolBar.Contacts)
    contacts.set_focus()
    contacts.click_input()
    ContactsLists=main_window.child_window(title='联系人',control_type='List')
    rec=ContactsLists.rectangle()
    mouse.click(coords=(rec.right-5,rec.top))
    pyautogui.press('Home')
    pyautogui.press('pageup')
    contacts_settings=main_window.child_window(**Main_window.ContactsManage)#通讯录管理窗口按钮 
    contacts_settings.set_focus()
    contacts_settings.click_input()
    contacts_settings_window=desktop.window(**Independent_window.ContactManagerWindow)
    if close_wechat:
        main_window.close()
    return contacts_settings_window,main_window

def open_contacts(wechat_path:str=None,is_maximize:bool=True):
    '''
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开通讯录列表\n
    '''
    main_window=None
    
    result=Tools.judge_wechat_state()
    if result=='主界面可见':
        wechat=Application(backend='uia').connect(**Main_window.MainWindow)
        main_window=wechat.window(**Main_window.MainWindow)
        Tools.move_window_to_center()
        if is_maximize:
            main_window.maximize()
    else:
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    toolbar=main_window.child_window(**Main_window.Toolbar)
    contacts=toolbar.child_window(**ToolBar.Contacts)
    contacts.set_focus()
    contacts.click_input()
    ContactsLists=main_window.child_window(**Main_window.ContactsList)
    rec=ContactsLists.rectangle()
    mouse.click(coords=(rec.right-5,rec.top))
    pyautogui.press('Home')
    pyautogui.press('pageup')
    return main_window

def open_friend_settings(friend:str,wechat_path:str=None,is_maximize:bool=True):
    '''
    friend:好友备注名称\n
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开好友的设置界面\n
    '''
    main_window=Tools.open_dialog_window(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize)[1]
    ChatMessage=main_window.child_window(title="聊天信息",control_type="Button")
    ChatMessage.click_input()
    friend_settings_window=main_window.child_window(**Main_window.FriendSettingsWindow)
    return friend_settings_window,main_window

def open_friend_settings_menu(friend:str,wechat_path:str=None,is_maximize:bool=True):
    '''
    friend:好友备注名称\n
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开好友的设置菜单\n
    '''
    friend_settings_window,main_window=Tools.open_friend_settings(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize)
    friend_button=friend_settings_window.child_window(title=friend,control_type="Button",found_index=0)
    friend_button.click_input()
    profile_window=friend_settings_window.child_window(class_name="ContactProfileWnd",control_type="Pane",framework_id='Win32')
    more_button=profile_window.child_window(title='更多',control_type='Button')
    more_button.click_input()
    friend_menu=profile_window.child_window(control_type="Menu",title="",class_name='CMenuWnd',framework_id='Win32')
    return friend_menu,main_window

def open_channel(wechat_path:str=None,is_maximize:bool=True):
    '''
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开视频号\n
    '''
    main_window=None
    
    result=Tools.judge_wechat_state()
    if result=='主界面可见':
        wechat=Application(backend='uia').connect(**Main_window.MainWindow)
        main_window=wechat.window(**Main_window.MainWindow)
        Tools.move_window_to_center()
        if is_maximize:
            main_window.maximize()
    else:
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    Toolbar=main_window.child_window(**Main_window.Toolbar)
    channel_button=Toolbar.child_window(**ToolBar.Channel)
    channel_button.click_input()
    desktop=Desktop(**Independent_window.Desktop)
    channel_window=desktop.window(**Independent_window.ChannelWindow)
    return channel_window

def open_top_stories(wechat_path:str=None,is_maximize:bool=True):
    '''
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开看一看
    '''
    main_window=None
    
    result=Tools.judge_wechat_state()
    if result=='主界面可见':
        wechat=Application(backend='uia').connect(**Main_window.MainWindow)
        main_window=wechat.window(**Main_window.MainWindow)
        Tools.move_window_to_center()
        if is_maximize:
            main_window.maximize()
    else:
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    Toolbar=main_window.child_window(**Main_window.Toolbar)
    top_stories_button=Toolbar.child_window(**ToolBar.Topstories)
    top_stories_button.click_input()
    desktop=Desktop(**Independent_window.Desktop)
    top_stories_window=desktop.window(**Independent_window.TopStoriesWindow)
    return top_stories_window

def open_collections(wechat_path:str=None,is_maximize:bool=True):
    '''
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开收藏
    '''
    main_window=None
    
    result=Tools.judge_wechat_state()
    if result=='主界面可见':
        wechat=Application(backend='uia').connect(**Main_window.MainWindow)
        main_window=wechat.window(**Main_window.MainWindow)
        Tools.move_window_to_center()
        if is_maximize:
            main_window.maximize()
    else:
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    Toolbar=main_window.child_window(**Main_window.Toolbar)
    collections_button=Toolbar.child_window(**ToolBar.Collections)
    collections_button.click_input()
    return main_window


def open_group_settings(group:str,wechat_path:str=None,is_maximize:bool=True):
    '''
    group:群聊备注名称\n
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开好友的设置界面
    '''
    main_window=Tools.open_dialog_window(friend=group,wechat_path=wechat_path,is_maximize=is_maximize)[1]
    ChatMessage=main_window.child_window(**Main_window.ChatMessage)
    ChatMessage.click_input()
    group_settings_window=main_window.child_window(**Main_window.GroupSettingsWindow)
    return group_settings_window,main_window


    
def open_chat_files(wechat_path:str=None,is_maximize:bool=True):
    '''
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开聊天界面
    '''
    main_window=None
    
    result=Tools.judge_wechat_state()
    if result=='主界面可见':
        wechat=Application(backend='uia').connect(**Main_window.MainWindow)
        main_window=wechat.window(**Main_window.MainWindow)
        Tools.move_window_to_center()
        if is_maximize:
            main_window.maximize()
    else:
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    Toolbar=main_window.child_window(**Main_window.Toolbar)
    moments_button=Toolbar.child_window(**ToolBar.ChatFiles)
    moments_button.click_input()
    desktop=Desktop(**Independent_window.Desktop)
    filelist_window=desktop.window(**Independent_window.ChatFilesWindow)
    main_window.close()
    return filelist_window
    
def open_friend_profile(friend:str,wechat_path:str=None,is_maximize:bool=True):
    '''
    friend:好友备注名称\n
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开好友的个人简介界面
    '''
    friend_settings_window,main_window=Tools.open_friend_settings(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize)
    friend_button=friend_settings_window.child_window(title=friend,control_type="Button",found_index=0)
    friend_button.click_input()
    profile_window=friend_settings_window.child_window(class_name="ContactProfileWnd",control_type="Pane",framework_id='Win32')
    return profile_window,main_window

def open_search(wechat_path:str=None,is_maximize:bool=True):
    '''
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开搜一搜
    '''
    main_window=None
    
    result=Tools.judge_wechat_state()
    if result=='主界面可见':
        wechat=Application(backend='uia').connect(**Main_window.MainWindow)
        main_window=wechat.window(**Main_window.MainWindow)
        Tools.move_window_to_center()
        if is_maximize:
            main_window.maximize()
    else:
        main_window=Tools.open_wechat(wechat_path=wechat_path,is_maximize=is_maximize)
    Toolbar=main_window.child_window(**Main_window.Toolbar)
    search_button=Toolbar.child_window(**ToolBar.Search)
    search_button.click_input()
    desktop=Desktop(**Independent_window.Desktop)
    search_window=desktop.window(**Independent_window.SearchWindow)
    main_window.close()
    return search_window

def find_wechat_path(copy_to_clipboard:bool=True):
    '''该方法用来查找正在运行的微信的路径'''
    wechat_path=None
    for process in psutil.process_iter(['name','exe']):
        if 'WeChat.exe' in process.info['name']:
            wechat_path=process.info['exe']
            break
    if wechat_path:
        if copy_to_clipboard:
            Systemsettings.copy_text_to_windowsclipboard(wechat_path)
            print("已将微信程序路径复制到剪贴板")
        return wechat_path
    else:
        raise WeChatNotStartError(f'微信未启动,请启动后再调用此函数！')
    
def find_wechat_pid():
    '''该方法用来查找正在运行的微信进程的PID'''
    wechat_pids=[]
    for process in psutil.process_iter(['name','pid']):
        if 'WeChat.exe' in process.info['name']:
            wechat_pid=process.info['pid']
            wechat_pids.append(wechat_pid)
        if 'Wechat.exe' in process.info['name']:
            wechat_pids.append(wechat_pid)
    if wechat_pids[0]:
        return wechat_pid
    else:
        print('微信未启动,请启动后再调用此函数！')
        return None

def set_wechat_as_environ_path():
    '''该函数用来自动打开系统环境变量设置界面,将微信路径自动添加至其中'''
    subprocess.Popen(["SystemPropertiesAdvanced.exe"])
    os.environ.update({"__COMPAT_LAYER":"RUnAsInvoker"})#添加管理员权限
    time.sleep(3)
    systemwindow=win32gui.FindWindow(None,u'系统属性')
    if win32gui.IsWindow(systemwindow):#将系统变量窗口置于桌面最前端
        win32gui.ShowWindow(systemwindow,win32con.SW_SHOW)
        win32gui.SetForegroundWindow(systemwindow)     
    pyautogui.hotkey('alt','n',interval=0.5)#添加管理员权限后使用一系列快捷键来填写微信刻路径为环境变量
    pyautogui.hotkey('alt','n',interval=0.5)
    pyautogui.press('shift')
    pyautogui.typewrite('wechatpath')
    try:
        Tools.find_wechat_path()
        pyautogui.hotkey('Tab',interval=0.5)
        pyautogui.hotkey('ctrl','v')
        pyautogui.press('enter')
        pyautogui.press('enter')
        pyautogui.press('esc')
    except WeChatNotStartError:
        pyautogui.press('esc')
        pyautogui.hotkey('alt','f4')
        pyautogui.hotkey('alt','f4')
        raise WeChatNotStartError(f'微信未启动,请启动后再调用此函数！')
   
     

def judge_wechat_state():
    '''该函数用来判断微信运行状态并返回窗口句柄'''
    time.sleep(1.5)
    if Tools.is_wechat_running():
        window=win32gui.FindWindow('WeChatMainWndForPC','微信')
        if IsIconic(window):
            win32gui.SetForegroundWindow(window)
            return '主界面最小化'
        elif win32gui.IsWindowVisible(window):
            return '主界面可见'
        else:
            return '主界面不可见'
    else:
        return "微信未打开"

 
def move_window_to_center(Window:dict=Main_window.MainWindow,Window_handle:int=0):
    '''该函数用来将已打开的界面移动到屏幕中央,使用时需注意传入参数为窗口的字典形式\n
    需要包括class_name与title两个键值对,任意一个没有值可以使用None代替\n
    '''
    desktop=Desktop(**Independent_window.Desktop)
    class_name=Window['class_name']
    title=Window['title']
    if Window_handle==0:
        handle=win32gui.FindWindow(class_name,title)
    else:
        handle=Window_handle
    screen_width,screen_height=win32api.GetSystemMetrics(win32con.SM_CXSCREEN),win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    move_window=desktop.window(handle=handle)
    window_width,window_height=move_window.rectangle().width(),move_window.rectangle().height()
    new_left=(screen_width-window_width)//2
    new_top=(screen_height-window_height)//2
    if screen_width!=window_width:
        win32gui.SetForegroundWindow(handle)
        win32gui.MoveWindow(handle,new_left,new_top,window_width,window_height,True)

def open_chat_history(friend:str,wechat_path:str=None,is_maximize:bool=True):
    '''
    friend:好友备注
    wechat_path:微信的WeChat.exe文件地址,当微信未登录时,该函数使用此地址启动微信并点击登录完成打开微信界面。\n
    这里强烈建议将微信路径加入到windows环境变量中,因为该函数默认使用windows环境变量中的Wechat.exe路径启动微信,此时调用该函数无需任何参数\n
    若你没有设置微信的Wechat.exe地址为环境变量,那么你需要传入该文件地址作为参数否则会引发错误无法打开微信！\n
    is_maximize:微信界面是否全屏,默认全屏。\n
    该函数用于打开与好友的聊天历史
    '''
    friend_settings_window,main_window=Tools.open_friend_settings(friend=friend,wechat_path=wechat_path,is_maximize=is_maximize)
    chat_history_button=friend_settings_window.child_window(title='聊天记录',control_type='Button')
    chat_history_button.click_input()
    desktop=Desktop(**Independent_window.Desktop)
    chat_history_window=desktop.window(**Independent_window.ChatHistoryWindow)
    return chat_history_window,main_window

def match_duration(duration:str):
    if "s" in duration:
        try:
            duration=duration.replace('s','')
            duration=float(duration)
            return duration
        except ValueError:
            print("请输入合法的时间长度!")
            return "错误"
    elif 'min' in duration:
        try:
            duration=duration.replace('min','')
            duration=float(duration)*60
            return duration
        except ValueError:
            print("请输入合法的时间长度！")
            return "错误"
    elif 'h' in duration:
        try:
            duration=duration.replace('h','')
            duration=float(duration)*60*60
            return duration
        except ValueError:
            print("请输入合法的时间长度！")
            return "错误"
    else:
        raise TimeNotCorrectError('请输入合法的时间长度！') 