import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import pickle

df = pd.read_csv('insurance.csv')

print(df.head())
print(df.info())
print(df['insurance_premium_category'].value_counts())

df_feat = df.copy()

df_feat['bmi'] = df_feat['weight'] / (df_feat['height'] ** 2)
print(df_feat[['weight', 'height', 'bmi']].head())

def age_group(age):
    if age <= 25:
        return 'young'
    elif age <= 45:
        return 'adult'
    elif age <= 60:
        return "middle_aged"
    return "senior"
df_feat['age_group']=df_feat['age'].apply(age_group)

print(df_feat[['age','age_group']].head)

def lifestyle_risk(row):
    smoker = row['smoker']
    bmi = row['bmi']
    if smoker==True and bmi> 30:
        return 'high'
    elif smoker==True or bmi> 27:
        return 'medium'
    else:
        return 'low'
df_feat['lifestyle_risk']=df_feat[['smoker','bmi']].apply(lifestyle_risk, axis=1)
print(df_feat[['smoker', 'bmi','lifestyle_risk']].head(10))
    
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = ["Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Bhopal",
                 "Nagpur", "Surat", "Rajkot", "Mysore", "Guwahati", "Kota", "Noida", "Coimbatore"]
    
def city_tier(city):
    if city in tier_1_cities:
        return 1
    elif city in tier_2_cities:
        return 2
    else:
        return 3
df_feat['city_tier']=df_feat['city'].apply(city_tier)
print(df_feat[['city', 'city_tier']].head(10))

print('#'*45)

X = df_feat[['age_group', 'lifestyle_risk', 'city_tier', 'bmi', 'income_lpa', 'occupation']]
Y = df_feat['insurance_premium_category']

print(X.head())
print('#$'*45)
print(Y.head())

X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

print('train : ',X_train.shape)
print("test : ", X_test.shape)


categorical_features =['age_group','lifestyle_risk','occupation']
numeric_features =['bmi','income_lpa','city_tier']

preprocessor = ColumnTransformer(
    transformers=[
        ('categorical',OneHotEncoder(),categorical_features),
        ('num','passthrough',numeric_features)
    ]
)
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])
pipeline.fit(X_train, Y_train)

Y_pred=pipeline.predict(X_test)

print('Accuracy : ',accuracy_score(Y_test,Y_pred))
print('*'*20)
print(classification_report(Y_test, Y_pred))

def save_train(pipeline):
    with open ('model.pkl','wb') as f:
        pickle.dump(pipeline,f)
save_train(pipeline)
print("✅")