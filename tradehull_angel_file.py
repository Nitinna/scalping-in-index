# https://trade.angelbroking.com/Login
# https://smartapi.angelbroking.com/signin

import warnings
from smartapi import SmartConnect
import pdb
import requests
import pandas as pd
import datetime
import time
import mibian
import pyotp

step_values = {'BANKNIFTY':100, 'NIFTY':50, 'AARTIIND': 20, 'ACC': 20, 'ADANIENT': 20, 'ADANIPORTS': 10, 'ALKEM': 20, 'AMARAJABAT': 10, 'AMBUJACEM': 5, 'APLLTD': 10, 'APOLLOHOSP': 50, 'APOLLOTYRE': 5, 'ASHOKLEY': 2.5, 'ASIANPAINT': 20, 'AUBANK': 20, 'AUROPHARMA': 10, 'AXISBANK': 10, 'BAJAJ-AUTO': 50, 'BAJAJFINSV': 100, 'BAJFINANCE': 100, 'BALKRISIND': 20, 'BANDHANBNK': 5, 'BANKBARODA': 2.5, 'BATAINDIA': 20, 'BEL': 2.5, 'BERGEPAINT': 10, 'BHARATFORG': 10, 'BHARTIARTL': 10, 'BHEL': 1, 'BIOCON': 5, 'BOSCHLTD': 250, 'BPCL': 10, 'BRITANNIA': 20, 'CADILAHC': 5, 'CANBK': 5, 'CHOLAFIN': 10, 'CIPLA': 10, 'COALINDIA': 2.5, 'COFORGE': 50, 'COLPAL': 20, 'CONCOR': 10, 'CUB': 2.5, 'CUMMINSIND': 20, 'DABUR': 5, 'DEEPAKNTR': 20, 'DIVISLAB': 50, 'DLF': 5, 'DRREDDY': 50, 'EICHERMOT': 50, 'ESCORTS': 20, 'EXIDEIND': 2.5, 'FEDERALBNK': 1, 'GAIL': 2.5, 'GLENMARK': 5, 'GMRINFRA': 1, 'GODREJCP': 10, 'GODREJPROP': 20, 'GRANULES': 5, 'GRASIM': 20, 'GUJGASLTD': 10, 'HAVELLS': 20, 'HCLTECH': 10, 'HDFC': 50, 'HDFCAMC': 50, 'HDFCBANK': 20, 'HDFCLIFE': 10, 'HEROMOTOCO': 50, 'HINDALCO': 5, 'HINDPETRO': 5, 'HINDUNILVR': 20, 'IBULHSGFIN': 5, 'ICICIBANK': 10, 'ICICIGI': 20, 'ICICIPRULI': 5, 'IDEA': 1, 'IDFCFIRSTB': 1, 'IGL': 10,
			   'INDIGO': 20, 'INDUSINDBK': 20, 'INDUSTOWER': 5, 'INFY': 20, 'IOC': 1, 'IRCTC': 20, 'ITC': 2.5, 'JINDALSTEL': 10, 'JSWSTEEL': 5, 'JUBLFOOD': 50, 'KOTAKBANK': 20, 'L&TFH': 2.5, 'LALPATHLAB': 50, 'LICHSGFIN': 10, 'LT': 20, 'LTI': 100, 'LTTS': 50, 'LUPIN': 20, 'M&M': 10, 'M&MFIN': 5, 'MANAPPURAM': 2.5, 'MARICO': 5, 'MARUTI': 100, 'MCDOWELL-N': 5, 'MFSL': 20, 'MGL': 20, 'MINDTREE': 20, 'MOTHERSUMI': 5, 'MPHASIS': 20, 'MRF': 500, 'MUTHOOTFIN': 20, 'NAM-INDIA': 5, 'NATIONALUM': 1, 'NAUKRI': 100, 'NAVINFLUOR': 50, 'NESTLEIND': 100, 'NMDC': 2.5, 'NTPC': 1, 'ONGC': 2.5, 'PAGEIND': 500, 'PEL': 50, 'PETRONET': 5, 'PFC': 2.5, 'PFIZER': 50, 'PIDILITIND': 20, 'PIIND': 20, 'PNB': 1, 'POWERGRID': 2.5, 'PVR': 20, 'RAMCOCEM': 10, 'RBLBANK': 5, 'RECLTD': 2.5, 'RELIANCE': 20, 'SAIL': 2.5, 'SBILIFE': 10, 'SBIN': 5, 'SHREECEM': 500, 'SIEMENS': 20, 'SRF': 100, 'SRTRANSFIN': 20, 'SUNPHARMA': 10, 'SUNTV': 10, 'TATACHEM': 10, 'TATACONSUM': 10, 'TATAMOTORS': 5, 'TATAPOWER': 2.5, 'TATASTEEL': 10, 'TCS': 50, 'TECHM': 20, 'TITAN': 20, 'TORNTPHARM': 20, 'TORNTPOWER': 5, 'TRENT': 20, 'TVSMOTOR': 10, 'UBL': 20, 'ULTRACEMCO': 100, 'UPL': 10, 'VEDL': 5, 'VOLTAS': 20, 'WIPRO': 5, 'ZEEL': 5}

warnings.filterwarnings("ignore")


def angelbrok_login():
	try:
		global feed_token, client_code, angel, password

		angel = SmartConnect(api_key="F78V76K0")
		client_code = "N303894"
		password = "Nitin&123"
		token = 'ADVGBRQACAVTVMNFT4N357PJ3A'

		data = angel.generateSession(client_code, password, pyotp.TOTP(token).now())
		refreshToken = data['data']['refreshToken']
		feed_token = angel.getfeedToken()
		print("Login successful")
	except Exception as e:
		print("Error in login", e)


angelbrok_login()


def get_instruments():
	global instrument_df
	url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
	request = requests.get(url=url, verify=False)
	data = request.json()
	instrument_df = pd.DataFrame(data)
	instrument_df.to_csv("instruments.csv")
	instrument_df.set_index("symbol", inplace=True)
	return instrument_df

instrument_df = get_instruments()


def get_token_and_exchange(name):
	symboltoken = instrument_df.loc[name]['token']
	exchange = instrument_df.loc[name]['exch_seg']
	return symboltoken, exchange


def get_ohlc(name, exchange):
	symboltoken = instrument_df.loc[name]['token']
	ohlc_data = angel.ltpData(exchange, name, symboltoken)
	ohlc_data = ohlc_data['data']
	return ohlc_data


def get_ltp(name, exchange):
	symboltoken = instrument_df.loc[name]['token']
	ltp_data = angel.ltpData(exchange, name, symboltoken)
	ltp = ltp_data['data']['ltp']
	return ltp


def lot_size(name):
	lot = instrument_df.loc[name]['lotsize']
	return lot


def get_historical_data(name, interval, timeperiod):

	token, exchange = get_token_and_exchange(name)


	try:
		intervals_dict = {'1min': 'ONE_MINUTE', '3min': 'THREE_MINUTE', '5min': 'FIVE_MINUTE', '10min': 'TEN_MINUTE', '15min': 'FIFTEEN_MINUTE', '30min': 'THIRTY_MINUTE', 'hour': 'ONE_HOUR', 'day': 'ONE_DAY'}
		todate = str(datetime.datetime.now())[:16]
		from_date = str(datetime.datetime.now().date() - datetime.timedelta(days=timeperiod))+" "+"09:15"
		symboltoken = instrument_df.loc[name]['token']
		historicParam = {"exchange": exchange, "symboltoken": symboltoken, "interval": intervals_dict[interval], "fromdate": from_date,  "todate": todate}
		response = angel.getCandleData(historicParam)
		dict1 = {}
		historic_df = pd.DataFrame()
		for data in response['data']:
			dict1['date'] = data[0]
			dict1['open'] = data[1]
			dict1['high'] = data[2]
			dict1['low'] = data[3]
			dict1['close'] = data[4]
			dict1['volume'] = data[5]
			historic_df = historic_df.append(dict1, ignore_index=True)
		return historic_df
	except Exception as e:
		print(e)


def place_order(orderparams):

	time.sleep(1)


	orderId = angel.placeOrder(orderparams)
	print("		order is placed with orderid= ", orderId)
	return orderId



def option_name_finder(multiplier, name, exipry, ce_pe):
	temp_name = name.split("-")[0]
	ltp = get_ltp(name=name, exchange='NSE')
	step_value = step_values[temp_name]
	atm_strike = round(ltp/step_value)*step_value + multiplier*step_value
	option_name = temp_name + exipry + str(atm_strike) + 'CE'
	return option_name


def make_straddle(name, exipry, gap):
	ltp = get_ltp(name, "NSE")
	atm_strike = round(ltp/gap)*gap
	call_name = name + exipry + str(atm_strike) + 'CE'
	put_name = name + exipry + str(atm_strike) + 'PE'
	return [call_name, put_name]


def get_combined_premium(call_orderId, put_orderId):
	orders = pd.DataFrame(angel.orderBook()['data'])

	call_avg_price = float(orders.loc[orders['orderid'] == call_orderId]['averageprice'])
	put_avg_price = float(orders.loc[orders['orderid'] == put_orderId]['averageprice'])
	
	combined_premium = call_avg_price + put_avg_price

	return combined_premium

def get_current_premium(call_script, put_script):
	call_ltp= get_ltp(call_script,"NFO")
	put_ltp= get_ltp(put_script,"NFO")
	current_premium = call_ltp + put_ltp
	return current_premium

def get_option_greeks(name, call_strike, put_strike, expiry):
    underlying_price = get_ltp(name=name,exchange="NSE")
    underlying_name = name.split("-")[0]
    call_script = underlying_name+ expiry +str(call_strike)+"CE"
    put_script = underlying_name+ expiry +str(put_strike)+"PE"
    call_price = get_ltp(name=call_script,exchange="NFO")
    put_price = get_ltp(name=put_script,exchange="NFO")
    interest_rate = 7
    days_to_expiry = 20


    civ = mibian.BS([underlying_price, call_strike, interest_rate, days_to_expiry], callPrice= call_price)
    print("Greeks for: ", "\t" ,call_script)
    print("IV :" , "\t\t" ,civ.impliedVolatility)

    cval = mibian.BS([underlying_price, call_strike, interest_rate, days_to_expiry],volatility = civ.impliedVolatility ,callPrice= call_price)
    print("callPrice: ", "\t" , cval.callPrice)
    print("callDelta: ", "\t" , cval.callDelta)
    print("callTheta: ", "\t" , cval.callTheta)
    print("vega: ", "\t\t" , cval.vega)
    print("gamma: ", "\t" , cval.gamma)
    print("\n","-------------------------------------------------------------------","\n")
    
    piv = mibian.BS([underlying_price, put_strike, interest_rate, days_to_expiry], putPrice= put_price)
    print("Greeks for: ", "\t" , put_script)
    print("IV : ", "\t\t" , piv.impliedVolatility)
    
    pval = mibian.BS([underlying_price, put_strike, interest_rate, days_to_expiry],volatility = piv.impliedVolatility ,putPrice= put_price)
    print("callPrice: ", "\t" , pval.callPrice)
    print("callDelta: ", "\t" , pval.callDelta)
    print("callTheta: ", "\t" , pval.callTheta)
    print("vega: ", "\t\t" , pval.vega)
    print("gamma: ", "\t" , pval.gamma)


def telegram_bot_sendtext(bot_message):
	# in bot_message give any message which you want to send into telegram 

	bot_token = '5799830063:AAG8wvXFxxTbnkI3aUJAvyp1HFcCDV5mEv0'
	bot_chatID = '551998351'
	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id='+ bot_chatID + '&text=' + bot_message
	response = requests.get(send_text)

	return response.json()
