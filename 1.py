# coding=gbk
import pandas as pd
import datetime   #�����������ڲ�İ�
import orangecontrib.associate.fpgrowth as oaf  #���й�����������İ�

def dataInterval(data1,data2):
    d1 = datetime.datetime.strptime(data1, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(data2, '%Y-%m-%d')
    delta = d1 - d2
    return delta.days

def getInterval(arrLike):  #�����������ڼ�������ĵ��õĺ���
    PublishedTime = arrLike['PublishedTime']
    ReceivedTime = arrLike['ReceivedTime']
#    print(PublishedTime.strip(),ReceivedTime.strip())
    days = dataInterval(PublishedTime.strip(),ReceivedTime.strip())  #ע��ȥ�����˿հ�
    return days

def dealRules(rules):
    returnRules = []
    for i in rules:
        temStr = '';
        for j in i[0]:   #�����һ��frozenset
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
        for j in i[0]:   #�����һ��frozenset
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

def ResultDFToSave(rules,itemsets):   #����Qrange3�����������ɵĹ���õ������ض��ڵ�DataFrame���ݽṹ�ĺ���
    returnRules = []
    for i in rules:
        temList = []
        temStr = '';
        list1 = [];
        for j in i[0]:   #�����һ��frozenset
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
    return pd.DataFrame(returnRules,columns=('����','�������Ŀ','���Ŷ�','���Ƕ�','����','������','���ö�','ȫ���Ŷ�'))
    

if __name__ == '__main__':    
    df = pd.read_csv('E:\winemag-data_first150k.csv',delimiter=',')

    listToAnalysis = []
    listToStore = []
    for i in range(df.iloc[:,0].size):             #df.iloc[:,0].size
        #����Country��λ
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
   #��ʼ���й�������     
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
    result = list(oaf.rules_stats(rules, itemsets, len(listToAnalysis)))   #������������ı���rules����rules�����ˣ�
    printResult = dealResult(result)
    
#################################################���潫��������excel��ʽ���ļ�    
    dfToSave = ResultDFToSave(result,itemsets)
    saveRegularName = str(supportRate)+'֧�ֶ�_'+str(confidenceRate)+'���Ŷ�_������'+str(regularNum)+'������'+'.csv'
    dfToSave.to_csv('E:\\'+saveRegularName,index=None,encoding="utf_8")


