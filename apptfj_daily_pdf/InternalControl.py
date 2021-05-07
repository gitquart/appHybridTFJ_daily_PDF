import os

class cInternalControl:
    idControl=9
    timeout=70
    heroku=False
    pdfOn=True
    version='apptfj_daily_pdf'
    download_dir='Download_'+version
    hfolder=version  
    rutaHeroku='/app/'+hfolder
    rutaLocal=os.getcwd()+'\\'+hfolder+'\\'
    
    