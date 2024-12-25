import re
from .b64save import json2dict, dict2json
import os
import sys
from . import time_htht as htt
import time

prodir = os.path.dirname(os.path.abspath(__file__))


def dtime2stime(dtime):
    dtime = str(dtime)
    dtime = re.sub('(^0\.0*\d{3}).*', r'\1', dtime)
    dtime = re.sub(r'(.*[^0].*\.\d{2})\d+', r'\1', dtime)
    dtime = re.sub(r'(\..*[^0])0+$', r'\1', dtime)
    stime = re.sub(r'\.0+$', '.0', dtime)
    return stime


def project(*args, **kw):
    p = PROJECT(*args, **kw)
    return p.say, p


class PROJECT():

    """Docstring for project. """

    def __init__(self, inputjson, steps='初始化|输出', pname='tctb'):
        """TODO: to be defined. """
        self.pname = pname
        self.status = '成功'
        self.error = ''
        self.outputs = []
        self.time0 = time.time()
        self.outdir = '/tmp/'
        self.time00 = self.time0

        if str(type(steps)) == str(type('-')):
            self.steps = re.split(r'\|', steps)
        else:
            self.steps = steps

        try:
            self.input = json2dict(inputjson)
        except Exception as e:
            self.pname = 'base'
            inputjson = prodir+'/'+self.pname+'/input.json'
            self.input = json2dict(inputjson)

        try:
            settingsjson = prodir+'/'+\
                    self.pname+'/settings.json'
            self.settings = json2dict(settingsjson)
        except Exception as e:
            self.settings = {'info':''}

        try:
            self.outdir = self.input['resultPath']
            self.pfile = self.input['primaryFile']
        except Exception as e:
            pass

        self.flow_file = self.input['resultFlowFile']
        self.result_file = self.input['resultJsonFile']
        self.log_file = self.input['resultLogFile']

        # 初始化flowjson
        self.flow_dict = json2dict(prodir+'/'+self.pname+'/flow.json')
        self.step_dict = {} 
        num = 0
        for sname in self.steps:
            num += 1
            tmp = json2dict(prodir+'/'+self.pname+'/step.json')
            tmp['stepName'] = sname
            tmp['stepNo'] = str(num)
            self.flow_dict['step'].append(tmp)
            self.step_dict[sname] = tmp
        dict2json(self.flow_dict, self.flow_file)
        self.flow('初始化')

        # 初始化resultjson
        self.result_dict = json2dict(prodir+'/'+self.pname+'/result.json')
        self.result_dict['productionTime'] = htt.time2str(time.time()+8*3600, 'yyyy/mm/dd HH:MM:SS CST')
        dict2json(self.result_dict, self.result_file)


    def flow(self, sname):
        if sname in self.step_dict:
            pass
        else:
            return

        if self.step_dict[sname]['status'] == 0:
            return


        for s in self.steps:
            if self.step_dict[s]['status'] == 0:
                continue
            stime = htt.time2str(time.time()+8*3600, 'yyyy/mm/dd HH:MM:SS CST')
            self.step_dict[s]['status'] = 0 
            self.step_dict[s]['log'] = s+'完成' 
            self.step_dict[s]['timeStamp'] = stime
            dict2json(self.flow_dict, self.flow_file)

            # 处理完成时间字符串
            dtime = str(time.time()-self.time0)
            dtime = re.sub('(^0\.0*\d{3}).*', r'\1', dtime)
            dtime = re.sub(r'(.*[^0].*\.\d{2})\d+', r'\1', dtime)
            dtime = re.sub(r'(\..*[^0])0+$', r'\1', dtime)
            dtime = re.sub(r'\.0+$', '.0', dtime)

            self.log(s+'完成, 耗时'+dtime+'秒')
            self.time0 = time.time()
            if s == sname:
                break

    def finish(self, info={}):
        if self.error == '':
            pass
        else:
            self.status = '失败'

        if self.status == '失败':
            self.result_dict['status'] = '1'
            self.result_dict['message'] = self.error
        if self.status == '成功':
            self.result_dict['status'] = '0'
            self.result_dict['message'] = '执行成功。'
            self.flow('输出')
        if self.status == '重做':
            self.result_dict['status'] = '9'
            self.result_dict['message'] = '需要重做。'+self.error
        dict2json(self.result_dict, self.result_file)
        return

    def result(self, outpath='', info={}):

        if outpath == '':
            if self.error == '':
                pass
            else:
                self.status = '失败'

            if self.status == '失败':
                self.result_dict['status'] = '1'
                self.result_dict['message'] = self.error
            if self.status == '成功':
                self.result_dict['status'] = '0'
                self.result_dict['message'] = '执行成功。'
                self.flow('输出')
            if self.status == '重做':
                self.result_dict['status'] = '9'
                self.result_dict['message'] = '需要重做。'+self.error
            dict2json(self.result_dict, self.result_file)
            self.log('运行完毕, 耗时'+\
                dtime2stime(time.time()-self.time00)+'秒')
            return

        self.flow('处理')
        product = json2dict(prodir+'/'+self.pname+'/product.json')

        if str(type(info)) == str(type('')):
            info1 = {}
            for tmp in re.split(r'\|', info):
                try:
                    tmp1 = re.search('(.+):(.+)', tmp)
                    info1[tmp1.group(1)] = tmp1.group(2)
                except Exception as e:
                    pass
            info = info1
    
        self.outputs.append(outpath)
        if re.search(r'^:', outpath):
            outpath = re.sub(r'^:'+self.outdir, '', outpath)
        if re.search(r'^\|', outpath):
            outpath = re.sub(r'^\|'+self.outdir, '', outpath)
        if re.search(r'-norootpath-', self.settings['info']):
            outpath = re.sub(r'^'+self.outdir, '', outpath)

        product['filePath'] = outpath
        for k in product.keys():
            if k in info:
                product[k] = info[k]
        self.result_dict['result'].append(product)
        dict2json(self.result_dict, self.result_file)

    def log(self, stmp):
        if stmp == '输出开始':
            self.flow('处理')

        if re.search(r'.*开始$', stmp):
            self.time0 = time.time()

        if re.search(r'.*完成$', stmp):
            stime = dtime2stime(time.time()-self.time0)
            stmp = stmp + ', 耗时'+stime+'秒'
            self.time0 = time.time()

        with open(self.log_file, 'a') as f:
            s = htt.time2str(time.time()+8*3600, 'yyyy/mm/dd HH:MM:SS CST: ')+stmp
            print(s, flush=True)
            f.write(s+'\n')

    def update(self):
        return

    def say(self, stmp='', info={}):
        if stmp == '更新结果状态' or\
                stmp == '' or stmp == 'update result':
            self.result()
            return

        if re.search(r'^错误:', stmp):
            print(stmp)
            self.error = stmp

        if re.search(r'^ERROR:', stmp):
            print(stmp)
            self.error = stmp

        if re.search(r'^error:', stmp):
            print(stmp)
            self.error = stmp

        if re.search(r'.+完成$', stmp):
            step = re.search(r'(.+)完成$', stmp).group(1)
            if step in self.step_dict:
                self.flow(step)
                return

        if re.search(r'^[p|o|r]?:', stmp):
            outfile = re.sub(r'^[p|o|r]?:', '', stmp)
            self.result(outfile, info)
            self.log('输出文件: '+outfile)
            return
 
        if re.search(r'^output:', stmp):
            outfile = re.sub(r'^output:', '', stmp)
            self.result(outfile, info)
            self.log('输出文件: '+outfile)
            return

        if re.search(r'^result:', stmp):
            outfile = re.sub(r'^result:', '', stmp)
            self.result(outfile, info)
            self.log('输出文件: '+outfile)
            return

        if re.search(r'^输出:', stmp):
            outfile = re.sub(r'^输出:', '', stmp)
            self.result(outfile, info)
            self.log('输出文件: '+outfile)
            return

        if stmp == 'INPUT' or\
                stmp == 'input' or\
                stmp == '显示输入:' or\
                stmp == '输入': 
            try:
                self.log('输入主文件: '+self.pfile)
            except Exception as e:
                pass
            try:
                self.log('输出根目录: '+self.outdir)
            except Exception as e:
                pass
            return

        self.log(stmp)
