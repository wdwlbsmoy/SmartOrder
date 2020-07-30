import requests,json
import traceback

def parseDictOrList(dict_or_list_Result,targetTag):
    '''
    遍历字典/列表中key对应的value值
    dictResult表示原始的json字典；targetTag表示要查找的key，层级之间用逗号隔开
    '''
    emptyValue = ''
    #如果入参是整数或字符串，如果是json结构，转换成字典后继续递归解析，如果是普通int或str直接返回
    if isinstance(dict_or_list_Result,(int,str)):
        #结构中包含json串，转换并获取值
        try:
            newDict = json.loads(dict_or_list_Result)
            return parseDictOrList(newDict,targetTag)
        except Exception:
            return dict_or_list_Result
    #如果是list结构，根据入参split的长度判断，如果是1直接返回，如果是多个值，继续递归解析
    if isinstance(dict_or_list_Result,list):
        try:
            targetList = targetTag.split('.')
            if len(targetList) == 1:
                return dict_or_list_Result[int(targetList[0])]
            else:
                return parseDictOrList(dict_or_list_Result[int(targetList[0])], '.'.join(targetList[1:]))
        except:
            traceback.print_exc()
            return emptyValue
    #字典结构递归解析
    targetList = targetTag.split('.')
    if len(targetList) == 1:
        return dict_or_list_Result[targetTag]
    else:
        if isinstance(dict_or_list_Result,dict) and (targetList[0] in dict_or_list_Result):
            return parseDictOrList(dict_or_list_Result[targetList[0]],'.'.join(targetList[1:]))
        return emptyValue

class udcTrack(object):
    #该类主要用于实现查询跟单结果、日志等，实现查询http://beta.udc.jd.com/结果
    baseUrl = 'http://beta.udc.jd.com/api/'
    interfaceType = {'下单平台':'type','跟单':'track','点击信息':'click','P/D参数':'desp',
                 '逆向分配明细':'backAlloc','逆向订单明细':'backSku','正向订单明细':'alloc',
                 'UNPL':'unpl','订单XML':'xml'}
    @classmethod
    def get_result(cls,checkName,checkValue,targetTag=None):
        #用于查询所有的结果信息，并以字典格式返回
        response = requests.get(cls.baseUrl+cls.interfaceType[checkName]+'?id=' + str(checkValue))
        try:
            result =  response.json()
            if targetTag is None:
                return result
            return parseDictOrList(result,targetTag)
        except Exception as err:
            traceback.print_exc(err)
            return {}  #解析失败返回空字典

if __name__ == '__main__':
    result = udcTrack.get_result('跟单','123669600127','CpsRelatedResult.sku.0.orderid')
    print(result)
