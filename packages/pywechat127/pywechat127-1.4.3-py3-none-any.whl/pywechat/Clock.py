
'''
定时模块schedule:可以按照当天指定时刻或一段时间后运行指定函数或方法\n
使用方法:\n
在指定的一段时间后执行\n
from pywechat127.clock import schedule\n
schedule(funcs=[func1,func2],parameters=[{func1的参数字典},{func2的参数字典},waitPeriods=['20s','20min']]).execute()
在指定的一段时刻执行\n
from pywechat127.clock import schedule\n
schedule(funcs=[func1,func2],parameters=[{func1的参数字典},{func2的参数字典},Time=['08:31:14','08:45']]).execute()
注:时刻可以精确到秒,若某个函数无需任何参数,那你在传入其对印的参数字典时,传入一个空字典即可\n
若给定的时间戳与当前时间戳之差为负数,定时任务将会立即执行\n
'''
import re
from  datetime import datetime
import asyncio
from pywechat.WechatTools import match_duration
class schedule:#创建定时任务
    '''
    funcs:所有需要定时执行的函数名列表,注意函数名的类型为函数\n
    不是类型为字符串的函数的名字!\n
    parameters:所有需要定时执行的函数的参数\n
    Times:各个函数定时执行的时间点,Times=['08:31','08:45:54']可精确到秒\n
    waitPeriod:各个函数在指定的一段时间执行的等待时长,waitPeriod=['20s','1h']分别在20s后和1h后执行两个函数、\n
    比如:有两个函数分别为,test1(num:int,string:str),test2(num:int,string:str)\n
    那么传入funcs和parameters时应为:funcs=[test1,test2]\n
    parameters=[{'num':2,'string':'test1'},{{'num':3,'string':'test2'}}]\n
    这个类通过构建协程池来创建定时任务\n
    '''
    def __init__(self,funcs:list,parameters:list[dict],Times:list[str]=[],waitPeriods:list[str]=[]):
        self.Times=Times#指定时间点，'08:31','08:45:54'可精确到秒
        self.waitPeriods=waitPeriods#指定时长，20s,1min,1h
        self.funcs=funcs#所有需要定时执行的函数名
        self.parameters=parameters##所有需要定时执行的函数的参数[{},{}]，

    def calculate_time_difference(self,target_time_string):
        colons=re.findall(r':',target_time_string)
        current_time = datetime.now()
        target_date = current_time.date()  # 获取当前日期
        if len(colons)==2:
            target_time_format="%H:%M:%S"
        elif len(colons)==1:
            target_time_format="%H:%M"
        else:
            raise ValueError('输入的时间戳有误!请重新输入!')
        target_time = datetime.combine(target_date, datetime.strptime(target_time_string, target_time_format).time())
        # 计算时间差
        time_difference = target_time - current_time
        hours_difference = time_difference.seconds // 3600  # 整除3600得到小时数
        minutes_remainder = time_difference.seconds % 3600  # 求余得到剩余的秒数，再转换为分钟
        minutes_difference = minutes_remainder // 60  # 整除60得到分钟数
        seconds_difference = minutes_remainder % 60  # 再次求余得到秒数
        print(f"时间差：{hours_difference}小时 {minutes_difference}分钟 {seconds_difference}秒")
        time_difference=time_difference.total_seconds()
        return  time_difference
    
    async def async_task(self,func,parameter,Time:str=None,waitPeriod:str=None):
        if Time:
            print(f"函数{func.__name__}将会在{Time}时执行")
            await asyncio.sleep(self.calculate_time_difference(Time))
            result=func(**parameter)
            return result
        if waitPeriod:
            print(f"函数{func.__name__}将会在{waitPeriod}后执行")
            waitPeriod=match_duration(waitPeriod)
            await asyncio.sleep(waitPeriod)
            result=func(**parameter)
            return result
    async def main(self):
        #构建协程池实现异步定时任务
        tasks=[]
        if self.waitPeriods:
            for func,parameter,waitPeriod in zip(self.funcs,self.parameters,self.waitPeriods):
                tasks.append(self.async_task(func,parameter,waitPeriod=waitPeriod))
            results=await asyncio.gather(*tasks)
            return results
        if self.Times:
            for func,parameter,time in zip(self.funcs,self.parameters,self.Times):
                tasks.append(self.async_task(func,parameter,Time=time))
            results=await asyncio.gather(*tasks)
            return results
    def execute(self):
        #运行所有任务
        results=asyncio.run(self.main())
        return results