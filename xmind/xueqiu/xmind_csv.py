# -*- coding: utf-8 -*-
# @Time    : 2020-07-10 14:15
# @Author  : feier
# @File    : xmind_csv_3.py

from xmindparser import xmind_to_dict
import csv
import logging
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


class XmindToCsv():

    def my_log(self):
        '''创建对象的类方法'''
        # 创建日志搜集器
        mylog = logging.getLogger('mylog')
        mylog.setLevel('DEBUG')
        # 创建日志输出渠道
        sh = logging.StreamHandler()
        sh.setLevel('INFO')
        # 按时间进行轮转的收集器
        file_name = datetime.now().strftime("%Y-%m-%d") + '.log'
        fh = TimedRotatingFileHandler(file_name, encoding='utf8', when='h', interval=24, backupCount=3)
        fh.setLevel('DEBUG')
        # 将日志输出渠道和日志收集器进行绑定
        mylog.addHandler(fh)
        mylog.addHandler(sh)
        # 设置日志输出格式
        fot = '%(asctime)s-[%(filename)s-->line:%(lineno)d]-%(message)s'
        formatter = logging.Formatter(fot)
        # 将日志输出格式与输出渠道进行绑定
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)
        return mylog

    def topics_num(self, value):
        """获取xmind标题个数"""
        try:
            return len(value['topics'])
        except KeyError:
            return 0

    def xmind_title(self, value):
        """获取xmind标题内容"""
        return value['title']

    def write_csv(self, filename, case):
        '''写入csv文件，case为列表'''
        headers = ["模块", "测试标题", "测试步骤", "预期结果"]

        with open(filename, 'w')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(case)
        print("success!")

    def read_xmind(self, filename):
        '''读取xmind内容，返回case列表'''

        # xmind内容
        xmind_content = xmind_to_dict(filename)[0]['topic']
        # 模块内容
        module_name = self.xmind_title(xmind_content)
        # 二级模块的数量
        module_num2 = self.topics_num(xmind_content)
        # 用例列表
        case_list = []

        for i in range(module_num2):
            case_num = self.topics_num(xmind_content['topics'][i])
            if case_num == 0:
                print(f'第{i + 1}个功能模块下，测试的功能点数量为0，请确认用例是否编写完成')
                self.my_log().debug(f'第{i + 1}个功能模块下，测试的功能点数量为0，请确认用例是否编写完成')
            else:
                tag = self.xmind_title(xmind_content['topics'][i])
                case_point_num = self.topics_num(xmind_content['topics'][i])
                for j in range(case_point_num):
                    case = []
                    if case_point_num == 0:
                        print(f'第{j + 1}个功能模块下，测试的功能点数量为0，请确认用例是否编写完成')
                    else:
                        case_point = self.xmind_title(xmind_content['topics'][i]['topics'][j])
                        case_step = self.xmind_title(xmind_content['topics'][i]['topics'][j]['topics'][0])
                        expected_result = self.xmind_title(xmind_content['topics'][i]['topics'][j]['topics'][0]['topics'][0])
                        case_title = "【" + tag + "】" + case_point
                        case.append(module_name)
                        case.append(case_title)
                        case.append(case_step)
                        case.append(expected_result)
                        case_list.append(case)
        return case_list

    def main(self, csv_file, xmind_file):
        case_list = self.read_xmind(xmind_file)
        self.write_csv(csv_file, case_list)

if __name__ == '__main__':
    xmind_file = "/Users/Administrator/Desktop/实战/4 测试流程与实战/02 测试流程建设实战之测试用例管理/雪球自选设置.xmind"
    csv_file = "/Users/Administrator/Desktop/实战/4 测试流程与实战/02 测试流程建设实战之测试用例管理/xueqiu.csv"
    XmindToCsv().main(csv_file, xmind_file)