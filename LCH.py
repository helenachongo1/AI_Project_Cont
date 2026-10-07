import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Q1.1
#from sklearn import linear_model
train = pd.read_csv("C:/Users/Acer/Downloads/train.csv")
#To get summary of dataset
'''print(train.head())
print(train.info())
print(train.shape())
#To remove rows that have missing values for any of the variables
#print(train.dropna())
#•	Basic statistics of numerical columns (mean, median, mode)
print(train[["Age","Fare"]].mean())
print(train[["Age","Fare"]].median())
print(train[["Age","Fare"]].mode())

t=sns.countplot(x='Survived',data=train)
print(t)
t1=sns.countplot(x='Sex',hue='Survived',data=train)
print(t1)
t2=sns.countplot(x="Pclass",hue="Survived",data=train)
print(t2)
t3=sns.countplot(x="Embarked",hue="Survived",data=train)
print(t3)'''
#Q1.2
'''total=train.isnull().sum().sort_values(ascending=False)
per_1=train.isnull().sum()/train.isnull().count()*100
per_2=(round(per_1,1)).sort_values(ascending=False)
miss_value=pd.concat([total,per_2],axis=1,keys=['Total','%'])
print(miss_value.head(6))

data=train.copy()
#To know which columns contains null values
print(data.isnull().sum())
#to handle this situation,for age we can replace the null values by the correspondent mean
int(data['Age'].mean())
data['Age']=data['Age'].fillna(np.mean(data['Age']))
#For embarked, we can drop the rows or we can replace with the mode of the columns,
#since its an object column
data['Embarked'].fillna(data['Embarked'].mode()[0], inplace=True)
#For cabin, we can use mode of this column to replace the null values
data['Cabin'].fillna(data['Cabin'].mode()[0], inplace=True)
print(data.isnull().sum())'''
#Q1.3
'''print(train["Sex"].value_counts())
print(train["Embarked"].value_counts())
train.replace({
    "Sex":{"male":0,"female":1},
    "Embarked":{"S":0,"C":1,"Q":2}
    }, inplace=True)
print(train.head())

train['FamilySize']=train['SibSp']+ train['Parch']+1
train['isAlone']=(train['FamilySize']==1).astype(int)
b=[0,18,65,100]
labels=['child','adult','elderly']
s=train['AgeGroup']=pd.cut(train['Age'],bins=b,labels=labels)'''

'''#print(test.info())
#print(test.dropna())
print(test[["Age","Fare"]].mean())
print(test[["Age","Fare"]].median())
print(test[["Age","Fare"]].mode())'''

test = pd.read_csv("C:/Users/Acer/Downloads/test.csv")
#Part 3
'''X= train.drop(["PassengerId","Survived","Name","Ticket"],axis=1)
Y=train["Survived"]
from sklearn.model_selection import train_test_split as tts
x_train,x_test,y_train,y_test = tts(X,Y,test_size=0.25, random_state=42)
print(x_train.shape,x_test.shape,y_train.shape,y_test.shape)
from sklearn.linear_model import LogisticRegression
model=LogisticRegression()
model.fit(x_train,y_train)
print(LogisticRegression())
from sklearn.metrics import accuracy_score
x_train_prediction=model.predict(x_train)
print(x_train_prediction)
accurancy_train=accuracy_score(y_train,x_train_prediction)
print(accurancy_train)
x_test_prediction=model.predict(x_test)
print(x_test_prediction)
accurancy_test=accuracy_score(y_test,x_test_prediction)
print(accurancy_test)'''

'''import pickle
with open("model.pkl","wb") as f:
    pickle.dump(model,f)
    
with open("model.pkl","rb") as f:
    loaded_model=pickle.load(f)
    
loaded_model.predict([[3,0,22,1,0,7,0]])
print(X)'''

#Part 2
'''survived = 'survived'
not_survived = 'not survived'
fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(10, 4))
women = train[train['Sex']=='female']
men = train[train['Sex']=='male']
ax = sns.distplot(women[women['Survived']==1].Age.dropna(), bins=18, label = survived, ax = axes[0], kde =False)
ax = sns.distplot(women[women['Survived']==0].Age.dropna(), bins=40, label = not_survived, ax = axes[0], kde =False)
ax.legend()
ax.set_title('Female')
ax = sns.distplot(men[men['Survived']==1].Age.dropna(), bins=18, label = survived, ax = axes[1], kde = False)
ax = sns.distplot(men[men['Survived']==0].Age.dropna(), bins=40, label = not_survived, ax = axes[1], kde = False)
ax.legend()
_ = ax.set_title('Male')

FacetGrid = sns.FacetGrid(train, row='Embarked', aspect=1.6)
FacetGrid.map(sns.pointplot, 'Pclass', 'Survived', 'Sex', palette=None,  order=None, hue_order=None )
FacetGrid.add_legend()

sns.barplot(x='Pclass', y='Survived', data=train)'''

#Part3
'''from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
#An 80/20 split ensures that 80% of the data is used for training the model
X = train.iloc[:, :-1]
y = train.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print(f"Training set shape: {X_train.shape}")
print(f"Validation set shape: {y_train.shape}")

log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

y_pred_log_reg = log_reg.predict(X_test)
accuracy_log_reg = accuracy_score(y_test, y_pred_log_reg)
print(f'Logistic Regression Accuracy: {accuracy_log_reg}')

random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit(X_train, y_train)
Y_prediction = random_forest.predict(X_test)
random_forest.score(X_train, y_train)
acc_random_forest = round(random_forest.score(X_train, y_train) * 100, 2)

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
X = train.drop('Survived', axis=1)
y = train['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Check data info 
#Fir the model using following command 
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
#predict value using following command 
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))'''


test['Age'].fillna(test['Age'].median(), inplace=True)
test['Fare'].fillna(test['Fare'].median(), inplace=True)
test['Sex'] = test['Sex'].map({'male': 0, 'female': 1})
test['Embarked'] = test['Embarked'].map({'C': 0, 'Q': 1, 'S': 2})
test['Embarked'].fillna(test['Embarked'].mode()[0], inplace=True)
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
X_test = test[features]
print(X_test)





