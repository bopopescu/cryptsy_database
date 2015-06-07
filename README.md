**CryptsyData 1.0**
===================

This is a python program which collects data from Cryptsy Exchange and store them in MySQL database.

> **Data Collected:**

> - Price
> - Volume
> - Recent Trades
> - Order book snapshot




Database Schemas
-------------

![Schemas](https://github.com/lxjhk/cryptsy_database/blob/master/schemas.png?raw=true)



Documentation
-------------
#### <i class="icon-file"></i> How to run
 1. Set up your own MySQL database
 2. Change the configuration file **Settings.py**
 
```
    Settings = {
	"API_address": "http://pubapi.cryptsy.com/api.php?method=marketdatav2",
	"db_host": "localhost",
	"db_user": "USERNAME",
	"db_password": "PASSWORD",
	"db_port": 3306,
	"db_use_unicode": True,
	"charset": "utf8",
	"db_name":"cryptsy_database"
}
```
In the command prompt,
```
   python Cryptsy.py
```



License
-------------------
![MIT](http://opensource.org/trademarks/opensource/OSI-Approved-License-100x137.png)  **Under The MIT License (MIT)**


**Copyright (c) <2015> <lxjhk>**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.