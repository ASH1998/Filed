import json
from logging import exception
import mysql.connector
import datetime
from datetime import timedelta
from dateutil import parser

from exceptionUtils import *


class Filed:
    def __init__(self, config):
        # initialising all the variables
        self.config = config
        self.connection = None
        self.currentdatetime = datetime.datetime.now()
        self.pastdatetime = datetime.datetime.now() - timedelta(days=1)

        self.insertaudiobook = r'''
        INSERT into file(name, duration, uploadtime, author, narrator, ftype)
        VALUES(%s, %s, %s, %s, %s, 3)
        '''
        self.insertsong = r'''
        INSERT into file(name, duration, uploadtime, ftype)
        VALUES(%s, %s, %s, 1)
        '''
        self.insertpodcast = r'''
        INSERT into file(name, duration, uploadtime, host, participants, ftype)
        VALUES(%s, %s, %s, %s, %s, 2)
        '''
        self.deleterecord = r'''
        delete from file where id=%s and ftype=%s
        '''

        self.inserttest = r'''INSERT into file(name, duration, uploadtime, author, narrator, ftype)
                 VALUES("testfile4", 78754, now(), 'testingauthor', null, 3)'''
        
        self.updatesong = r'''
        update file set name=%s, duration=%s, uploadtime=%s, ftype=%s
        where id=%s
        '''
        self.updatepodcast = r'''
        update file set name=%s, duration=%s, uploadtime=%s, ftype=%s, host=%s, participants=%s
        where id=%s
        '''
        self.updateaudiobook = r'''
        update file set name=%s, duration=%s, uploadtime=%s, ftype=%s, author=%s, narrator=%s
        where id=%s
        '''

    def getCursor(self):
        '''connect with the DB'''
        try:
            params = json.load(open(self.config))
            self.connection = mysql.connector.connect(**params)
            cursor = self.connection.cursor()
            return cursor
        except Exception as e:
            print(e)
            return False

    def closeConnection(self, cursor):
        '''close the connection'''
        cursor.close()
        cursor = None
        self.connection = self.connection.close()
        return cursor

    @property
    def refreshDatetime(self, pastdate=2):
        '''refresh the date time'''
        self.currentdatetime = datetime.datetime.now()
        self.pastdatetime = datetime.datetime.now() - timedelta(days=pastdate)

    def checkpasttime(self, fdate):
        '''checking if the date is in past or not'''
        try:
            fdate = parser.parse(fdate)
            print("checking: " , fdate)
        except parser.ParserError:
            return False
        
        # print("current time : ", self.currentdatetime)
        # print("past time : ", self.pastdatetime)
        # print("timedelta : ", self.currentdatetime - fdate)
        # print("timedelta2 : ", self.currentdatetime-self.pastdatetime)
        # print("time threshold : ", self.currentdatetime-self.pastdatetime)

        # comparing dates
        if  self.currentdatetime - fdate < self.currentdatetime-self.pastdatetime:
            return True
        else:
            return False

    def getallData(self, cursor):
        cursor.execute(r"SELECT * FROM file")
        result = cursor.fetchall()
        return result

    def checkAudioData(self, **params):
        pass

    def insertsinglerecord(self, cursor, audiofile, recordtype=None): # *args, **kwargs):
        print("starting insertion...")
        
        if recordtype==None:
            raise FileNotFoundError
        
        if int(recordtype)==1:
            name = audiofile['name']
            duration = audiofile['duration']
            uploadtime = audiofile['uploadtime']
            # self.checkAudioData(name, duration, uploadtime)
            print(self.insertsong)
            cursor.execute(self.insertsong, (name, duration, uploadtime))
            self.connection.commit()
        
        elif int(recordtype)==2:
            name = audiofile['name']
            duration = audiofile['duration']
            uploadtime = audiofile['uploadtime']
            host = audiofile['host']
            participants = str(audiofile['participants'])
            # self.checkAudioData(name, duration, uploadtime)
            print(self.insertpodcast)
            cursor.execute(self.insertpodcast, (name, duration, uploadtime, host, participants))
            self.connection.commit()
        
        elif int(recordtype)==3:
            name = audiofile['name']
            duration = audiofile['duration']
            uploadtime = audiofile['uploadtime']
            author = audiofile['author']
            narrator = audiofile['narrator']
            # self.checkAudioData(name, duration, uploadtime)
            print(self.insertaudiobook)
            cursor.execute(self.insertaudiobook, (name, duration, uploadtime, author,  narrator))
            self.connection.commit()
        
        else:
            return False 

        return True

    def updatesinglerecord(self, cursor, audiofile, recordtype=None): # *args, **kwargs):
        '''updating a single record'''
        print("starting updation...")
        
        if recordtype==None:
            raise FileNotFoundError
        
        # song update
        if int(recordtype)==1:
            fileid = audiofile['audioFileID']
            name = audiofile['name']
            duration = audiofile['duration']
            uploadtime = audiofile['uploadtime']
            # self.checkAudioData(name, duration, uploadtime)
            cursor.execute(self.updatesong, (name, duration, uploadtime, recordtype, fileid))
            self.connection.commit()
        # podcast update
        elif int(recordtype)==2:
            fileid = audiofile['audioFileID']
            name = audiofile['name']
            duration = audiofile['duration']
            uploadtime = audiofile['uploadtime']
            host = audiofile['host']
            participants = str(audiofile['participants'])
            # self.checkAudioData(name, duration, uploadtime)
            cursor.execute(self.updatepodcast, (name, duration, uploadtime, recordtype, host, participants, fileid))
            self.connection.commit()
        # audio book update
        elif int(recordtype)==3:
            fileid = audiofile['audioFileID']
            name = audiofile['name']
            duration = audiofile['duration']
            uploadtime = audiofile['uploadtime']
            author = audiofile['author']
            narrator = audiofile['narrator']
            # self.checkAudioData(name, duration, uploadtime)
            cursor.execute(self.updateaudiobook, (name, duration, uploadtime, recordtype, author,  narrator, fileid))
            self.connection.commit()
        
        else:
            return 0

        return 1

    def deleteSingleRecord(self, cursor, ftype, deleteid) :
        '''delete a single record'''
        cursor.execute(self.deleterecord, (deleteid,ftype,) )
        self.connection.commit()

    def showRecords(self, cursor, ftype=None, recordid=None):
        '''showing of records of different audio types'''
        results = None
        # showing all records of a single audio type
        if recordid==None:
            if ftype==None:
                cursor.execute(r"SELECT * FROM file")
                results = cursor.fetchall()
            elif ftype==1:
                cursor.execute(r"SELECT id, name, duration, uploadtime FROM file where ftype=1")
                results = cursor.fetchall()
            elif ftype==2:
                cursor.execute(r"SELECT id, name, duration, uploadtime, host, participants FROM file where ftype=2")
                results = cursor.fetchall()
            elif ftype==3:
                cursor.execute(r"SELECT id, name, duration, uploadtime, author, narrator FROM file where ftype=3")
                results = cursor.fetchall()
            else:
                raise AudioTypeDoesNotExist
        else:
            # showing a specific id 
            if ftype==None:
                cursor.execute(r"SELECT * FROM file where id=%s", (recordid,))
                results = cursor.fetchall()
            elif ftype==1:
                cursor.execute(r"SELECT id, name, duration, uploadtime FROM file where ftype=1 and id=%s", (recordid,))
                results = cursor.fetchall()
            elif ftype==2:
                cursor.execute(r"SELECT id, name, duration, uploadtime, host, participants FROM file where ftype=2 and id=%s", (recordid,))
                results = cursor.fetchall()
            elif ftype==3:
                cursor.execute(r"SELECT id, name, duration, uploadtime, author, narrator FROM file where ftype=3 and id=%s", (recordid,))
                results = cursor.fetchall()
            else:
                raise AudioTypeDoesNotExist
        
        return results


    def checkDataSanity(self, data):
        '''checking if the request has valid data'''
        sanityscore = 0
        # check if necessary meta exists
        if all(_ in data for _ in ("audioFileType", "name", "duration", "uploadtime")):
            audiofiletype = data['audioFileType']
            name = data['name']
            duration = data['duration']
            uploadtime = data['uploadtime']
            host = data['host']
            participants = data['participants']
            author = data['author']
            narrator = data['narrator']

            # check if date is in past
            pasttime = self.checkpasttime(uploadtime)
            # checking lengths and duration type and duration positive
            if type(name)==str and len(name)<101 and type(duration)==int and duration>0 and pasttime:
                #check for songs
                if int(audiofiletype)==1:
                    sanityscore=1
                #check for podcast
                if int(audiofiletype)==2:
                    # host length and type
                    if type(host)==str and len(host)<101:
                        if participants!=None:
                            sanityscore=1
                        # participants type, length
                        elif type(participants)==list and len(participants)<11 and len(str(sorted(participants, key=len)[-1]))<101:
                            sanityscore=1
                        else:
                            sanityscore=0
                #check for audiobook
                if int(audiofiletype)==3:
                    if type(author)==str and len(author)<101 and type(narrator)==str and len(narrator)<101:
                        sanityscore=1

        else:
            return sanityscore

        return sanityscore



        
        







