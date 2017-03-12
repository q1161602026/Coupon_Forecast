from feature_feature_extract import *

def extract_user_merchant_feature(feature_file_path,num):

	feature=pd.read_csv(feature1_file_path)

	user_merchant = feature[['User_id','Merchant_id']]
	user_merchant.drop_duplicates(inplace=True)

	# 用户领取该商家的所有优惠券个数
	t1 = feature[feature['Coupon_id'].notnull()][['User_id','Merchant_id']]
	t1.loc[:,'user_merchant_received'] = 1
	t1 = t1.groupby(['User_id','Merchant_id']).agg('sum').reset_index()
	print '用户领取该商家的所有优惠券个数提取'

	# 用户领取该商家优惠券核销次数
	t2 = feature[(feature.Date.notnull())&(feature.Date_received.notnull())][['User_id','Merchant_id']]
	t2.loc[:,'user_merchant_buy_use_coupon'] = 1
	t2 = t2.groupby(['User_id','Merchant_id']).agg('sum').reset_index()
	print '用户领取该商家优惠券核销次数提取'
	    

	# 用户领取该商家优惠券不核销次数
	t3 = feature[(feature.Date.isnull())&(feature.Date_received.notnull())][['User_id','Merchant_id']]
	t3.loc[:,'user_merchant_buy_notuse_coupon'] = 1
	t3 = t3.groupby(['User_id','Merchant_id']).agg('sum').reset_index()

	print '用户领取该商家优惠券不核销次数提取'

	# 用户总的不核销次数
	t4 = feature[(feature.Date.isnull())&(feature.Date_received.notnull())][['User_id']]
	t4.loc[:,'user_buy_notuse_coupon'] = 1
	t4 = t4.groupby(['User_id']).agg('sum').reset_index()
	print '用户总的不核销次数提取'


	# 用户总的核销次数
	t5 = feature[(feature.Date.notnull())&(feature.Date_received.notnull())][['User_id']]
	t5.loc[:,'user_buy_use_coupon'] = 1
	t5 = t5.groupby(['User_id']).agg('sum').reset_index()

	print '用户总的核销次数提取'


	# 商家总的不核销次数
	t6 = feature[(feature.Date.isnull())&(feature.Date_received.notnull())][['Merchant_id']]
	t6.loc[:,'merchant_sell_notuse_coupon'] = 1
	t6 = t6.groupby(['Merchant_id']).agg('sum').reset_index()

	print '商家总的不核销次数提取'

	# 商家总的核销次数
	t7 = feature[(feature.Date.notnull())&(feature.Date_received.notnull())][['Merchant_id']]
	t7.loc[:,'merchant_sell_use_coupon'] = 1
	t7 = t7.groupby(['Merchant_id']).agg('sum').reset_index()
	print '商家总的核销次数提取'

	user_merchant = pd.merge(user_merchant,t1,on=['User_id','Merchant_id'],how='left')
	user_merchant = pd.merge(user_merchant,t2,on=['User_id','Merchant_id'],how='left')
	user_merchant = pd.merge(user_merchant,t3,on=['User_id','Merchant_id'],how='left')
	user_merchant = pd.merge(user_merchant,t4,on=['User_id'],how='left')
	user_merchant = pd.merge(user_merchant,t5,on=['User_id'],how='left')
	user_merchant = pd.merge(user_merchant,t6,on=['Merchant_id'],how='left')
	user_merchant = pd.merge(user_merchant,t7,on=['Merchant_id'],how='left')


	# 用户领取该商家的优惠券核销率
	user_merchant.loc[:,'user_merchant_buy_use_coupon_rate']=user_merchant.apply(cal_user_merchant_buy_use_coupon_rate,axis=1)

	# 用户对每个商家的不核销次数占用户总的不核销次数的比重
	user_merchant.loc[:,'user_merchant_buy_notuse_coupon_of_user_buy_notuse_coupon_rate']=user_merchant.apply(cal_user_merchant_buy_notuse_coupon_of_user_buy_notuse_coupon_rate,axis=1)

	# 用户对每个商家的核销次数占用户总的核销次数的比重
	user_merchant.loc[:,'user_merchant_buy_use_coupon_of_user_buy_use_coupon_rate']=user_merchant.apply(cal_user_merchant_buy_use_coupon_of_user_buy_use_coupon_rate,axis=1)
	
	# 用户对每个商家的不核销次数占商家总的不核销次数的比重
	user_merchant.loc[:,'user_merchant_buy_notuse_coupon_of_merchant_sell_notuse_coupon_rate']=user_merchant.apply(cal_user_merchant_buy_notuse_coupon_of_merchant_sell_notuse_coupon_rate,axis=1)

	# 用户对每个商家的优惠券核销次数占商家总的核销次数的比重
	user_merchant.loc[:,'user_merchant_buy_use_coupon_of_merchant_sell_use_coupon_rate']=user_merchant.apply(cal_user_merchant_buy_use_coupon_of_merchant_sell_use_coupon_rate,axis=1)

	user_merchant.to_csv('data/user_merchant{0}.csv'.format(2),index=None)

if __name__ == '__main__':
	for k,path in enumerate(processed_feature_path):
    	extract_user_merchant_feature(path,k+1)