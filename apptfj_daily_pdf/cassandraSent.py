import json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
import os
from InternalControl import cInternalControl

objControl=cInternalControl()
idControl=objControl.idControl
keyspace='test'
timeOut=objControl.timeout  

def returnCluster():
    #Connect to Cassandra
    objCC=CassandraConnection()
    cloud_config={}
    secure_connect_zip=''
    secure_zip='secure-connect-dbquart.zip'
    if objControl.heroku:
        secure_connect_zip=objControl.rutaHeroku+'/'+secure_zip
    else:
        secure_connect_zip= objControl.rutaLocal+secure_zip

    cloud_config['secure_connect_bundle']=secure_connect_zip
    cloud_config['init-query-timeout']=10 
    cloud_config['connect_timeout']=10 
    cloud_config['set-keyspace-timeout']=10            


    auth_provider = PlainTextAuthProvider(objCC.cc_user_test,objCC.cc_pwd_test)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider) 
    cluster.protocol_version=66

    return cluster  


def executeStatement(st):

    cluster=returnCluster()
    session = cluster.connect()
    session.default_timeout=timeOut        
    future = session.execute_async(st)
    future.result()
    cluster.shutdown()
                         
    return True

def getQuery(query):    

    cluster=returnCluster()
    session = cluster.connect()
    session.default_timeout=timeOut
    row=''
    future = session.execute_async(query)
    row=future.result()
    cluster.shutdown()
                   
    return row  

def insertJSON(json_doc,table):
     
    record_added=False
    cluster=returnCluster()
    session = cluster.connect()
    session.default_timeout=timeOut
    jsonS=json.dumps(json_doc)           
    insertSt="INSERT INTO "+keyspace+"."+table+" JSON '"+jsonS+"';" 
    future = session.execute_async(insertSt)
    future.result()  
    record_added=True
    cluster.shutdown()     
                    
                         
    return record_added    



class CassandraConnection():
    cc_user_test='MpvtYRWPigKTDLxfcZMNIfYQ'
    cc_pwd_test='joFIPwAoFL_JWNsgAr,xTNf30gZpZu3Fg6,eMxQjKxm-Gz5Uva2R.ELwwzj88f4XPePGhXLWU89xzzP8a1BdgSpwLN+iPHhQpjRmXnvA-cbmvoK_In8Sr,MGadqF+TAh'
        

