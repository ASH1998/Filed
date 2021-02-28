import requests


#insertion

# # songs
# # audioFileType= 1
# # audioFileMeta={'name':'hellotestsong', 'duration':1232, 'uploadtime' : '2021-02-26'}

# #podcast
# # audioFileType= 2
# # audioFileMeta={'name':'hellotestsong2', 'duration':1232, 'uploadtime' : '2021-02-26', 'host': 'testhost', 'participants': ['one1', 'two2', 'three3']}

# #audiobook
# audioFileType= 3
# audioFileMeta={'name':'hellotestsong3', 'duration':123223, 'uploadtime' : '2021-02-27', 'author': 'testauthor', 'narrator': 'myoldnarrator'}


# gotRequest = requests.post('http://localhost:9000/create', 
# json={'audioFileType':str(audioFileType), 'audioFileMeta': audioFileMeta})

# print(gotRequest.text, gotRequest.status_code)

#------------------------------------------------------------------------------------------------------------------------

# updation

# songs
# audioFileType= 1
# audioFileMeta={'name':'hellotestsong', 'duration':1232, 'uploadtime' : '2021-02-26'}

#podcast
# audioFileType= 2
# audioFileMeta={'name':'hellotestsong2', 'duration':1232, 'uploadtime' : '2021-02-26', 'host': 'testhost', 'participants': ['one1', 'two2', 'three3']}

#audiobook
audioFileType= '3'
fileid='15'
audioFileMeta={'name':'hellotestsong3', 'duration':215, 'uploadtime' : '2021-03-26', 'author': 'testauthorupoader22', 'narrator': 'myoldnarrator22'}


gotRequest = requests.post('http://localhost:9000/update/{}/{}'.format(audioFileType, fileid), 
json={'audioFileType':str(audioFileType), 'audioFileMeta': audioFileMeta})

print(gotRequest.text, gotRequest.status_code)