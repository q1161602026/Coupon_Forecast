#!/usr/bin/python 
#-*- coding: UTF-8 -*-   

import pandas as pd
import numpy as np
from config import *
from feature_extract import *
from datetime import date

def extract_user_feature(feature_file_path,num):
	print '第{0}个样本提取'.format(num)
	feature = pd.read_csv(feature_file_path)
	feature.drop_duplicates(inplace=True)

	user = feature[['User_id']]
	user.drop_duplicates(inplace=True)

	# 用户交易次数
	t0 = user_buy_count(feature)

	# 用户领取优惠券次数
	t1 = user_received_count(feature)

	# # 用户15天总的不核销次数
	# t2 = user_notuse_coupon_count(feature)

	# 用户15天总的核销次数
	t3 = user_buy_use_coupon_count(feature)

	# # 用户满0~50/50~200/200~500 减的优惠券核销数
	# t4 = user_discount_type_use_count(feature)
	
	# 用户核销优惠券中的平均/最大/最小用户-商家距离
	t5,t6,t7 = user_merchant_use_coupon_distance(feature)

	# 用户交易过的商家数提取
	t8 = user_merchants_count(feature)
	
	#用户核销天数提取
	t9,t10,t11=user_date_datereceived_gap(feature)

# 	用户核销满0~50/50~200/200~500减的优惠券占所有核销优惠券的比重
# 	t12 = user_each_rate_discount_rate(feature)

	user = pd.merge(user,t0,on=['User_id'],how='left')
	user = pd.merge(user,t1,on=['User_id'],how='left')
	# user = pd.merge(user,t2,on=['User_id'],how='left')
	user = pd.merge(user,t3,on=['User_id'],how='left')
	user = pd.merge(user,t5,on=['User_id'],how='left')
	user = pd.merge(user,t6,on=['User_id'],how='left')
	user = pd.merge(user,t7,on=['User_id'],how='left')
	user = pd.merge(user,t8,on=['User_id'],how='left')
	user = pd.merge(user,t9,on=['User_id'],how='left')
	user = pd.merge(user,t10,on=['User_id'],how='left')
	user = pd.merge(user,t11,on=['User_id'],how='left')
# 	user = pd.merge(user,t12,on=['User_id'],how='left')

	user.user_buy_use_coupon_count = user.user_buy_use_coupon_count.replace(np.nan,0)
	
	# 用户使用优惠券交易率

	user['user_buy_use_coupon_rate'] = user.user_buy_use_coupon_count.astype('float') / user.user_buy_count.astype('float') 
	
	# 用户使用优惠券率

	user.user_coupon_transfer_rate = user.user_buy_use_coupon_count.astype('float') / user.user_received_count.astype('float')

	user.user_buy_count = user.user_buy_count.replace(np.nan,0)
	user.user_buy_count = user.user_buy_count.astype('int')
	user.user_coupon_transfer_rate = user.user_coupon_transfer_rate.replace(np.nan,0)
	user.user_received_count = user.user_received_count.replace(np.nan,0)
	user.user_received_count = user.user_received_count.astype('int')
	# user.user_notuse_coupon_count = user.user_notuse_coupon_count.replace(np.nan,0)
	user.user_buy_use_coupon_count = user.user_buy_use_coupon_count.replace(np.nan,0)
	user.user_buy_use_coupon_count = user.user_buy_use_coupon_count.astype('int')
	user.user_buy_use_coupon_rate = user.user_buy_use_coupon_rate.replace(np.nan,0)
	user.drop_duplicates(inplace=True)
	user.to_csv('data/user{0}.csv'.format(num),index=None)
	
if __name__ == '__main__':
	for k,path in enumerate(processed_feature_path):
    	extract_user_feature(path,k+1)