import pandas as pd
import numpy as np

df=pd.read_csv('static\data1.csv')
df.drop(df.columns[[0,1,2,3,7,9]],axis=1,inplace=True)
df=df.replace({'property':{'Urban':0,'Rural':1,'Semiurban':2}})
df=df.replace({'education':{'Graduate':0,'Not Graduate':1}})
df=df.replace({'employment':{'No':0,'Yes':1}})
df=df.replace({'status':{'Y':1,'N':0}})
#df=pd.get_dummies(df,drop_first=True)
df.dropna(inplace=True)
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
x=df.iloc[:,:6]
y=df.iloc[:,6]
x=sc.fit_transform(x)
from sklearn.linear_model import LogisticRegression
lr=LogisticRegression()
lr.fit(x,y)
prediction=lr.predict(x)
import pickle

pickle.dump(lr,open('bank_lr.pkl','wb'))

model=pickle.load(open('bank_lr.pkl','rb'))
print(model.predict([[4583,23680,1,1,0,1]]))

print(df.head())
