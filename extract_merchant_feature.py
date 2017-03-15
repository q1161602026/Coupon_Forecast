#!/usr/bin/python 
#-*- coding: UTF-8 -*-   
import pandas as pd
import numpy as np
from config import *
from feature_extract import *
from datetime import date

import pandas as pd
import numpy as np
from config import *
from feature_extract import *
from datetime import date

def extract_merchant_feature(feature_file_path,num):
	print '第{0}个样本提取'.format(num)
	feature = pd.read_csv(feature_file_path)

	merchant = feature[['Merchant_id']]
	merchant.drop_duplicates(inplace=True)

	# 该商家的所有交易数
	t0 = merchant_sales_count(feature)

	# 该商家的所有优惠券个数
	t1 = merchant_coupon_count(feature)

	# 商家优惠券被领取后15天核销次数
	t2 = merchant_coupon_used_count(feature)

# 	商家优惠券被领取后15天不核销次数
# 	t3 = merchant_coupon_notused_count(feature)

	# 商家被核销优惠券中的(平均、最小、最大)用户-商家距离
	t4,t5,t6 = merchant_coupon_distance_count(feature)
	
	# 商家被核销优惠券天数
	t9,t10,t11=merchant_date_datereceived_gap(feature)

	# 商家每种优惠券核销多少张
	# t7 = merchant_discount_type_used_count(feature)
	
	merchant = pd.merge(merchant,t0,on='Merchant_id',how='left')
	merchant = pd.merge(merchant,t1,on='Merchant_id',how='left')
	merchant = pd.merge(merchant,t2,on='Merchant_id',how='left')
# 	merchant = pd.merge(merchant,t3,on='Merchant_id',how='left')
	merchant = pd.merge(merchant,t4,on='Merchant_id',how='left')
	merchant = pd.merge(merchant,t5,on='Merchant_id',how='left')
	merchant = pd.merge(merchant,t6,on='Merchant_id',how='left')
	merchant = pd.merge(merchant,t9,on='Merchant_id',how='left')
	merchant = pd.merge(merchant,t10,on='Merchant_id',how='left')
	merchant = pd.merge(merchant,t11,on='Merchant_id',how='left')
	# merchant=pd.merge(merchant,t7,on='Merchant_id',how='left')

	# # 商家被核销过的不同优惠券占所有核销领数量取的过的不同优惠券数量比重
	# merchant.loc[:,'merchant_coupontype_used_rate']=merchant.apply(cal_merchant_coupontype_used_rate,axis=1)

	# 商家优惠券被领取后核销率
	merchant.loc[:,'merchant_coupon_used_rate'] = merchant.apply(cal_merchant_coupon_used_rate,axis=1)
	merchant.merchant_coupon_used_rate = merchant.merchant_coupon_used_rate.replace(np.nan,0)
	merchant.loc[:,'coupon_uesd_sales_rate'] = merchant.apply(cal_coupon_uesd_sales_rate,axis=1)
	
	merchant.coupon_uesd_sales_rate = merchant.coupon_uesd_sales_rate.replace(np.nan,0)
	merchant.merchant_coupon_count = merchant.merchant_coupon_count.replace(np.nan,0)
	merchant.merchant_coupon_count = merchant.merchant_coupon_count.astype('int')
	merchant.merchant_coupon_used_count = merchant.merchant_coupon_used_count.replace(np.nan,0)
	merchant.merchant_coupon_used_count = merchant.merchant_coupon_used_count.astype('int')
	merchant.merchant_sales_count = merchant.merchant_sales_count.replace(np.nan,0)
	merchant.merchant_sales_count = merchant.merchant_sales_count.astype('int')
# 	merchant.merchant_coupon_notused_count = merchant.merchant_coupon_notused_count.replace(np.nan,0)

	# user_merchant = user_merchant[['Merchant_id','merchant_coupon_count','merchant_coupon_used_count','merchant_coupon_distance_count','merchant_coupontype_used_rate','merchant_coupon_used_rate']]
	merchant.to_csv('data/merchant{0}.csv'.format(num),index=None)



if __name__ == '__main__':
	for k,path in enumerate(processed_feature_path):
    	extract_merchant_feature(path,k+1)