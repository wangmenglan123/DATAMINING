import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.font_manager import FontProperties
from sklearn.ensemble import RandomForestRegressor
import numpy as np
font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14)
df_train = pd.read_csv('F:\data\chicago-building-violations\\building-violations.csv',delimiter=',')
x_numeric = df_train.columns[df_train.dtypes !='object']
print(df_train['PROPERTY GROUP'].head(33))
print(x_numeric)
def visual(i,data):
    plt.hist(data, bins=4)
    plt.xlabel(i)
    plt.ylabel('value')
    plt.title(u'ֱ��ͼ', FontProperties=font)
    plt.show()
    stats.probplot(data, dist="norm", plot=plt)
    plt.xlabel(i)
    plt.title(u'qqͼ', FontProperties=font)
    plt.show()
    plt.boxplot(data)
    plt.xlabel(i)
    plt.title(u'��ͼ', FontProperties=font)
    plt.show()
for i in df_train.columns[1:-1]:
    if i in x_numeric:
        print(i)
        print("max:",df_train[i].describe()['max'])
        print("min:", df_train[i].describe()['min'])
        print("mean:", df_train[i].describe()['mean'])
        print("medium:", df_train[i].describe()['50%'])
        print("25%:", df_train[i].describe()['25%'])
        print("75%:", df_train[i].describe()['75%'])
        print("miss data:",len(df_train[i])-df_train[i].describe()['count'])
        visual(i,df_train[i])
    else:
        print(df_train[i].value_counts())
df_train_new=[]
df_train1=df_train.dropna(axis=0,subset = [ "PROPERTY GROUP"])
df_train_new.append(df_train1)
dict={}
key=0
ff_name=["��ȱʧ�����޳�","�����Ƶ��ֵ���ȱʧֵ","ͨ�����ݶ���֮������������ȱʧֵ","ͨ�����Ե���ع�ϵ���ȱʧֵ"]
for i in df_train.columns[1:-1]:
    dict[i]=df_train[i].value_counts().index[0]
df_train2=df_train.fillna(dict)
df_train_new.append(df_train2)
def set_missing(df):
    # �����е���ֵ������ȡ��������Random Forest Regressor��
    _df = df[['PROPERTY GROUP', 'STREET NUMBER']]

    # �˿ͷֳ���֪�����δ֪����������

    known= _df[_df['PROPERTY GROUP'].notnull()].as_matrix()

    unknown= _df[_df['PROPERTY GROUP'].isnull()].as_matrix()

    # y��Ŀ������

    y = known[:, 0]

    # X����������ֵ

    X = known[:, 1::]

    # fit��RandomForestRegressor֮��

    rfr = RandomForestRegressor(random_state=0, n_estimators=2000, n_jobs=-1)

    rfr.fit(X, y)

    # �õõ���ģ�ͽ���δ֪������Ԥ��

    predicted = rfr.predict(unknown[:, 1:])

    #     print predictedAges

    # �õõ���Ԥ�����ԭȱʧ����

    df.loc[(_df['PROPERTY GROUP'].isnull()), 'PROPERTY GROUP'] = predicted

    return df, rfr
df_train3=set_missing(df_train)
df_train_new.append(df_train3)
for i in df_train_new:
print(ff_name[key])
visual('PROPERTY GROUP',i['PROPERTY GROUP'])
Key+=1
