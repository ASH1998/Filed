from audioServer import Filed

filed = Filed('config.json')
cursor = filed.getCursor()
audioupload = {"name":'rec1', "duration":10, "uploadtime":filed.currentdatetime }
filed.insertsinglerecord(cursor, audiofile=audioupload, recordtype=1)
filed.deleteSingleRecord(cursor, '3')
filed.showRecords(cursor )
print('-'*20)
filed.showRecords(cursor, ftype=1)
print('-'*20)
filed.showRecords(cursor, ftype=2)

cursor = filed.closeConnection(cursor)