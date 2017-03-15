#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

from config import *
import pandas as pd

def train_test_split():
	
	offline_train = pd.read_csv(offline_train_file_path,dtype=columns_type)
	offline_test = pd.read_csv(offline_test_file_path,dtype=columns_type)

	feature1,feature2,test_feature = [offline_train[((offline_train['Date']!='null')&(offline_train['Date']>=x['feature_start_time'])&(offline_train['Date']<=x['feature_end_time']))|((offline_train['Date']=='null')&(offline_train['Date_received']>=x['feature_start_time'])&(offline_train['Date_received']<=x['feature_end_time']))] for x in feature_train_teat_split]

	dataset1,dataset2 = [offline_train[(offline_train['Date_received']!='null')&(offline_train['Date_received']>=x['dataset_start_time'])&(offline_train['Date_received']<=x['dataset_end_time'])] for x in dataset_train_test_split]
	test_dataset = offline_test

	for k,x in enumerate([feature1,feature2,test_feature]):
		x.to_csv(processed_feature_path[k],index=None)


	for k,x in enumerate([dataset1,dataset2,test_dataset]):
		x.to_csv(processed_dataset_path[k],index=None)

if __name__ == '__main__':
	train_test_split()