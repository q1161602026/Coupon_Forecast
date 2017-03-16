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
	print other_feature.shape
	# 用户该月/该天收到的优惠券数
	t1 = user_this_month_all_coupon_count(other_feature)
	t2 = user_this_day_all_coupon_count(other_feature)
	t3 = user_this_month_same_coupon_count(other_feature)
	t4 = user_this_day_same_coupon_count(other_feature)
	t5 = user_this_month_same_coupon_ago_late_date(other_feature)

	other_feature = pd.merge(other_feature,t1,on='User_id',how='left')
	other_feature = pd.merge(other_feature,t2,on=['User_id','Date_received'],how='left')
	other_feature = pd.merge(other_feature,t3,on=['User_id','Coupon_id'],how='left')

	other_feature = pd.merge(other_feature,t4,on=['User_id','Coupon_id','Date_received'],how='left')

	other_feature = pd.merge(other_feature,t5,on=['User_id','Coupon_id'],how='left')

	# 用户收到的优惠券是哪一天/周末吗
	other_feature['day_of_week'] = other_feature.Date_received.astype('str').apply(lambda x:date(int(x[0:4]),int(x[4:6]),int(x[6:8])).weekday()+1 if x!='null' else 'null')
	other_feature['is_weekend'] = other_feature.day_of_week.apply(lambda x:1 if x in (6,7) else 0 if x!='null' else 'null')
	other_feature['day_of_month'] = other_feature.Date_received.astype('str').apply(lambda x:int(x[6:8]) if x!='null' else 'null')

    
	other_feature.loc[:,'user_receive_coupon_first'] = other_feature.apply(lambda x:1 if (x['user_this_month_same_coupon_count']!=1)&(x['Date_received']==x['Date_received_min']) else 0,axis=1)
	other_feature.loc[:,'user_receive_coupon_last'] = other_feature.apply(lambda x:1 if (x['user_this_month_same_coupon_count']!=1)&(x['Date_received']==x['Date_received_max']) else 0,axis=1)
	other_feature['user_receive_coupon_first'][other_feature['user_this_month_same_coupon_count']==1] = -1
	other_feature['user_receive_coupon_last'][other_feature['user_this_month_same_coupon_count']==1] = -1

# 	other_feature = other_feature.drop(['Discount_rate'],axis=1)
	other_feature = other_feature.drop(['Date_received_min'],axis=1)
	other_feature = other_feature.drop(['Date_received_max'],axis=1)

	other_feature['discount_man'] = other_feature.Discount_rate.apply(get_discount_man)
	other_feature['discount_jian'] = other_feature.Discount_rate.apply(get_discount_jian)
	other_feature['is_man_jian'] = other_feature.Discount_rate.apply(is_man_jian)
	other_feature['discount_per'] = other_feature.Discount_rate.apply(calc_discount_rate)    
    
	print other_feature.shape

	other_feature.to_csv('data/other_feature{0}.csv'.format(num),index=None)
    
if __name__ == '__main__':
	for k,path in enumerate(processed_dataset_path):
    	extract_other_feature(path,k+1)