#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import generators
from __future__ import division
from __future__ import absolute_import
from __future__ import with_statement
from __future__ import nested_scopes

""" Forward Compatability Test (Python 3.x)"""


""" 
===================================================
=  Author:LI XIANGJUN                             
=  Email: lixiangjun941@gmail.com    
=                                                 
=  Singapore Management University                
=  Sim Kee Boon Institute for Financial Economics 
=  June-2015                                       
==================================================
"""


import json,requests
import datetime
import time
from settings import *
from Cryptsy_database import cryptsy_database
import get_key
from time_conversion import time_cryptsy
from multiprocessing import Process, Pipe
import os
from math import ceil
import datetime

class Cryptsy():
	def __init__(self,settings):
		self.API_address = settings["API_address"]
		self.db_host = settings["db_host"]
		self.db_user = settings["db_user"]
		self.db_password = settings["db_password"]
		self.db_port = settings["db_port"]
		self.db_use_unicode = settings["db_use_unicode"]
		self.charset = settings["charset"]
		self.db_name = settings["db_name"]
		self.cryptsy_database_instance = cryptsy_database(self.db_user,self.db_password,self.db_name,\
													self.db_host,self.db_port,self.db_use_unicode,self.charset)
		self.time_cryptsy = time_cryptsy()
		self.temporaryHold = {}
		for i in range(0,10000):
			self.temporaryHold['%d'%i] = [[0,0]]
		self.marketlable={} #  'market_label':id 
	def __del__(self):
		del self.cryptsy_database_instance

	def json_Obj_Update(self):
		"""
		Note: I/O bound
		Usage:
		json_obj = json_Obj_Update(API_address)
		"""
		"""
		Exceptions:
		In the event of a network problem (e.g. DNS failure, refused connection, etc), 
		Requests will raise a ConnectionError exception.

		In the rare event of an invalid HTTP response, 
		Requests will raise an HTTPError exception.

		If a request times out, a Timeout exception is raised.

		If a request exceeds the configured number of maximum redirections, 
		a TooManyRedirects exception is raised.

		All exceptions that Requests explicitly raises inherit from 
		requests.exceptions.RequestException.
		"""
		try:
			print("Starting to retrieve data from the server ...")
			self.response = requests.get(self.API_address,timeout = (6.05,10)) #connect,read timeouts
			self.time_cryptsy.update() #Record the tiem at which the data is received
			
		except requests.exceptions.RequestException:
			raise

		if str(self.response.text[11:12])!="1": 
			raise Exception("status indicator: 'success:'1 not detected. Retriving information from the server failed!")
		
		try:
			self.json_obj = json.loads(self.response.text)
		except:
			raise


	def debug_Import_json_object(self,filename): #For debugging purposes
		self.json_import = open("%s.json"%filename,'r')
		self.json_obj = json.loads(self.json_import.read())

	def Save_json_object(self):#once exception --> save + write log
		"""
		return: None
		parameter response of requests.get
		response_of_requests = requests.get(url)
		"""
		try:
			name_of_file = str(int(self.time_cryptsy.Unix_epoch))
			json_storage = open("%s.json"%name_of_file,'w')
			json_storage.write(self.response.text)
		except Exception as e:
			print("Saving response as *.json Failed!")

	def return_market_info_as_a_list(self):
		return_list = [] #Python list declaration
		try:
			for i_market in self.json_obj['return']["markets"]:
				for m,n in self.json_obj['return']["markets"]["%s"%str(i_market)].items():
					if (str(n).lower()=='none'):
						self.json_obj['return']["markets"]["%s"%str(i_market)]['%s'%m] = None
				
				return_list.append((\
								int(self.json_obj['return']["markets"]["%s"%str(i_market)]["marketid"]),\
								str(self.json_obj['return']["markets"]["%s"%str(i_market)]["label"]),\
								   (self.json_obj['return']["markets"]["%s"%str(i_market)]["lasttradeprice"]),\
								str(self.json_obj['return']["markets"]["%s"%str(i_market)]["volume"]),\
								self.time_cryptsy.strpi_time_to_Unix_Epoch_format_UTC(time_string=str(self.json_obj['return']["markets"]["%s"%str(i_market)]["lasttradetime"])),\
								str(self.json_obj['return']["markets"]["%s"%str(i_market)]["primarycode"]),\
								str(self.json_obj['return']["markets"]["%s"%str(i_market)]["secondarycode"]),\
								str(self.json_obj['return']["markets"]["%s"%str(i_market)]["primaryname"]),\
								str(self.json_obj['return']["markets"]["%s"%str(i_market)]["secondaryname"]),\
								  ))
				self.time_cryptsy.strpi_time_to_Unix_Epoch_format_UTC()

				""" 
				Index of  items in the sub-list :
							0	int  --                   "marketid" 
							1	str  --                   "label" 
							2	str  --                   "lasttradeprice" 
							3	str  --                   "volume" 
							4	int_Unix_UTC      "lasttradetime" 
							5	str  --                   "primarycode" 
							6	str  --                   "secondarycode" 
							7	str  --                   "primaryname" 
							8	str  --                   "secondaryname" 
				"""
		except Exception as e:
			print (e,i_market)
			raise

		finally:
			return return_list

	def return_recent_trades_as_a_list(self,market_label=""):
		return_list = [] #Python list declaration
		try:
			for i_trade in self.json_obj['return']["markets"]["%s"%str(market_label)]["recenttrades"]:

				return_list.append((\
								(i_trade["id"]),\
								self.time_cryptsy.strpi_time_to_Unix_Epoch_format_UTC(str(i_trade["time"])),\
								str(i_trade["type"]),\
								str(i_trade["price"]),\
								str(i_trade["quantity"]),\
								str(i_trade["total"])\
								))
				""" 
				Index of the items in the sub-list :
							0	int--  "id" 
							1	int_Unix_UTC--  "time" 
							2	str--  "type" 
							3	str--  "price" 
							4	str--  "quantity" 
							5	str--  "total" 						
				"""
		except:
			print("ALERT: There is no recent trades for %d"%market_label)
		finally:
			return return_list

	def return_buy_orders_as_a_list(self,market_label=""):
		return_list = [] #Python list declaration
		try:
			for i_buy_order in self.json_obj['return']["markets"]["%s"%str(market_label)]["buyorders"]:
				return_list.append((\
								str(i_buy_order["price"]),\
								str(i_buy_order["total"]),\
								str(i_buy_order["quantity"])\
								))
				""" 
				Index of the items in the sub-list :
							0	str--  "price" 
							1	str--  "total" 
							2	str--  "quantity" 
				"""
		except:
				print("ALERT: There is no buy orders for %d"%market_label)
		finally:
			return return_list

	def return_sell_orders_as_a_list(self,market_label=""):
		return_list = [] #Python list declaration
		try:
			for i_sell_order in self.json_obj['return']["markets"]["%s"%str(market_label)]["sellorders"]:
				return_list.append((\
								str(i_sell_order["price"]),\
								str(i_sell_order["total"]),\
								str(i_sell_order["quantity"])\
								))
				""" 
				Index of the items in the sub-list :
							0	str--  "price" 
							1	str--  "total" 
							2	str--  "quantity" 
				"""
		except:
			print("ALERT: There is no sell orders for %d"%market_label)
		finally:
			return return_list

	def generate_dictionaries_linking_market_label_with_market_id(self):
		"""
		Decription: Generate two dictionaries for quick referrence later on        
		self.dict_for_marktlabel_to_market_id
		self.dict_for_market_id_to_marktlabel
		"""
		self.dict_for_marktlabel_to_market_id = {} #Python dictionary declaration
		self.dict_for_market_id_to_marktlabel =  {} #Python dictionary declaration

		for i_market in self.json_obj["return"]["markets"]:
			self.dict_for_marktlabel_to_market_id[str(i_market)] = int(self.json_obj["return"]["markets"][str(i_market)]["marketid"])
		for i_market in self.dict_for_marktlabel_to_market_id:
			self.dict_for_market_id_to_marktlabel[int(self.dict_for_marktlabel_to_market_id[str(i_market)])] = str(i_market)

	def query_market_or_market_label(self,market_id=-1,market_label="0XFFFFFF"):
		"""
		Description:
		This function is to query market_id from market_label
							   or market_label from market_id

		Parameter: (int)market_id (str)market_label (Pass in either one)
		Return type:
		1)market_id    to   marktlabel --> str 
		2)marktlabel   to   market_id  --> int

		"""
		dict_for_marktlabel_to_market_id, dict_for_market_id_to_marktlabel =\
				self.generate_dictionaries_linking_market_label_with_market_id()
		try:
			if (market_id==-1)and(market_label=="0XFFFFFF"):
				raise Exception("No argument passed in: function query_market_or_market_label exits")
			else:
				try:	
					if(market_id!=-1):
						return dict_for_market_id_to_marktlabel[market_id]
					else:
						return dict_for_marktlabel_to_market_id[market_label]
				except KeyError as err:
					raise KeyError("Returned KeyError message:",err,"parameters passed in : %s and %s"%(str(market_id),market_label))
				except:
					raise Exception("Unknown errors in function query_market_or_market_label",\
									"parameters passed in : %s and %s"%(str(market_id),market_label))
				finally:
					pass
		except Exception as e: 
			raise   
		finally:
			pass
	
	def process(self):
		self.generate_dictionaries_linking_market_label_with_market_id()
		market_info = self.return_market_info_as_a_list()
		market_info = sorted(market_info, key=get_key.getKey_market_info_marketid)
		time_of_collection = self.time_cryptsy.Unix_epoch

		data_pricechart = []
		newRecentTrades = []
		data_orderbook = []

		Totaltrades_count = 0
		TotalDiscarded = 0

		for each_market in market_info:
			marketid = each_market[0]
			market_label = each_market[1]
			temporarylist = []
			newtrades=0
			""" Query the `markets` table to get the corresponding id """
			try:
				corrsponding_id = self.marketlable["%s"%market_label];
			except KeyError:
				corrsponding_id = self.cryptsy_database_instance.query_table_markets_to_get_the_id\
								(each_market[0],each_market[1])
				self.marketlable["%s"%market_label] = corrsponding_id


			if (corrsponding_id == None):
				print("New trading pair detected: Market id: %s  Market label: %s"\
					%(marketid,market_label))
				print("Stating to update the `markets` Table in the database ...", end='\n')
				data = (each_market[0],'%s'%each_market[1],'%s'%each_market[7],'%s'%each_market[5],\
					'%s'%each_market[8],'%s'%each_market[6])
				print (data)
				self.cryptsy_database_instance.insert_data_into_markets(data)
				corrsponding_id = self.cryptsy_database_instance.query_table_markets_to_get_the_id\
								(each_market[0],each_market[1])
				print("corrsponding_id:  %d"%corrsponding_id)
				if (corrsponding_id == None):
					raise Exception("Failed to locate the new market added into the database")
				print("Insertion of new trading pair into `markets` Completed.")

			
			print ("Loading recenttrades of ", each_market[1], ";  Cryptcy Market id: ", each_market[0])
			recent_trades = self.return_recent_trades_as_a_list(market_label)


			for each_trade in recent_trades:
				Totaltrades_count += 1
				tx_id = each_trade[0]
				found = False
				for ii in range(0,len(self.temporaryHold['%d'%corrsponding_id])):
					i = self.temporaryHold['%d'%corrsponding_id][ii]
					if (tx_id==i[0]):
						found = True
						i[1] = 1
						break

				if (found==False):
					self.temporaryHold['%d'%corrsponding_id].append([tx_id,1])
					newtrades+=1
					newRecentTrades.append((corrsponding_id, tx_id, each_trade[1],'%s'%each_trade[2],\
							each_trade[3], each_trade[4], each_trade[5]))


			noDiscarded = 0
			print("Processing temporaryHold...")
			for i in range(0,len(self.temporaryHold['%d'%corrsponding_id])):
				if (self.temporaryHold['%d'%corrsponding_id][i][1] == 1):
					self.temporaryHold['%d'%corrsponding_id][i][1] = 0
					temporarylist.append(self.temporaryHold['%d'%corrsponding_id][i])
				else:
					noDiscarded += 1
					pass
			TotalDiscarded = noDiscarded + TotalDiscarded
			self.temporaryHold['%d'%corrsponding_id] = temporarylist

			print ("temporaryHold: ",len(self.temporaryHold['%d'%corrsponding_id]),\
				"No.of elements discarded: ",noDiscarded,sep='\n')
			print ('New trades : ', newtrades)

			""" Insert data into the `orderbook` table """

			buy_order = self.return_buy_orders_as_a_list(market_label= market_label)
			sell_order = self.return_sell_orders_as_a_list(market_label= market_label)
			
			print ("Loading buy orders of ", each_market[1], ";  Cryptcy Market id: ", each_market[0])
			for each_buy_order in buy_order:
				data_orderbook.append((corrsponding_id,'buy',each_buy_order[0],each_buy_order[1],each_buy_order[2],time_of_collection))
			
			print ("Loading sell orders of ", each_market[1], ";  Cryptcy Market id: ", each_market[0])
			for each_sell_order in sell_order:
				data_orderbook.append((corrsponding_id,'sell',each_sell_order[0],each_sell_order[1],each_sell_order[2],time_of_collection))

			"""Insert data into the `pricechart` table"""
			print("Collecting price,volume ...")
			data_pricechart.append((corrsponding_id, each_market[2],each_market[4],each_market[3],time_of_collection))
			print ("Collecting data for Market %s Completed!"% market_label)

			print("\n\n")


		print ("===============================")			
		print ("newRecentTrades: ",len(newRecentTrades))
		print ("TotalDiscarded",TotalDiscarded)
		print ("Total_recenttrades_count: ",Totaltrades_count)
		print ("Writing pricechart, newRecentTrades,orderbook")
		
		T= int(ceil(len(newRecentTrades)/10000.0))
		for i in range(int(0),T):
			self.cryptsy_database_instance.insert_data_into_recenttrades\
													(newRecentTrades[i*10000:(i+1)*10000-1])
		T= int(ceil(len(data_pricechart)/10000.0))
		for i in range(int(0),T):
			self.cryptsy_database_instance.insert_data_into_pricechart\
													(data_pricechart[i*10000:(i+1)*10000-1])

		T= int(ceil(len(data_orderbook)/10000.0))
		for i in range(int(0),T):
			self.cryptsy_database_instance.insert_data_into_orderbook\
													(data_orderbook[i*10000:(i+1)*10000-1])
																								

		print ()
		print ("\n\n\n")
		
		
if __name__ == '__main__':
	interval = 300
	buffer_left = 17
	buffer_right = 60
	precision = 0.5
	logfile=open('log.log','a')


	"""
	a = Cryptsy(settings)
	start = time.time()
	a.debug_Import_json_object(1433655915)
	a.process()
	print ("Execution Time:", time.time()-start)
	a.debug_Import_json_object(1433655915)
	a.process()
	print ("Execution Time:", time.time()-start)
	"""

	a = Cryptsy(settings)
	while True:
		try:
			mod_time = time.time()%interval
			EXCEXUTED = False
			if ((mod_time>=interval-buffer_left)or(mod_time<buffer_right))and(not(EXCEXUTED)):
				EXCEXUTED = True
				#############################
				start = time.time()
				try:
					a.json_Obj_Update()
					while (a.json_obj['return'] == False):
						print ("Waiting for 60s before the next attempt ...")
						time.sleep(60)
						a.json_Obj_Update()
					a.process()
					print ("Execution Time:", time.time()-start)
				except Exception as e:
					logfile.write(str(datetime.datetime.now()))
					logfile.write('     ')
					a.Save_json_object()
					logfile.write(str(e))
					logfile.write('\n')
					pass
				##############################
				while ((mod_time>=interval-buffer_left)or(mod_time<buffer_right)):
					mod_time = time.time()%interval
					time.sleep(precision)
			else:
				EXCEXUTED = False
				time.sleep(precision)
		except Exception as e:
				logfile.write(str(datetime.datetime.now()))
				logfile.write('     ')
				logfile.write(str(e))
				logfile.write('\n')
				a.Save_json_object()
				pass