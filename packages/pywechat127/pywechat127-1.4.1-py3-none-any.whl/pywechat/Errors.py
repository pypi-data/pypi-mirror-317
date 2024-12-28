'''各种可能产生的错误'''
class PathNotFoundError(Exception):
    pass
class WeChatNotStartError(Exception):
    pass
class NetWorkNotConnectError(Exception):
    pass
class ScanCodeToLogInError(Exception):
    pass
class TimeNotCorrectError(Exception):
    pass
class HaveBeenPinnedError(Exception):
    pass
class HaveBeenUnpinnedError(Exception):
    pass
class NoSuchFriendError(Exception):
    pass
class HaveBeenMutedError(Exception):
    pass
class HaveBeenStickiedError(Exception):
    pass
class HaveBeenUnmutedError(Exception):
    pass
class HaveBeenUnstickiedError(Exception):
    pass
class HaveBeenStaredError(Exception):
    pass
class HaveBeenUnstaredError(Exception):
    pass
class HaveBeenInBlackListError(Exception):
    pass
class HaveBeenOutofBlackListError(Exception):
    pass
class HaveBeenSetChatonlyError(Exception):
    pass
class HaveBeenSetUnseentohimError(Exception):
    pass
class HaveBeenSetDontseehimError(Exception):
    pass
class PrivacytNotCorrectError(Exception):
    pass
class NoWechat_number_or_Phone_numberError(Exception):
    pass
class EmptyFileError(Exception):
    pass
class EmptyFolderError(Exception):
    pass
class NotFileError(Exception):
    pass
class NotFolderError(Exception):
    pass
class CantCreateGroupError(Exception):
    pass
class NoPermissionError(Exception):
    pass
class SameNameError(Exception):
    pass
class AlreadyOpenError(Exception):
    pass
class AlreadyCloseError(Exception):
    pass
class AlreadyInContactsError(Exception):
    pass
class EmptyNoteError(Exception):
    pass
class NoChatHistoryError(Exception):
    pass
class HaveBeenSetError(Exception):
    pass

