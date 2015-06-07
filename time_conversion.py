# -*- coding: utf-8 -*-
#!/usr/bin/python

import time,calendar

"""
class time.struct_time:

Index        Attribute	                 Values
	0	         tm_year	            (for example, 1993)
	1	         tm_mon	                range [1, 12]
	2	         tm_mday	            range [1, 31]
	3	         tm_hour	            range [0, 23]
	4	         tm_min	                range [0, 59]
	5	         tm_sec	                range [0, 61]; see (2) in strftime() description
	6	         tm_wday	            range [0, 6], Monday is 0
	7	         tm_yday	            range [1, 366]
	8	         tm_isdst	            0, 1 or -1; see below
 N/A	     tm_zone	            abbreviation of timezone name
 N/A	     tm_gmtoff	            offset east of UTC in seconds

 ==============================================================
 ==============================================================
 
Directive	            Meaning	Notes
	 %a	     Locale's abbreviated weekday name.	 
	 %A	     Locale's full weekday name.	 
	 %b	     Locale's abbreviated month name.	 
	 %B	     Locale's full month name.	 
	 %c	     Locale's appropriate date and time representation.	 
	 %d	     Day of the month as a decimal number [01,31].	 
	 %H	     Hour (24-hour clock) as a decimal number [00,23].	 
	 %I	     Hour    (12-hour clock) as a decimal number [01,12].	 
	 %j	     Day of the year as a decimal number [001,366].	 
	 %m	     Month as a decimal number [01,12].	 
	 %M	     Minute as a decimal number [00,59].	 
	 %p	     Locale's equivalent of either AM or PM.	(1)
	 %S	     Second as a decimal number [00,61].	(2)
	 %U	     Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. 
						 All days in a new year preceding the first Sunday are considered to be in week 0.	
	 %w	     Weekday as a decimal number [0(Sunday),6].	 
	 %W	     Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. 
						 All days in a new year preceding the first Monday are considered to be in week 0.	
	 %x	     Locale's appropriate date representation.	 
	 %X	     Locale's appropriate time representation.	 
	 %y	     Year without century as a decimal number [00,99].	 
	 %Y	     Year with century as a decimal number.	 
	 %z	     Time zone offset indicating a positive or negative time difference from UTC/GMT of the form 
						 +HHMM r -HHMM, where H represents decimal hour digits and M represents decimal minute digits 
						 [-23:59, +23:59].	 
	 %Z	     Time zone name (no characters if no time zone exists).	 
	 %%	     A literal '%' character.	 

"""

time_zone_offset_for_singapore = +8
time_zone_offset_for_EST =-5
output_format_string = "%d %b %Y %H:%M:%S"


class time_cryptsy():
		def __init__(self):
			self.UTC_time = time.gmtime(time.time())
			self.local_time =time.localtime(time.time())
			self.Unix_epoch = time.time()

		def update(self):
			self.UTC_time = time.gmtime(time.time())
			self.local_time =time.localtime(time.time())
			self.Unix_epoch = time.time()

		def get_Unix_epoch_time_UTC(self):
			""" Return type: Float e.g.1418823700.309625 """
			return self.Unix_epoch

		def strpi_time_to_Unix_Epoch_format_UTC(self,time_string="2014-12-15 22:05:25",\
												time_format="%Y-%m-%d %H:%M:%S",\
												time_zone_offset=-5): #e.g EST – Eastern Standard Time:-0500
																															#--> Pass in -5 only
																															#Check here: http://www.timeanddate.com/time/zones/
			"""Return: struct_time"""
			if (time_string=='None')or(time_string==''):
				return None
			temp_tuple = time.strptime(time_string,time_format)
			return int(calendar.timegm(temp_tuple)-(time_zone_offset*3600))

		def construct_time_UTC_from_Unix_epoch_time_format_UTC(self,Unix_time,format_string="%d %b %Y %H:%M:%S"):
			return str((time.strftime("%d %b %Y %H:%M:%S",time.gmtime(Unix_time))))

		def construct_time_LOCAL_from_Unix_epoch_time_format_UTC(self,Unix_time,\
																format_string="%d %b %Y %H:%M:%S",\
																time_zone_offset=+8):
			return str(time.strftime("%d %b %Y %H:%M:%S",time.gmtime(Unix_time+time_zone_offset*3600)))