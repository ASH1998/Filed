import sys
import logging
import requests
logging.basicConfig( stream=sys.stderr )
import unittest
import datetime
import json

class AudioServerTest(unittest.TestCase):
    
    def returnRoutes(self):
        return ['http://localhost:9000/create/', 'http://localhost:9000/update/', 'http://localhost:9000/get/', 
                'http://localhost:9000/delete/', 'http://localhost:9000/sanitycheck', 'http://localhost:9000/refreshconnection/']

    def test_api(self):
        sanitycheck = self.returnRoutes()[4]
        gotRequest = requests.post(sanitycheck)
        statuscode = gotRequest.status_code
        text = gotRequest.text

        self.assertEqual(statuscode, 200)
        self.assertEqual(text, "App Working")

    def test_updateRecords(self):
        audioFileType= '3'
        fileid='15'
        newuploadtime = datetime.datetime.now()
        audioFileMeta={'name':'hellotestsong3', 'duration':123223, 'uploadtime' : str(newuploadtime), 'author': 'testauthorupoader', 'narrator': 'myoldnarrator'}
        gotRequest = requests.post('http://localhost:9000/update/{}/{}'.format(audioFileType, fileid), json={'audioFileType':str(audioFileType), 'audioFileMeta': audioFileMeta})
        statuscode = gotRequest.status_code

        self.assertEqual(statuscode, 200)

    def test_pastddate(self):
        audioFileType= '3'
        fileid='15'
        newuploadtime = datetime.datetime.now() - datetime.timedelta(days=4)
        audioFileMeta={'name':'hellotestsong3', 'duration':123223, 'uploadtime' : str(newuploadtime), 'author': 'testauthorupoader', 'narrator': 'myoldnarrator'}
        gotRequest = requests.post('http://localhost:9000/update/{}/{}'.format(audioFileType, fileid), json={'audioFileType':str(audioFileType), 'audioFileMeta': audioFileMeta})
        statuscode = gotRequest.status_code

        self.assertEqual(statuscode, 400)
    
    def test_futureDate(self):
        audioFileType= '3'
        fileid='15'
        newuploadtime = datetime.datetime.now() + datetime.timedelta(days=20)
        audioFileMeta={'name':'hellotestsong3', 'duration':123223, 'uploadtime' : str(newuploadtime), 'author': 'testauthorupoader', 'narrator': 'myoldnarrator'}
        gotRequest = requests.post('http://localhost:9000/update/{}/{}'.format(audioFileType, fileid), json={'audioFileType':str(audioFileType), 'audioFileMeta': audioFileMeta})
        statuscode = gotRequest.status_code

        self.assertEqual(statuscode, 200)

    def test_getSingleRecord(self):
        gotRequest = requests.post(self.returnRoutes()[2]+'1/1')
        statuscode = gotRequest.status_code
        try:
            result = json.loads(gotRequest.text)
        except:
            # raise assert error if results are not in json
            assert 4==5

        self.assertEqual(statuscode, 200)
        self.assertEqual(type(result), dict)

    def test_getMultipleRecord(self):
        gotRequest = requests.post(self.returnRoutes()[2]+'3')
        statuscode = gotRequest.status_code
        try:
            result = json.loads(gotRequest.text)
        except:
            # raise assert error if results are not in json
            assert 4==5

        self.assertEqual(statuscode, 200)
        self.assertEqual(type(result), dict)

    def test_deleteRecord(self):
        gotRequest = requests.post(self.returnRoutes()[3]+'1/1')
        statuscode = gotRequest.status_code
        result = gotRequest.text

        self.assertEqual(statuscode, 200)
        self.assertEqual(type(result), str)

    def test_deleteInvalidRecord(self):
        gotRequest = requests.post(self.returnRoutes()[3]+'10000000/1')
        statuscode = gotRequest.status_code
        result = gotRequest.text

        self.assertEqual(statuscode, 400)
        self.assertEqual(result, "INVALID REQUEST")
    
    def test_deleteInvalidRecord(self):
        gotRequest = requests.post(self.returnRoutes()[3]+'10000000')
        statuscode = gotRequest.status_code

        self.assertEqual(statuscode, 404)
    
    def test_create(self):
        audioFileType= 3
        newuploadtime = datetime.datetime.now()
        audioFileMeta={'name':'hellotestsong3', 'duration':562, 'uploadtime' : str(newuploadtime), 'author': 'testauthor', 'narrator': 'myoldnarrator'}
        gotRequest = requests.post('http://localhost:9000/create', 
        json={'audioFileType':str(audioFileType), 'audioFileMeta': audioFileMeta})

        self.assertEqual(gotRequest.status_code, 200)
    
    def test_Invalidcreate(self):
        audioFileType= 344
        newuploadtime = datetime.datetime.now()
        audioFileMeta={'name':'hellotestsong3', 'duration':562, 'uploadtime' : str(newuploadtime), 'author': 'testauthor', 'narrator': 'myoldnarrator'}
        gotRequest = requests.post('http://localhost:9000/create', 
        json={'audioFileType':str(audioFileType), 'audioFileMeta': audioFileMeta})

        self.assertEqual(gotRequest.status_code, 400)


if __name__=="__main__":
    unittest.main()
