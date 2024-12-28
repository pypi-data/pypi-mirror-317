'''
Uielements
---------
PC微信中的各种Ui-Object'''
class Login_window():
    '''登录界面要用到的唯二的两个Ui:登录界面与进入微信按钮\n'''
    LoginWindow={'title':'微信','class_name':'WeChatLoginWndForPC','visible_only':False}
    LoginButton={'title':'进入微信','control_type':'Button'}

class ToolBar():
    '''主界面导航栏下的所有Ui'''
    Chat={'title':'聊天','control_type':'Button'}
    Contacts={'title':'通讯录','control_type':'Button'}
    Collections={'title':'收藏','control_type':'Button'}
    ChatFiles={'title':'聊天文件','control_type':'Button'}
    Moments={'title':'朋友圈','control_type':'Button'}
    Channel={'title':'视频号','control_type':'Button'}
    Topstories={'title':'看一看','control_type':'Button'}
    Search={'title':'搜一搜','control_type':'Button'}
    Miniprogram_pane={'title':'小程序面板','control_type':'Button'}
    SettingsAndOthers={'title':'设置及其他','control_type':'Button'}

    
class Main_window():
    '''主界面下所有的第一级Ui\n'''
    AddTalkMemberWindow={'title':'AddTalkMemberWnd','control_type':'Window','class_name':'AddTalkMemberWnd','framework_id':'Win32'}
    MainWindow={'title':'微信','class_name':'WeChatMainWndForPC'}
    Toolbar={'title':'导航','control_type':'ToolBar'}
    MessageList={'title':'会话','control_type':'List'}
    Search={'title':'搜索','control_type':'Edit'}
    SearchResult={'title_re':"@str:IDS_FAV_SEARCH_RESULT",'control_type':'List'}
    CerateGroupChatButton={'title':"发起群聊",'control_type':"Button"}
    ChatToolBar={'title':'','found_index':0,'control_type':'ToolBar'}
    ChatMessage={'title':'聊天信息','control_type':'Button'}
    CurrentChatWindow={'control_type':'Edit','found_index':1}
    CerateNewNote={'title':'新建笔记','control_type':'Button'}
    ProfileWindow={'class_name':"ContactProfileWnd",'control_type':'Pane','framework_id':'Win32'}
    MoreButton={'title':'更多','control_type':'Button'}
    FriendMenu={'control_type':'Menu','title':'','class_name':'CMenuWnd','framework_id':'Win32'}
    FriendSettingsWindow={'class_name':'SessionChatRoomDetailWnd','control_type':'Pane','framework_id':'Win32'}
    GroupSettingsWindow={'title':'SessionChatRoomDetailWnd','control_type':'Pane','framework_id':'Win32'}    
    SettingsMenu={'class_name':'SetMenuWnd','control_type':'Window'}
    SettingsButton={'title':'设置','control_type':'Button'}
    ContactsManage={'title':'通讯录管理','control_type':'Button'}
    ContactsList={'title':'联系人','control_type':'List'}
    AddNewFriendButon={'title':'添加朋友','control_type':'Button'}
    SearchNewFriendBar={'title':'微信号/手机号','control_type':'Edit'}
    SearchNewFriendResult={'title_re':'@str:IDS_FAV_SEARCH_RESULT','control_type':'List'}
    AddFriendRequestWindow={'title':'添加朋友请求','class_name':'WeUIDialog','control_type':'Window','framework_id':'Win32'}
    AddMemberWindow={'title':'AddMemberWnd','control_type':'Window','framework_id':'Win32'}
    DeleteMemberWindow={'title':'DeleteMemberWnd','control_type':'Window','framework_id':'Win32'}
    QuitGroupButton={'title':"退出",'control_type':'Button'}
    EmptyChatHistoryButon={'title':'清空','control_type':'Button'}
    Tickle={'title':'拍一拍','control_type':'MenuItem'}
    SelectContactWindow={'title':'','control_type':'Window','class_name':'SelectContactWnd','framework_id':'Win32'}
    SetTag={'title':'设置标签','framework_id':'Win32','class_name':'StandardConfirmDialog'}
    FriendChatList={'title':'消息','control_type':'List'}


class Independent_window():
    '''独立于微信主界面,将微信主界面关闭后仍能在桌面显示的Ui\n'''
    Desktop={'backend':'uia'}
    SettingWindow={'title':'设置','class_name':"SettingWnd",'control_type':'Window'}
    ContactManagerWindow={'title':'通讯录管理','class_name':'ContactManagerWindow'}
    MomentsWindow={'title':'朋友圈','control_type':"Window",'class_name':"SnsWnd"}
    ChatFilesWindow={'title':'聊天文件','control_type':'Window','class_name':'FileListMgrWnd'}
    MiniProgramWindow={'title':'微信','control_type':'Pane','class_name':'Chrome_WidgetWin_0'}
    SearchWindow={'title':'搜一搜','control_type':'Document'}
    ChannelWindow={'title':'视频号','control_type':'Document','framework_id':'Chrome'}
    ContactProfileWindow={'title':'微信','class_name':'ContactProfileWnd','framework_id':'Win32','control_type':'Pane'}
    TopStoriesWindow={'title':'看一看','control_type':'Document','framework_id':'Chrome'}
    ChatHistoryWindow={'control_type':'Window','class_name':'FileManagerWnd','framework_id':'Win32'}
    GroupAnnouncementWindow={'title':'群公告','framework_id':'Win32','class_name':'ChatRoomAnnouncementWnd'}
    NoteWindow={'title':'笔记','class_name':'FavNoteWnd','framework_id':"Win32"}
    OldIncomingCallWindow={'class_name':'VoipTrayWnd','title':'微信'}
    NewIncomingCallWindow={'class_name':'ILinkVoipTrayWnd','title':'微信'}
    OldVoiceCallWindow={'title':'微信','class_name':'AudioWnd'}
    NewVoiceCallWindow={'title':'微信','class_name':'ILinkAudioWnd'}
    OldVideoCallWindow={'title':'微信','class_name':'VoipWnd'}
    NewVideoCallWindow={'title':'微信','class_name':'ILinkVoipWnd'}