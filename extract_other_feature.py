#!/usr/bin/python 
#-*- coding: UTF-8 -*-   

import pandas as pd
import numpy as np
from config import *
from feature_extract import *
from datetime import date

def extract_other_feature(dataset_file_path,num):
	print '第{0}个样本提取'.format(num)
	other_feature = pd.read_csv(dataset_file_path)
	# other_feature.drop_duplicates(inplace=True)

	# 用户该月/该天收到的优惠券数
	t1 = user_this_month_all_coupon_count(other_feature)
	t2 = user_this_day_all_coupon_count(other_feature)
	t3 = user_this_month_same_coupon_count(other_feature)
	t4 = user_this_day_same_coupon_count(other_feature)

	other_feature = pd.merge(other_feature,t1,on='User_id')
	other_feature = pd.merge(other_feature,t2,on=['User_id','Date_received'])
	other_feature = pd.merge(other_feature,t3,on=['User_id','Coupon_id'])
	other_feature = pd.merge(other_feature,t4,on=['User_id','Coupon_id','Date_received'])

	# 用户收到的优惠券是哪一天/周末吗
	other_feature['day_of_week'] = other_feature.Date_received.astype('str').apply(lambda x:date(int(x[0:4]),int(x[4:6]),int(x[6:8])).weekday()+1 if x!='null' else 'null')
	# other_feature['day_of_month'] = other_feature.Date_received.astype('str').apply(lambda x:int(x[6:8]) if x!='null' else 'null')
	other_feature['is_weekend'] = other_feature.day_of_week.apply(lambda x:1 if x in (6,7) else 0 if x!='null' else 'null')

	other_feature = other_feature.drop(['Discount_rate'],axis=1)
	other_feature.to_csv('data/other_feature{0}.csv'.format(num),index=None)
    
if __name__ == '__main__':
	for k,path in enumerate(processed_dataset_path):
    	extract_other_feature(path,k+1)