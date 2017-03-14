columns_type={
		'User_id':'str', 
		'Merchant_id':'str',
        'Coupon_id':'str', 
        'Discount_rate':'str',
        'Distance':'str',
        'Date_received':'str', 
        'Date':'str'}

# data file path
online_train_file_path = 'data/raw/ccf_online_stage1_train.csv'
offline_train_file_path = 'data/raw/ccf_offline_stage1_train.csv'
offline_test_file_path = 'data/raw/ccf_offline_stage1_test_revised.csv'

feature1_file_path = 'data/processed/train_feature1.csv'
feature2_file_path = 'data/processed/train_feature2.csv'
feature3_file_path = 'data/processed/test_feature3.csv'
processed_feature_path=[feature1_file_path,feature2_file_path,feature3_file_path]


dataset1_file_path = 'data/processed/train_dataset1.csv'
dataset2_file_path = 'data/processed/train_dataset2.csv'
dataset3_file_path = 'data/processed/test_dataset3.csv'
processed_dataset_path=[dataset1_file_path,dataset2_file_path,dataset3_file_path]


train_path1={'couponpath':'data/coupon1.csv',
			'merchantpath':'data/merchant1.csv',
			'userpath':'data/user1.csv',
			'user_merchantpath':'data/user_merchant1.csv',
			'other_featurepath':'data/other_feature1.csv'
			}
train_path2={'couponpath':'data/coupon2.csv',
			'merchantpath':'data/merchant2.csv',
			'userpath':'data/user2.csv',
			'user_merchantpath':'data/user_merchant2.csv',
			'other_featurepath':'data/other_feature2.csv'
			}
test_path={'couponpath':'data/coupon3.csv',
			'merchantpath':'data/merchant3.csv',
			'userpath':'data/user3.csv',
			'user_merchantpath':'data/user_merchant3.csv',
			'other_featurepath':'data/other_feature3.csv'
			}

train_file_path1 = 'data/dataset1.csv'
train_file_path2 = 'data/dataset2.csv'
test_file_path = 'data/dataset3.csv'


# raw field name
user_label = 'User_id'
merchant_label = 'Merchant_id'
coupon_label = 'Coupon_id'
action_label = 'Action'
discount_label = 'Discount_rate'
distance_label = 'Distance'
date_received_label = 'Date_received'
date_consumed_label = 'Date'
probability_consumed_label = 'Probability'

# global values
consume_time_limit = 15


feature_split_by_time1={
	'feature_start_time' : '20160101',
	'feature_end_time' : '20160413'
}

feature_split_by_time2={
	'feature_start_time' : '20160201',
	'feature_end_time' : '20160514'
}

feature_test={
	'feature_start_time' : '20160315',
	'feature_end_time' : '20160630'
}

feature_train_teat_split=[feature_split_by_time1,feature_split_by_time2,feature_test]



dataset_split_by_time1={
	'dataset_start_time' : '20160414',
	'dataset_end_time' : '20160514'
}

dataset_split_by_time2={
	'dataset_start_time' : '20160515',
	'dataset_end_time' : '20160615'
}

dataset_test={
	'dataset_start_time' : '20160701',
	'dataset_end_time' : '20160731'
}

dataset_train_test_split=[dataset_split_by_time1,dataset_split_by_time2]
