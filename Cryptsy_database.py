#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
import time

class cryptsy_database():

	def __init__(self,db_user,db_password,db_name,db_host='localhost',\
				port=3306,use_unicode=True,charset="utf8"):

		self.db_host = db_host
		self.db_user = db_user
		self.db_password= db_password
		self.db_name = db_name
		self.port = port
		self.use_unicode = use_unicode
		self.charset = charset
		self.database_config = {
			'host':db_host, 
			'user':db_user, 
			'password':db_password,
			'port':port,
			'use_unicode':use_unicode,
			'charset':charset,
		}
		self.Mysql_instance = self.connect_to_Mysql_and_retuen_the_instance()
		print ("Connected to the Database successfully.")
		self.db_cursor = self.Mysql_instance.cursor()
		print ("Cursor Created.","Starting to connect the Database ...",sep="\n")
		self.connect_to_database()  # cursor will be set to the database
		print ("Successful connected to database: %s ; %s @ %s"%(self.db_name,self.db_user,self.db_host))
		print ("Initialisation Complete.")
	def __del__ (self):
		self.db_cursor.close()
		self.Mysql_instance.close()
		print ("Destructor invoked: Mysql_instance and db_cursor closed")
	def connect_to_Mysql_and_retuen_the_instance(self):
		"""
		return the connection object
		cnx = connect_to_database(database_config)
		"""
		try:
			self.cnx = mysql.connector.connect(**self.database_config)
			#Comprehensive List of arguments:
			#http://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
		except mysql.connector.Error as err:
			#handle connection errors
			print ("Error code:", err.errno)        # error number
			print ("SQLSTATE value:", err.sqlstate) # SQLSTATE value
			print ("Error message:", err.msg)       # error message
			print ("Error:", err)                   # errno, sqlstate, msg values
			raise Exception(str(err))  
		else:
			return self.cnx
	def connect_to_database(self):
		try:
			self.Mysql_instance.database = self.db_name #Try to connect to the specified database
		except mysql.connector.Error as err:   #Exception Handling
			if err.errno == errorcode.ER_BAD_DB_ERROR: #If the databse  does not exist
				try:
					print ("Database does not exist. The system will create a new database ...")
					self.create_new_database()
					self.Mysql_instance.database = self.db_name
					self.detect_a_new_machine()
				except:
					raise
			else:
				raise
	def create_new_database(self):
		try:
			#Create a database
			self.db_cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.db_name))
		except mysql.connector.Error as err: #Exception Handling
			raise Exception("Failed creating database: {}".format(err))
		else:
			print ("Database '{}' created successfully".format(self.db_name), end='\n')	
			self.Mysql_instance.database = self.db_name

	def detect_a_new_machine(self):
		create_table = [] # Python Dictionary Delcaration
		#Table markets
		create_table.append(["markets",(
			"CREATE TABLE `markets` ("
			"  `id` INT(50) NOT NULL AUTO_INCREMENT,"
			"  `marketid` INT(50),"
			"  `label` VARCHAR(50) CHARACTER SET utf8,"
			"  `primaryname` VARCHAR(100) CHARACTER SET utf8,"
			"  `primarycode` VARCHAR(100) CHARACTER SET utf8,"
			"  `secondaryname` VARCHAR(100) CHARACTER SET utf8,"
			"  `secondarycode` VARCHAR(100) CHARACTER SET utf8,"
			"  PRIMARY KEY (`id`),"
			"  INDEX (`marketid`) ,"
			"  INDEX (`label`), "
			"  INDEX (`primaryname`) ,"
			"  INDEX (`primarycode`) ,"
			"  INDEX (`secondaryname`), "
			"  INDEX (`secondarycode`) "
			") ENGINE=InnoDB, ROW_FORMAT=COMPRESSED")])

		
		#Table recenttrades
		create_table.append(["recenttrades",(
		    "CREATE TABLE `recenttrades` ("
		    "  `id` BIGINT(50) NOT NULL AUTO_INCREMENT,"
		    "  `id_corresponding_to_that_in_markets_table` INT(50),"
		    "  `tx_id` BIGINT(50) ,"
		    "  `time` INT(50) UNSIGNED,"
		    "  `type` VARCHAR(10) CHARACTER SET utf8,"
		    "  `price` DECIMAL(30,15) ,"
		    "  `quantity` DECIMAL(30,15) ,"
		    "  `total` DECIMAL(30,15) ,"
		    "  PRIMARY KEY (`id`),"
		    "  INDEX (`id_corresponding_to_that_in_markets_table`), "
		    "  INDEX (`time`), "
		    "  FOREIGN KEY fk_id(id_corresponding_to_that_in_markets_table)   REFERENCES markets(id)   ON UPDATE RESTRICT   ON DELETE CASCADE"
		    ") ENGINE=InnoDB, ROW_FORMAT=COMPRESSED")])

		#Table orderbook
		create_table.append(["orderbook",(
		    "CREATE TABLE `orderbook` ("
		    "  `id` BIGINT(50) NOT NULL AUTO_INCREMENT,"
		    "  `id_corresponding_to_that_in_markets_table` INT(50),"
		    "  `type` VARCHAR(15) CHARACTER SET utf8,"
		    "  `price` DECIMAL(30,15) ,"
		    "  `total` DECIMAL(30,15),"
		    "  `quantity` DECIMAL(30,15) ,"
		    "  `time_of_collection` INT(50) UNSIGNED,"
		    "  PRIMARY KEY (`id`),"
		    "  INDEX (`id_corresponding_to_that_in_markets_table`), "
		    "  INDEX (`time_of_collection`), "
		    "  FOREIGN KEY fk_id(id_corresponding_to_that_in_markets_table)   REFERENCES markets(id)   ON UPDATE RESTRICT   ON DELETE CASCADE"
		    ") ENGINE=InnoDB, ROW_FORMAT=COMPRESSED")])

		#Table pricechart
		create_table.append(["pricechart",(
		    "CREATE TABLE `pricechart` ("
		    "  `id` BIGINT(50) NOT NULL AUTO_INCREMENT,"
		    "  `id_corresponding_to_that_in_markets_table` INT(50),"
		    "  `lasttradeprice` DECIMAL(30,15),"
		    "  `lasttradetime` INT(50) UNSIGNED ,"
		    "  `volume` DECIMAL(30,15),"
		    "  `time_of_collection` INT(50) UNSIGNED,"
		    "  INDEX (`id_corresponding_to_that_in_markets_table`) ,"
		    "  INDEX (`time_of_collection`) ,"
		    "  PRIMARY KEY (`id`),"
		    "   FOREIGN KEY fk_id(id_corresponding_to_that_in_markets_table)   REFERENCES markets(id)   ON UPDATE RESTRICT   ON DELETE CASCADE"
		    ") ENGINE=InnoDB, ROW_FORMAT=COMPRESSED")])
		

		self.create_table(create_table)

	def create_table(self, LIST_tables):
		""" Pass in a Dictionary """
		self.db_cursor.execute("SET GLOBAL innodb_file_per_table=1")
		self.db_cursor.execute("SET GLOBAL innodb_file_format=Barracuda")
		
		for each_table in LIST_tables:
			try:
				self.db_cursor.execute(each_table[1])
			except mysql.connector.Error as err:
				if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
					print("Table {} already exists.".format(each_table[0]))
				else:
					print("Creating Table {} Failed: ".format(each_table[0]), err.msg)
			else:
				print("Table {} Created.".format(each_table[0]))

	def query_table_markets_to_get_the_id(self,marketid,label):
		query = ("SELECT id FROM markets"
				" WHERE marketid= %s AND label= %s")
		self.db_cursor.execute(query, (int(marketid), str(label)))

		temp = self.db_cursor.fetchone()
		if not(temp):
			return temp
		output = int(temp[0])

		try:
			temp_temp = self.db_cursor.fetchone()
			if not(temp_temp==None):
				raise Exception("Alert: (query_table_markets_to_get_the_id) Found more than"
								" one result in the response")
		except Exception as e:
			print (e,":")
			print (("`id` returned: %d")%output)
			print ("Other Results: ", temp_temp, sep="\n")
			try:
				print (self.db_cursor.fetchall())
			except:
				pass
			finally:
				print("\n")
		finally:
			return output

	def loading_information_into_the_database(self,type_of_data,data,market_label,market_id):


		if (type_of_data == 'recenttrades'):
			"""check if the id is duplicate if so not insert"""
			pass
		elif (type_of_data == 'buyorders'):
			pass
		elif (type_of_data == 'sellorders'):
			pass
		else:
			raise Exception("In loading_information_into_the_database: Wrong Type %s"%type_of_data)
		


	def insert_data_into_markets(self,data):
		insertion_format = ("INSERT INTO markets"
					"(marketid, label, primaryname, primarycode, secondaryname, secondarycode)"
					"VALUES (%s,%s,%s,%s,%s,%s)"
					)

		self.db_cursor.execute(insertion_format,data)
		self.Mysql_instance.commit()

	def insert_data_into_recenttrades(self,data):
		insertion_format = ("INSERT INTO recenttrades"
							"(id_corresponding_to_that_in_markets_table, tx_id, time, type, price, quantity, total)"
							"VALUES (%s,%s,%s,%s,%s,%s,%s)"
							)
		self.db_cursor.executemany(insertion_format,data)
		self.Mysql_instance.commit()
	def insert_data_into_orderbook(self,data):
		insertion_format = ("INSERT INTO orderbook"
					"(id_corresponding_to_that_in_markets_table, type, price, total, quantity, time_of_collection)"
					"VALUES (%s,%s,%s,%s,%s,%s)"
					)

		self.db_cursor.executemany(insertion_format,data)
		self.Mysql_instance.commit()
	def insert_data_into_pricechart(self,data):

		insertion_format = ("INSERT INTO pricechart"
					"(id_corresponding_to_that_in_markets_table, lasttradeprice, lasttradetime, volume, time_of_collection)"
					"VALUES (%s,%s,%s,%s,%s)"
					)

		self.db_cursor.executemany(insertion_format,data)
		self.Mysql_instance.commit()
	def query_table_recenttrades_to_check_if_tx_id_exists(self,tx_id,id_corresponding_to_that_in_markets_table):
		"""exist->TRUE  ||  not exist->False"""

		query = ("SELECT id FROM recenttrades"
				" WHERE tx_id= %s AND id_corresponding_to_that_in_markets_table= %s")
		self.db_cursor.execute(query, (int(tx_id), int(id_corresponding_to_that_in_markets_table)))
		 
		if (self.db_cursor.fetchone()==None):
			return False
		else:
			try:
				print ('#######',self.db_cursor.fetchall())
			except:
				pass
			return True

if __name__ == '__main__':
	#Unit TEST : Creating Tables
	a= cryptsy_database("root", "root","cryptsy_database")
	del(a)


