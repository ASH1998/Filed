# Audio Server
This is a flask API that simulates an Audio Server.

# Dependencies
Install all dependencies using conda.                       
Requirements File : [environment.yml]          
`conda env create -f environment.yml`

# Usage

### Getting the DataBase ready
1. XAMPP was used for the DB (SQL MariaDB).             
2. The file is attached in [`DB/filed.sql`] (This can be executed directly to create the same schema).        

### DataBase Structure
1. Schema Name : file
2. filetype : mapper table, 1 - songs, 2 - podcast, 3 - audiobook           
3. file : mapping table. This table has all the information stored for all types of files.      
The Column `ftype` has values 1,2 or 3; this connects file to filetype.

### Directory Structure
0. [config.json] - main json file with all the credentials to the DB.           
1. API code is [main.py] in the directory called `src/`       
2. Test Files are in `test/`                
3. `DB/` directory contains the DB and schema and tables information.    
4. [main.py] is the main server.            
5. [audioServer.py] is the main class containing all the implementations and restrictions from  the instructions.           
6. [LogFile.log] stores all the logs, infos and Error messages.   
7. `test` directory has all the tests that makes sure the essential end points are working.            


### Starting the API
1. `cd src`
2. `python main.py`

### Testinf the API 
1. `cd src`
2. `python main.py`
3. `cd ..`
4. `cd test`
5. `python test_validate.py`


### Routes
(These are to be used with their respective parameters as in requirements)       
1. Create : 'http://localhost:9000/create/'             
2. Update : 'http://localhost:9000/update/'                     
3. GET records : 'http://localhost:9000/get/'               
4. Delete : 'http://localhost:9000/delete/'             
5. Refresh Connection : 'http://localhost:9000/refreshconnection/'               
6. Sanity Check : 'http://localhost:9000/sanitycheck'               

### Simple Example Routes: 
1. Check if API is working : http://localhost:9000/sanitycheck
2. Get multiple Records : http://localhost:9000/get/2
3. Get single Record : http://localhost:9000/get/2
4. Invalid Request : http://localhost:9000/get/2.2
5. Download Test File : http://localhost:9000/downloadtestfile

### Status Codes 
1. 200 - OK
2. 400 - Invalid Request
3. 404 - No parameters
4. 500 - Internal Server Error

## Download the Instructions  [[Test File Download]](http://localhost:9000/downloadtestfile)                               
                     

## Images

### 1. File Type
![File Type](https://i.imgur.com/2PWX911.jpg)

### 2. File

![File Table](https://i.imgur.com/7MeJJOV.jpg)

### 3. Successful get 
![successfulget](https://i.imgur.com/nrSM9L5.jpg)