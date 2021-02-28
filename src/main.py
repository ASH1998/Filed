import datetime
from exceptionUtils import DBError
from flask import Flask, request, jsonify, send_file
import markdown
import traceback

import logging
logging.basicConfig(filename='LogFile.log', level=logging.INFO)

import sys
sys.path.append('/static')
# import requests

from audioServer import Filed

app = Flask(__name__)

# start the audio server providing the config file 
fileobject = Filed('config.json')
# get the connection going and the cursor
cursor = fileobject.getCursor()
if cursor==False:
    logging.error("DB connection failed, check DB credentials in config.json")
    # raise DBError

@app.route("/sanitycheck", methods=['POST', 'GET'])
def sanity():
    '''checks if the app is up'''
    logging.info("sanity check started")
    return "App Working", 200

@app.route("/")
def index():
    '''main index page, shows the markdown'''
    readme_file = open("../README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    return md_template_string, 200

@app.route('/downloadtestfile')
def show_static_pdf():
    '''downloading and viewing the test file'''
    with open(r'static/Python_Test 2021.pdf', 'rb') as static_file:
        return send_file(static_file, attachment_filename='Test.pdf')

@app.route('/get/<audioFileType>', methods=["POST", "GET"])
def getAllRecords(audioFileType):
    '''showing all records of a single type'''
    try:
        # checking if type is correct
        if 'song' in str(audioFileType).lower():
            audioFileType = 1
        elif 'podcast' in str(audioFileType).lower():
            audioFileType = 2
        elif 'audiobook' in str(audioFileType).lower():
            audioFileType = 3
        else:
            if len(str(audioFileType))>1:
                return "INVALID REQUEST", 400
            if int(audioFileType)>3:
                return "INVALID REQUEST", 400

        # getting records
        records = fileobject.showRecords(cursor, int(audioFileType), recordid=None)
        return jsonify({"records" : records}), 200
    except Exception as e:
        logging.error(traceback.format_exc())
        return "Internal Server Error", 500

@app.route('/get/<audioFileType>/<audioFileID>', methods=["POST", "GET"])
def getSingleTypeRecord(audioFileType, audioFileID):
    '''get a single instance of a type'''
    try:
        #check audio type
        if 'song' in str(audioFileType).lower():
            audioFileType = 1
        elif 'podcast' in str(audioFileType).lower():
            audioFileType = 2
        elif 'audiobook' in str(audioFileType).lower():
            audioFileType = 3
        else:
            if len(str(audioFileType))>1:
                return "INVALID REQUEST", 400
            if int(audioFileType)>3:
                return "INVALID REQUEST", 400

        # get one single record with id
        records = fileobject.showRecords(cursor, int(audioFileType), recordid=int(audioFileID))
        return jsonify({"records" : records}), 200
    except Exception as e:
        logging.error(traceback.format_exc())
        return "Internal Server Error", 500
	

@app.route('/delete/<audioFileType>/<audioFileID>', methods=["POST", "GET"])
def deletesingleRecord(audioFileType, audioFileID):
    '''delete a single record'''
    try:
        # check audio type
        if 'song' in str(audioFileType).lower():
            audioFileType = 1
        elif 'podcast' in str(audioFileType).lower():
            audioFileType = 2
        elif 'audiobook' in str(audioFileType).lower():
            audioFileType = 3
        else:
            if len(str(audioFileType))>1:
                return "INVALID REQUEST", 400
            if int(audioFileType)>3:
                return "INVALID REQUEST", 400

        # delete a single record
        fileobject.deleteSingleRecord(cursor, audioFileType, audioFileID)
        return """Deletion of record : {} from Audio file type : {} is complete.""".format(audioFileID, audioFileType), 200
    except Exception as e:
        logging.error(traceback.format_exc())
        return "Internal Server Error", 500

@app.route('/create', methods=['POST'])
def createSingle():
    '''create a single record, all meta data is to be provided as json'''
    if request.method == "POST":
        data = {}
        success = 0
        # initialise null values, if it is song
        host = participants = author = narrator = None
        postrequest = (request.get_json())
        if postrequest['audioFileType']:
            audioFileType = postrequest['audioFileType']
            meta = postrequest['audioFileMeta']

            # if str(audioFileType)=='1':
            name =  meta['name']
            duration = meta['duration']
            uploadtime = meta['uploadtime']

            if str(audioFileType) == '2':
                host = meta['host']
                if 'participants' in meta:
                    participants = meta['participants']
            
            if str(audioFileType) == '3':
                author = meta['author']
                narrator = meta['narrator']

            data = {"name": name, 
                    "duration": duration, 
                    "uploadtime":uploadtime, 
                    "host" : host,
                    "participants" : participants,
                    "author" : author,
                    "narrator" : narrator,
                    "success": success, 
                    "audioFileType":audioFileType}
            
            # check the sanity of data, if the data is within contraints
            sanityScore = fileobject.checkDataSanity(data)

            if sanityScore==1:
                # insert single record
                boolval = fileobject.insertsinglerecord(cursor, data, data['audioFileType'])
                if boolval:
                    data['success'] = 1
                    print(name, duration, uploadtime)
                else:
                    return "Internal Server Error", 500
            else:
                return "BAD REQUEST", 400
    if data['success']==0:
        return data, 500
    return data, 200

@app.route('/update/<audioFileType>/<audioFileID>', methods=['POST'])
def uploadSingle(audioFileType, audioFileID):
    '''update a single record'''
    if request.method == "POST":
        data = {}
        success = 0
        
        host = participants = author = narrator = None
        postrequest = (request.get_json())
        if postrequest['audioFileMeta']:
            audioFileType = int(audioFileType)
            # check audio type
            if 'song' in str(audioFileType).lower():
                audioFileType = 1
            elif 'podcast' in str(audioFileType).lower():
                audioFileType = 2
            elif 'audiobook' in str(audioFileType).lower():
                audioFileType = 3
            else:
                if len(str(audioFileType))>1:
                    return "INVALID REQUEST", 400
                if int(audioFileType)>3:
                    return "INVALID REQUEST", 400

            audiofileid = int(audioFileID)
            meta = postrequest['audioFileMeta']

            name =  meta['name']
            duration = meta['duration']
            uploadtime = meta['uploadtime']

            # check the type of file
            if str(audioFileType) == '2':
                host = meta['host']
                if 'participants' in meta:
                    participants = meta['participants']
            
            if str(audioFileType) == '3':
                author = meta['author']
                narrator = meta['narrator']

            data = {"name": name, 
                    "duration": duration, 
                    "uploadtime":uploadtime, 
                    "host" : host,
                    "participants" : participants,
                    "author" : author,
                    "narrator" : narrator,
                    "success": success, 
                    "audioFileType":audioFileType, 
                    "audioFileID": audiofileid}

            #checking thr sanity of the data
            sanityScore = fileobject.checkDataSanity(data)

            if sanityScore==1:
                # updation of the data
                boolval = fileobject.updatesinglerecord(cursor, data, data['audioFileType'])
                if boolval==1:
                    data['success'] = 1
                    print(name, duration, uploadtime)
                else:
                    return "Internal Server Error", 500
            else:
                return "BAD REQUEST", 400
    if data['success']==0:
        return data, 500
    return data, 200

@app.route('/refreshconnection',  methods=["POST", "GET"])
def refreshConnection():
    # if on connection error, this can be used to refresh the connection.
    global cursor
    cursor = fileobject.closeConnection(cursor)
    cursor = fileobject.getCursor()
    if cursor==False:
        logging.error("DB connection failed, check DB creadentials in config.json")
        return "DB Error, check credentials.", 500
    logging.info("Connection Refreshed...")
    return "Connection Restarted", 200

if __name__ == "__main__":
    logging.info("Processing started at : " + str(datetime.datetime.now()))
    try:
        app.run(debug=True, port=9000)
        app.testing=True
    except RuntimeError:
        print("SERVER IS SHUTTING DOWN.")
    