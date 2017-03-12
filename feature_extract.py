

def cal_user_merchant_buy_use_coupon_rate(x):
        return 1.0*x['user_merchant_buy_use_coupon']/x['user_merchant_received']


def cal_user_merchant_buy_notuse_coupon_of_user_buy_notuse_coupon_rate(x):
        return 1.0*x['user_merchant_buy_notuse_coupon']/x['user_buy_notuse_coupon']


def cal_user_merchant_buy_use_coupon_of_user_buy_use_coupon_rate(x):
        return 1.0*x['user_merchant_buy_use_coupon']/x['user_buy_use_coupon']


def cal_user_merchant_buy_notuse_coupon_of_merchant_sell_notuse_coupon_rate(x):
		return 1.0*x['user_merchant_buy_notuse_coupon']/x['merchant_sell_notuse_coupon']


def cal_user_merchant_buy_use_coupon_of_merchant_sell_use_coupon_rate(x):
		return 1.0*x['user_merchant_buy_use_coupon']/x['merchant_sell_use_coupon']
