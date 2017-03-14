#!/usr/bin/python 
#-*- coding: UTF-8 -*-   

import pandas as pd
import numpy as np
from config import *
from feature_extract import *
from datetime import date

def extract_user_merchant_feature(feature_file_path,num):
	print '第{0}个样本提取'.format(num)
	feature = pd.read_csv(feature_file_path)

	user_merchant = feature[['User_id','Merchant_id']]
	user_merchant.drop_duplicates(inplace=True)

	# 用户领取该商家的所有优惠券个数
	t1 = user_merchant_received_count(feature)

	# 用户领取该商家优惠券15天核销次数
	t2 = user_merchant_buy_use_coupon_count(feature)

	# 用户15天总的核销次数(no)
	t5 = user_buy_use_coupon_count(feature)


	user_merchant = pd.merge(user_merchant,t1,on=['User_id','Merchant_id'],how='left')
	user_merchant = pd.merge(user_merchant,t2,on=['User_id','Merchant_id'],how='left')
	user_merchant = pd.merge(user_merchant,t5,on=['User_id'],how='left')

	# 用户领取该商家的优惠券核销率
	user_merchant.loc[:,'user_merchant_buy_use_coupon_rate'] = user_merchant.apply(cal_user_merchant_buy_use_coupon_rate,axis=1)
	print '用户领取该商家的优惠券核销率提取'
	
	# 用户对每个商家的核销次数占用户总的核销次数的比重
	user_merchant.loc[:,'user_merchant_buy_use_coupon_of_user_buy_use_coupon_rate'] = user_merchant.apply(cal_user_merchant_buy_use_coupon_of_user_buy_use_coupon_rate,axis=1)
	print '用户对每个商家的核销次数占用户总的核销次数的比重提取'

	user_merchant = user_merchant[['User_id','Merchant_id','user_merchant_received_count','user_merchant_buy_use_coupon_count','user_merchant_buy_use_coupon_rate','user_merchant_buy_use_coupon_of_user_buy_use_coupon_rate']]
	user_merchant.user_merchant_received_count = user_merchant.user_merchant_received_count.replace(np.nan,0)
	user_merchant.user_merchant_buy_use_coupon_count = user_merchant.user_merchant_buy_use_coupon_count.replace(np.nan,0)
	user_merchant.user_merchant_buy_use_coupon_rate = user_merchant.user_merchant_buy_use_coupon_rate.replace(np.nan,0)
	user_merchant.user_merchant_buy_use_coupon_of_user_buy_use_coupon_rate = user_merchant.user_merchant_buy_use_coupon_of_user_buy_use_coupon_rate.replace(np.nan,0)

	user_merchant.to_csv('data/user_merchant{0}.csv'.format(num),index=None)


if __name__ == '__main__':
	for k,path in enumerate(processed_feature_path):
    	extract_user_merchant_feature(path,k+1)