import os

class cInternalControl(object):
    idControl=9
    timeout=70
    heroku=True
    pdfOn=True
    version='apptfj_daily_pdf'
    download_dir='Download_'+version
    hfolder=version  
    rutaHeroku='/app/'+hfolder
    #Ruta de archivos en worspace
    rutaLocal=os.getcwd()+'\\'+hfolder+'\\'
        
    
    