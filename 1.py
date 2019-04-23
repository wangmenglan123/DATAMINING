# coding=gbk
import pandas as pd
import datetime   #用来计算日期差的包
import orangecontrib.associate.fpgrowth as oaf  #进行关联规则分析的包

def dataInterval(data1,data2):
    d1 = datetime.datetime.strptime(data1, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(data2, '%Y-%m-%d')
    delta = d1 - d2
    return delta.days

def getInterval(arrLike):  #用来计算日期间隔天数的调用的函数
    PublishedTime = arrLike['PublishedTime']
    ReceivedTime = arrLike['ReceivedTime']
#    print(PublishedTime.strip(),ReceivedTime.strip())
    days = dataInterval(PublishedTime.strip(),ReceivedTime.strip())  #注意去掉两端空白
    return days

def dealRules(rules):
    returnRules = []
    for i in rules:
        temStr = '';
        for j in i[0]:   #处理第一个frozenset
            temStr = temStr+j+'&'
        temStr = temStr[:-1]
        temStr = temStr + ' ==> '
        for j in i[1]:
            temStr = temStr+j+'&'
        temStr = temStr[:-1]
        temStr = temStr + ';' +'\t'+str(i[2])+ ';' +'\t'+str(i[3])
#        print(temStr)
        returnRules.append(temStr)
    return returnRules

def dealResult(rules):
    returnRules = []
    for i in rules:
        temStr = '';
        for j in i[0]:   #处理第一个frozenset
            temStr = temStr+j+'&'
        temStr = temStr[:-1]
        temStr = temStr + ' ==> '
        for j in i[1]:
            temStr = temStr+j+'&'
        temStr = temStr[:-1]
        temStr = temStr + ';' +'\t'+str(i[2])+ ';' +'\t'+str(i[3])+ ';' +'\t'+str(i[4])+ ';' +'\t'+str(i[5])+ ';' +'\t'+str(i[6])+ ';' +'\t'+str(i[7])
#        print(temStr)
        returnRules.append(temStr)
    return returnRules

def ResultDFToSave(rules,itemsets):   #根据Qrange3关联分析生成的规则得到并返回对于的DataFrame数据结构的函数
    returnRules = []
    for i in rules:
        temList = []
        temStr = '';
        list1 = [];
        for j in i[0]:   #处理第一个frozenset
            temStr = temStr + str(j) + '&'
            list1.append(str(j));
        temStr = temStr[:-1]
        temStr = temStr + ' ==> '
        for j in i[1]:
            temStr = temStr + str(j) + '&'
            list1.append(str(j));
        temStr = temStr[:-1]
        temList.append(temStr); temList.append(i[2]); temList.append(i[3]); temList.append(i[4])
        temList.append(i[5]); temList.append(i[6]); temList.append(i[7])
        temList.append(min(itemsets[frozenset(list1)]/itemsets[frozenset(i[0])],itemsets[frozenset(list1)]/itemsets[frozenset(i[1])] ))
        returnRules.append(temList)
    return pd.DataFrame(returnRules,columns=('规则','项集出现数目','置信度','覆盖度','力度','提升度','利用度','全置信度'))
    

if __name__ == '__main__':    
    df = pd.read_csv('E:\winemag-data_first150k.csv',delimiter=',')

    listToAnalysis = []
    listToStore = []
    for i in range(df.iloc[:,0].size):             #df.iloc[:,0].size
        #处理Country段位
        s = df.iloc[i]['country']
        s = 'country_'+str(s)
        listToStore.append(s)
        s = df.iloc[i]['points']
        if s <= 85:
            s = 'points_'+'85'
        elif s <= 90 and s > 85:
            s = 'points_'+'85_90'
        elif s<= 95 and s>90:
            s = 'points_'+'90_95'
        elif s<= 100 and s>95:
            s = 'points_'+'95_100'
        #s = 'points_'+str(s)
        listToStore.append(s)
        s = df.iloc[i]['price']
        if s < 100:
            s = 'price_'+'100'
        elif s >= 100 and s < 300:
            s = 'price_'+'100_300'
        elif s >= 300 and s < 600:
            s = 'price_'+'300_600'
        elif s >= 600 and s < 1000:
            s = 'price_'+'600_1000'
        elif s>=1000:
            s = 'price_'+'1000'
        
        #s = 'price_'+str(s)
        listToStore.append(s)
        #print(listToStore)
        listToAnalysis.append(listToStore.copy())
        listToStore.clear()
   #开始进行关联分析     
    supportRate = 0.02
    confidenceRate = 0.5
    itemsets = dict(oaf.frequent_itemsets(listToAnalysis, supportRate))
    for itemset in itemsets.items():
        print(itemset)
    #print(itemsets[frozenset({'country_Chile'})])
    rules = oaf.association_rules(itemsets, confidenceRate)
    rules = list(rules)
    regularNum = len(rules)
    printRules = dealRules(rules)
    result = list(oaf.rules_stats(rules, itemsets, len(listToAnalysis)))   #下面这个函数改变了rules，把rules用完了！
    printResult = dealResult(result)
    
#################################################下面将结果保存成excel格式的文件    
    dfToSave = ResultDFToSave(result,itemsets)
    saveRegularName = str(supportRate)+'支持度_'+str(confidenceRate)+'置信度_产生了'+str(regularNum)+'条规则'+'.csv'
    dfToSave.to_csv('E:\\'+saveRegularName,index=None,encoding="utf_8")


