import pandas as pd
import xgboost as xgb
from config import *
from sklearn.preprocessing import MinMaxScaler

train1 = pd.read_csv(train_file_path1)
train2 = pd.read_csv(train_file_path2)
test = pd.read_csv(test_file_path)

train = pd.concat([train1,train2],axis=0)

train1_x = train1.drop(['label'],axis=1)
train1_y = train1.label

train2_x = train2.drop(['label'],axis=1)
train2_y = train2.label

train_x = train.drop(['label'],axis=1)
train_y = train.label


test_x = test.drop(['User_id','Coupon_id','Merchant_id','Date_received'],axis=1)
test_preds = test[['User_id','Coupon_id','Date_received']]

print train_x.shape,test_x.shape

train = xgb.DMatrix(train_x,label=train_y)
train1 = xgb.DMatrix(train1_x,label=train1_y)
train2 = xgb.DMatrix(train2_x,label=train2_y)
test = xgb.DMatrix(test_x)

params={'booster':'gbtree',
		'objective': 'rank:pairwise',
		'eval_metric':'auc',
		'gamma':0.1,
		'min_child_weight':1.1,
		'max_depth':5,
		'lambda':10,
		'subsample':0.7,
		'colsample_bytree':0.7,
		'colsample_bylevel':0.7,
		'eta': 0.01,
		'tree_method':'exact',
		'seed':0,
		'nthread':12
	    }

#train on dataset1, evaluate on dataset2
# watchlist = [(train1,'train'),(train2,'val')]
watchlist = [(train,'train')]
# model = xgb.train(params,train,num_boost_round=300,evals=watchlist) #,early_stopping_rounds=300,xgb_model=model)
model = xgb.train(params,train,num_boost_round=7000,evals=watchlist,early_stopping_rounds=300)#,xgb_model=model)

#predict test set
test_preds.loc[:,'Probability'] = model.predict(test)
test_preds.Probability = MinMaxScaler().fit_transform(test_preds.Probability)
test_preds.sort_values(by=['Coupon_id','Probability'],inplace=True)
test_preds.to_csv("preds.csv",index=None)



