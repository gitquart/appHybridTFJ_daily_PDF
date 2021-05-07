import os

class cInternalControl:
    idControl=8
    timeout=70
    heroku=False
    pdfOn=False
    download_dir='Download_tfja_Daily'
    hfolder='apptfj_daily_3'   
    rutaHeroku='/app/'+hfolder
    rutaLocal=os.getcwd()+'\\'+hfolder+'\\'
    
    