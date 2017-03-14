#-*- coding: UTF-8 -*-   
from config import *
from feature_extract import *
import numpy as np
import pandas as pd
from datetime import date

def generate_train_test_set(train_or_test_path,num,train=True):
	print '第{0}个样本提取'.format(num)
	userpath = train_or_test_path.get('userpath')
	merchantpath = train_or_test_path.get('merchantpath')
	couponpath = train_or_test_path.get('couponpath')
	user_merchantpath = train_or_test_path.get('user_merchantpath')
	other_featurepath = train_or_test_path.get('other_featurepath')

	user = pd.read_csv(userpath)
	merchant = pd.read_csv(merchantpath)
	coupon = pd.read_csv(couponpath)
	user_merchant = pd.read_csv(user_merchantpath)
	other_feature = pd.read_csv(other_featurepath)
    
	dataset = pd.merge(other_feature,user,on=['User_id'],how='left')
	dataset = pd.merge(dataset,merchant,on=['Merchant_id'],how='left')
	dataset = pd.merge(dataset,coupon,on=['Coupon_id'],how='left')
	dataset = pd.merge(dataset,user_merchant,on=['User_id','Merchant_id'],how='left')
	dataset.drop_duplicates(inplace=True)
	dataset['Date_received']=dataset['Date_received'].astype('str')
	if train==True:
		dataset.loc[:,'label'] = dataset.apply(get_label,axis=1)
		dataset.drop(['User_id','Merchant_id','Coupon_id','Date','Date_received'],axis=1,inplace=True)
	# dataset.drop(['Merchant_id','Date','Date_received','Coupon_id'],axis=1,inplace=True)
	dataset = dataset.replace('null',np.nan)
	dataset.to_csv('data/dataset{0}.csv'.format(num),index=None)
    
    


if __name__ == '__main__':
	generate_train_test_set(train_path1,num=1)
	generate_train_test_set(train_path2,num=2)
	generate_train_test_set(test_path,num=3,train=False)