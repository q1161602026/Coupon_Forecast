#-*- coding: UTF-8 -*-   

from datetime import date
import pandas as pd


def cal_user_merchant_buy_use_coupon_rate(x):
	# 用户领取该商家优惠券15天核销率提取
	return 1.0*x['user_merchant_buy_use_coupon_count']/x['user_merchant_received_count']


def cal_user_merchant_notuse_coupon_of_user_buy_notuse_coupon_rate(x):
	return 1.0*x['user_merchant_notuse_coupon']/x['user_buy_notuse_coupon']


def cal_user_merchant_buy_use_coupon_of_user_buy_use_coupon_rate(x):
	return 1.0*x['user_merchant_buy_use_coupon_count']/x['user_buy_use_coupon_count']

def cal_user_buy_use_coupon_of_user_received_rate(x):
	return 1.0*x['user_buy_use_coupon_count']/x['user_received_count']

def cal_user_merchant_notuse_coupon_of_merchant_sell_notuse_coupon_rate(x):
	return 1.0*x['user_merchant_notuse_coupon']/x['merchant_sell_notuse_coupon_count']


def cal_user_merchant_buy_use_coupon_of_merchant_sell_use_coupon_rate(x):
	return 1.0*x['user_merchant_buy_use_coupon_count']/x['merchant_sell_use_coupon']

def cal_coupon_uesd_sales_rate(x):
	return 1.0*x['merchant_coupon_used_count']/x['merchant_sales_count']

def cal_user_discount_type_use_of_all_use_rate(x):
	# 用户核销满0~50/50~200/200~500减的优惠券占所有核销优惠券的比重
	return 1.0*x['user_discount_type_use_count']/x['user_buy_use_coupon_count']

def cal_merchant_coupon_used_rate(x):
	# 商家优惠券被领取后核销率
	return 1.0*x['merchant_coupon_used_count']/x['merchant_coupon_count']

def cal_merchant_discount_type_used_rate(x):
	# 商家被核销过的不同优惠券占所有核销领数量取的过的不同优惠券数量比重
	return 1.0*x['merchant_discount_type_used_count']/x['merchant_coupon_count']


def use_coupon_within_15days(x):
	days=(date(int(x['Date'][0:4]),int(x['Date'][4:6]),int(x['Date'][6:8]))-date(int(x['Date_received'][0:4]),int(x['Date_received'][4:6]),int(x['Date_received'][6:8]))).days
	if days < 16:
		return 1
	else:
		return 0


def user_notuse_coupon_count(feature):
	# 用户领取该优惠券15天不核销次数
	t3 = feature[(feature.Date=='null')&(feature.Date_received!='null')]
	t3.loc[:,'user_notuse_coupon_count'] = 1

	t3_2 = feature[(feature.Date!='null')&(feature.Date_received!='null')]
	t3_2.loc[:,'user_notuse_coupon_count'] = 1-t3_2.apply(use_coupon_within_15days,axis=1)

	t3 = pd.concat([t3,t3_2],axis=0,ignore_index=True)
	t3 = t3[['User_id','user_notuse_coupon_count']]
	t3 = t3.groupby(['User_id']).agg('sum').reset_index()
	t3 = t3[t3['user_notuse_coupon_count']!=0]
	print '用户领取该优惠券15天不核销次数提取'
	return t3

def user_merchant_received_count(feature):
	# 用户领取该商家的所有优惠券个数
	t1 = feature[feature['Coupon_id']!='null'][['User_id','Merchant_id']]
	t1.loc[:,'user_merchant_received_count'] = 1
	t1 = t1.groupby(['User_id','Merchant_id']).agg('sum').reset_index()
	print '用户领取该商家的所有优惠券个数提取'
	return t1


def user_merchant_buy_use_coupon_count(feature):
	# 用户领取该商家优惠券15天核销次数
	t2 = feature[(feature.Date!='null')&(feature.Date_received!='null')]
	t2.loc[:,'user_merchant_buy_use_coupon_count'] = t2.apply(use_coupon_within_15days,axis=1)
	t2 = t2[['User_id','Merchant_id','user_merchant_buy_use_coupon_count']]
	t2 = t2.groupby(['User_id','Merchant_id']).agg('sum').reset_index()
	t2 = t2[t2['user_merchant_buy_use_coupon_count']!=0]
	print '用户领取该商家优惠券15天核销次数提取'
	return t2



def user_buy_use_coupon_count(feature):
	# 用户15天总的核销次数
	t5 = feature[(feature.Date!='null')&(feature.Date_received!='null')]
	t5.loc[:,'user_buy_use_coupon_count'] = t5.apply(use_coupon_within_15days,axis=1)

	t5 = t5[['User_id','user_buy_use_coupon_count']]
	t5 = t5.groupby(['User_id']).agg('sum').reset_index()
	t5 = t5[t5['user_buy_use_coupon_count']!=0]
	print '用户15天总的核销次数提取'
	return t5


def user_received_count(feature):
	# 用户领取优惠券次数
	t1 = feature[feature['Coupon_id']!='null'][['User_id']]
	t1.loc[:,'user_received_count'] = 1
	t1 = t1.groupby(['User_id']).agg('sum').reset_index()
	print '用户领取所有优惠券个数提取'
	return t1

def user_discount_type_use_count(feature):
	# 用户满0~50/50~200/200~500减的优惠券核销数
	t4 = feature[(feature['Coupon_id']!='null')&(feature['Date']!='null')]
	t4.loc[:,'user_discount_type_use_count'] = t4.apply(use_coupon_within_15days,axis=1)
	t4 = t4[['User_id','Discount_rate','user_discount_type_use_count']]
	t4 = t4[t4['user_discount_type_use_count']!=0]
	t4.drop_duplicates(inplace=True)
	t4.groupby(['User_id','Discount_rate']).agg('sum').reset_index()
	print '用户满0~50/50~200/200~500减的优惠券核销数提取'
	return t4

def user_merchant_use_coupon_distance(feature):

	# 用户核销优惠券中的平均/最大/最小用户-商家距离
	t5 = feature[(feature['Coupon_id']!='null')&(feature['Date']!='null')&(feature['Distance']!='null')]
	t5.loc[:,'user_use_coupon'] = t5.apply(use_coupon_within_15days,axis=1)
	t5 = t5[t5['user_use_coupon']!=0]
	t5 =t5[['User_id','Distance']]
	t5.Distance = t5.Distance.astype('int')
	temp = t5.groupby('User_id')

	t6=temp.agg('min').reset_index()
	t6.rename(columns={'Distance':'user_min_distance'},inplace=True)

	t7 = temp.agg('max').reset_index()
	t7.rename(columns={'Distance':'user_max_distance'},inplace=True)

	t8 = temp.agg('mean').reset_index()
	t8.rename(columns={'Distance':'user_mean_distance'},inplace=True)
	print '用户核销距离提取'
	return t6,t7,t8

def user_merchant_count(feature):
	t1 = feature[feature.Date!='null'][['User_id','Merchant_id']]
	t1.drop_duplicates(inplace=True)
	t1.Merchant_id = 1
	t1 = t1.groupby('User_id').agg('sum').reset_index()
	t1.rename(columns={'Merchant_id':'user_merchant_count'},inplace=True)
	print '用户交易过的商家数提取'
	return t1

def get_user_date_datereceived_gap(s):
    return (date(int(s.Date[0:4]),int(s.Date[4:6]),int(s.Date[6:8])) - date(int(s.Date_received[0:4]),int(s.Date_received[4:6]),int(s.Date_received[6:8]))).days


def user_date_datereceived_gap(feature):
	t10 = feature[(feature.Date_received!='null')&(feature.Date!='null')][['User_id','Date_received','Date']]
	t10['user_date_datereceived_gap'] = t10.apply(get_user_date_datereceived_gap,axis=1)
	t10 = t10[['User_id','user_date_datereceived_gap']]

	t11 = t10.groupby('User_id').agg('mean').reset_index()
	t11.rename(columns={'user_date_datereceived_gap':'avg_user_date_datereceived_gap'},inplace=True)
	t12 = t10.groupby('User_id').agg('min').reset_index()
	t12.rename(columns={'user_date_datereceived_gap':'min_user_date_datereceived_gap'},inplace=True)
	t13 = t10.groupby('User_id').agg('max').reset_index()
	t13.rename(columns={'user_date_datereceived_gap':'max_user_date_datereceived_gap'},inplace=True)
	print '用户核销天数提取'
	return t11,t12,t13

def merchant_sales_count(feature):
	# 该商家的所有交易次数
	t1 = feature[feature.Date!='null'][['Merchant_id']]
	t1['merchant_sales_count'] = 1
	t1 = t1.groupby('Merchant_id').agg('sum').reset_index()
	print '该商家的所有交易次数提取'
	return t1

def merchant_coupon_count(feature):
	# 该商家的所有优惠券个数
	t7 = feature[(feature.Coupon_id!='null')][['Merchant_id']]
	t7.loc[:,'merchant_coupon_count'] = 1
	t7 = t7.groupby(['Merchant_id']).agg('sum').reset_index()
	print '该商家的所有优惠券个数提取'
	return t7

def merchant_coupon_used_count(feature):
	# 商家15天总的核销次数
	t7 = feature[(feature.Date!='null')&(feature.Date_received!='null')]
	t7.loc[:,'merchant_coupon_used_count'] = t7.apply(use_coupon_within_15days,axis=1)

	t7 = t7[['Merchant_id','merchant_coupon_used_count']]
	t7 = t7.groupby(['Merchant_id']).agg('sum').reset_index()
	t7 = t7[t7['merchant_coupon_used_count']!=0]
	print '商家总的核销次数提取'
	return t7

def merchant_coupon_notused_count(feature):
	# 商家15天总的不核销次数
	t6 = feature[(feature.Date=='null')&(feature.Date_received!='null')]
	t6.loc[:,'merchant_coupon_notused_count'] = 1

	t6_2 = feature[(feature.Date!='null')&(feature.Date_received!='null')]
	t6_2.loc[:,'merchant_coupon_notused_count'] = 1-t6_2.apply(use_coupon_within_15days,axis=1)

	t6 = pd.concat([t6,t6_2],axis=0,ignore_index=True)
	t6 = t6[['Merchant_id','merchant_coupon_notused_count']]
	t6 = t6.groupby(['Merchant_id']).agg('sum').reset_index()
	t6 = t6[t6['merchant_coupon_notused_count']!=0]
	print '商家15天总的不核销次数提取'
	return t6

def merchant_coupon_distance_count(feature):
	# 商家被核销优惠券中的平均/最小/最大用户-商家距离

	t5 = feature[(feature['Coupon_id']!='null')&(feature['Date']!='null')&(feature['Distance']!='null')]
	t5.loc[:,'user_use_coupon'] = t5.apply(use_coupon_within_15days,axis=1)
	t5 = t5[t5['user_use_coupon']!=0]
	t5 =t5[['Merchant_id','Distance']]
	t5.Distance = t5.Distance.astype('int')
	temp = t5.groupby('Merchant_id')

	t6=temp.agg('min').reset_index()
	t6.rename(columns={'Distance':'merchant_min_distance'},inplace=True)

	t7 = temp.agg('max').reset_index()
	t7.rename(columns={'Distance':'merchant_max_distance'},inplace=True)

	t8 = temp.agg('mean').reset_index()
	t8.rename(columns={'Distance':'merchant_mean_distance'},inplace=True)
	print '商家被核销优惠券中的平均/最小/最大用户-商家距离'
	return t6,t7,t8


def merchant_discount_type_used_count(feature):
	# 商家每种优惠券核销多少张
	t4 = feature[(feature['Date_received']!='null')&(feature['Date']!='null')]
	t4.loc[:,'merchant_discount_type_used_count'] = t4.apply(use_coupon_within_15days,axis=1)
	t4 = t4[['Merchant_id','Discount_rate','merchant_discount_type_used_count']]
	t4 = t4[t4['merchant_discount_type_used_count']!=0]
	t4.drop_duplicates(inplace=True)
	t4.groupby(['Merchant_id','Discount_rate']).agg('sum').reset_index()
	print '商家每种优惠券核销数提取'
	return t4


def calc_discount_rate(x):
    x =str(x)
    x = x.split(':')
    if len(x)==1:
        return float(x[0])
    else:
        return 1.0-float(x[1])/float(x[0])

def get_discount_man(x):
    x =str(x)
    x = x.split(':')
    if len(x)==1:
        return 'null'
    else:
        return int(x[0])
        
def get_discount_jian(x):
    x =str(x)
    x = x.split(':')
    if len(x)==1:
        return 'null'
    else:
        return int(x[1])

def is_man_jian(x):
    x =str(x)
    x = x.split(':')
    if len(x)==1:
        return 0
    else:
        return 1
