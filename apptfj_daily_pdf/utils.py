from selenium.webdriver.common.by import By
import cassandraSent as bd
import PyPDF2
import uuid
import base64
import time
import json
import os
import sys
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from textwrap import wrap
import calendar
from InternalControl import cInternalControl

#Local
#download_dir='C:\\DownloadsTFJFA'

#Heroku
objControl=cInternalControl()
download_dir=objControl.download_dir
completeDownloadFolder=''

def getDatesForSearch(strDate):
    #dd/mm/yyyy
    chunks=strDate.split('/')
    day=chunks[0]
    month=chunks[1]
    year=chunks[2]
    fw,days=calendar.monthrange(int(year),int(month))
    lsDates=[]
    #Setting first day of query
    lsDates.append(day+'/'+month+'/'+year)
    secondDate=''
    nextDay=''
    nextMonth=''
    nextYear=''
    #Calculating second date of query
    if int(day)<days:
        #Comparing days in the same
        nextDay=int(day)+1
        secondDate=str(nextDay).zfill(2)+'/'+month+'/'+year
        lsDates.append(secondDate)
    else:
        nextDay='01'
        if int(month)==12:
            nextMonth='01'
            nextYear=int(year)+1
        else:
            nextMonth=int(month)+1  
            nextYear=str(year)  
        lsDates.append(str(nextDay)+'/'+str(nextMonth).zfill(2)+'/'+str(nextYear))

    return lsDates



def appendInfoToFile(path,filename,strcontent):
    txtFile=open(path+filename,'a+')
    txtFile.write(strcontent)
    txtFile.close()


"""
processRows:

//*[@id="dtRresul_data"]/tr[1]/td[1]
//*[@id="dtRresul_data"]/tr[1]/td[2]
//*[@id="dtRresul_data"]/tr[1]/td[3]
...
//*[@id="dtRresul_data"]/tr[1]/td[5]
"""

def processRows(browser,row):
    pdfDownloaded=False
    #For this version of code, the only fields to read are: num_exp, pdfname,pdf file
    for col in range(1,16):
        if col==2:
            numExp=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
        #if col==3:
            #viaTram=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
        #if col==4:
            #tipoJuicio=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
        #if col==5:
            #fechaPres=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
        #if col==6:
            #resolImp=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
        #if col==7:
            #leyQueFunda=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
        #if col==8:
            #sentDeLaSent=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
        #if col==9:
            #subject=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
        if col==10:
            sub_subject=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
        #if col==11:
            #region=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
        #if col==12:
            #court=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
        #if col==13:
            #title=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
        if col==14:
            namePDF=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
        #if col==15:
            #dt_date=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0].text
            
        
        if (objControl.pdfOn):
            if col==1:
                #This is the xpath of the link : //*[@id="grdSentencias_ctl00__'+str(row)+'"]/td['+str(col)+']/a
                #This find_element method works!
                time.sleep(5)
                pdfButton=browser.find_elements_by_xpath('//*[@id="dtRresul_data"]/tr['+str(row)+']/td['+str(col)+']')[0]
                pdfButton.click()
                #Wait some time until the file is downloaded
                time.sleep(15)
                #The file is downloaded rare, then just renaming it solves the issue
                for file in os.listdir(completeDownloadFolder):
                    pdfDownloaded=True
                    if objControl.heroku:
                        os.rename(completeDownloadFolder+'/'+file,completeDownloadFolder+'/00000.pdf')
                    else:
                        os.rename(completeDownloadFolder+'\\'+file,completeDownloadFolder+'\\00000.pdf')

        else:
            print('The pdf process is turned off now...')        
               

    
       
    #Build the json by row  
    if objControl.heroku:        
        json_sentencia=devuelveJSON(objControl.rutaHeroku+'/json_sentencia.json')
    else:
        json_sentencia=devuelveJSON(objControl.rutaLocal+'json_sentencia.json')             
    #Start of JSON filled
    json_sentencia['num_exp']=numExp.replace("'"," ")
    #json_sentencia['via_tramit']=viaTram.replace("'"," ")
    #json_sentencia['type_judge']=tipoJuicio.replace("'"," ")
    #json_sentencia['dt_demandfeature']=fechaPres.replace("'"," ")
    #json_sentencia['resolimpugnada']=str(resolImp).replace("'"," ")
    #json_sentencia['ley_base_res_impug']=leyQueFunda.replace("'"," ")
    #json_sentencia['sentido_sent']=sentDeLaSent.replace("'"," ")
    #json_sentencia['subject']=subject.replace("'"," ")
    #json_sentencia['sub_subject']=sub_subject.replace("'"," ")
    #json_sentencia['region']=region.replace("'"," ")
    #json_sentencia['court_room']=court.replace("'"," ")
    #json_sentencia['title']=title.replace("'"," ")
    json_sentencia['pdfname']=namePDF.replace("'"," ")
    #Working with the date, this field will deliver:
    #1.Date field,2. StrField and 3.year
    # timestamp accepted for cassandra: 
    # yyyy-mm-dd  , yyyy-mm-dd HH:mm:ss
    #In web site, the date comes as 27-10-2020 14:38:00
    #data=''
    #data=dt_date.split(' ')
    #dDate=str(data[0]).split('-')
    #dDay=dDate[0]
    #dMonth=dDate[1]
    #dYear=dDate[2]
    #dTime=data[1]
    #fullTimeStamp=dYear+'-'+dMonth+'-'+dDay+' '+dTime;
    #json_sentencia['year']=int(dYear)
    #json_sentencia['publication_datetime']=fullTimeStamp
    #json_sentencia['strpublicationdatetime']=fullTimeStamp                  
                   

    #First the metadata of document is inserted, then the PDF, hence the PDF must be validated by chunks
    if (objControl.pdfOn):
        #The metadata and pdf content is inserted in the same table
        if pdfDownloaded==True:
            #Check if the pdf is already in database
            pdfname=json_sentencia['pdfname']
            num_exp=json_sentencia['num_exp']
            query="select id from test.tbcourtdecisiontfjfa_pdf where pdfname='"+pdfname+"' and num_exp='"+num_exp+"' ALLOW FILTERING"
            res=bd.getQuery(query)
            if res:
                print('Pdf: '+pdfname+' is already in database, going on with next pdf...')
            else:    
                processPDF(json_sentencia)
                print('PDF done')
            for file in os.listdir(completeDownloadFolder):   
                if objControl.heroku:
                    os.remove(completeDownloadFolder+'/'+file)
                else:
                    os.remove(completeDownloadFolder+'\\'+file)

                


                    
"""
readPDF is done to read a PDF no matter the content, can be image or UTF-8 text
"""
def readPDF(file):
    separador=''
    if objControl.heroku:
        separador='/'
    else:
        separador='\\'      
    with open(completeDownloadFolder+separador+file, "rb") as pdf_file:
        bContent = base64.b64encode(pdf_file.read()).decode('utf-8')
    
    return bContent  
    

"""
This is the method to call when fetching the pdf enconded from cassandra which is a list of text
but that text is really bytes.
"""
def decodeFromBase64toNormalTxt(b64content):
    normarlText=base64.b64decode(b64content).decode('utf-8')
    return normarlText


def getPDFfromBase64(bContent):
    #Tutorial : https://base64.guru/developers/python/examples/decode-pdf
    bytes = base64.b64decode(bContent, validate=True)
    # Write the PDF contents to a local file
    f = open(download_dir+'\\result.pdf', 'wb')
    f.write(bytes)
    f.close()
    return "PDF delivered!"

def TextOrImageFromBase64(bContent):
    #If sData got "EOF" is an image, otherwise is TEXT
    sData=str(bContent)
    if "EOF" in sData:
        res=getPDFfromBase64(bContent) 
    else:
        res=decodeFromBase64toNormalTxt(bContent)

    return res 

def devuelveJSON(jsonFile):
    with open(jsonFile) as json_file:
        jsonObj = json.load(json_file)
    
    return jsonObj 

def processPDF(json_sentencia):
    """
    Docs:processPDF
    This process already sets a list of 20 items (the nice limit in cassandra list)
    """
    lsContent=[]  
    for file in os.listdir(completeDownloadFolder): 
        strFile=file.split('.')[1]
        if strFile=='PDF' or strFile=='pdf':
            strContent=readPDF(file) 
            print('Start wrapping text...') 
            lsContent=wrap(strContent,1000)  
            totalElements=len(lsContent)
            for i in range(0,totalElements+1):
                json_sentencia['lspdfcontent'].clear()
                json_sentencia['lspdfcontent'].append(lsContent[i])
                json_sentencia['secuencia']=i
                #Check if the current chunk exists
                pdfname=json_sentencia['pdfname']
                num_exp=json_sentencia['num_exp']
                secuencia=str(json_sentencia['secuencia'])
                query="select id from test.tbcourtdecisiontfjfa_pdf where pdfname='"+pdfname+"' and num_exp='"+num_exp+"' and secuencia="+secuencia+" ALLOW FILTERING"
                resQuery=bd.getQuery(query)
                if resQuery:
                    print('The chunk already exists')
                else:    
                    #If the pdf name, expedient name and sequence doesn't exist, then create the UUID to insert
                    json_sentencia['id']=str(uuid.uuid4())
                    resInsert=bd.insertJSON(json_sentencia,'tbcourtdecisiontfjfa_pdf') 
                    if resInsert:
                        print('Chunk of pdf added: '+str(i)+' of '+str(totalElements))  
                    
                
                           

def readPyPDF(file):
    #This procedure produces a b'blabla' string, it has UTF-8
    #PDF files are stored as bytes. Therefore to read or write a PDF file you need to use rb or wb.
    lsContent=[]
    pdfFileObj = open(download_dir+'/'+file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pags=pdfReader.numPages
    for x in range(0,pags):
        pageObj = pdfReader.getPage(x)
        #UTF-8 is the right encodeing, I tried ascii and didn't work
        #1. bContent is the actual byte from pdf with utf-8, expected b'bla...'
        bcontent=base64.b64encode(pageObj.extractText().encode('utf-8'))
        lsContent.append(str(bcontent.decode('utf-8')))
                         
    pdfFileObj.close()    
    return lsContent 

def returnChromeSettings():
    browser=''
    chromedriver_autoinstaller.install()
    profile = {"plugins.plugins_list": [{"enabled": True, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
               "download.default_directory": completeDownloadFolder , 
               "download.prompt_for_download": False,
               "download.directory_upgrade": True,
               "download.extensions_to_open": "applications/pdf",
               "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
               }           
    if objControl.heroku:
        #Chrome configuration for heroku
        chrome_options= webdriver.ChromeOptions()
        chrome_options.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option('prefs',profile)
        browser=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_options)

    else:
        options = Options()
        options.add_experimental_option("prefs", profile)
        browser=webdriver.Chrome(options=options)  

    

    return browser   

def initialDownloadDirCheck():
    print('Checking if download folder exists...')
    directory_created=''
    #Create directory depending if it's in heroku or not
    if objControl.heroku:
        isdir = os.path.isdir(objControl.rutaHeroku+'/'+download_dir)
        directory_created=objControl.rutaHeroku+'/'+download_dir
    else:
        isdir=os.path.isdir('C:\\'+download_dir)
        directory_created='C:\\'+download_dir 
    #Set directory created 
    global completeDownloadFolder   
    completeDownloadFolder=directory_created   
    #Create directory if it doesnt exist      
    if isdir==False:
        print('Creating download folder...')
        os.mkdir(completeDownloadFolder)  
        print('Download directory created...')
    #Dele files in folder    
    for file in os.listdir(completeDownloadFolder):
        if objControl.heroku:
            os.remove(completeDownloadFolder+'/'+file)
        else:
            os.remove(completeDownloadFolder+'\\'+file)
        print('Download folder empty...')   

def devuelveElemento(xPath, browser):
    cEle=0
    while (cEle==0):
        cEle=len(browser.find_elements_by_xpath(xPath))
        if cEle>0:
            ele=browser.find_elements_by_xpath(xPath)[0]

    return ele  

def devuelveListaElementos(xPath, browser):
    cEle=0
    while (cEle==0):
        cEle=len(browser.find_elements_by_xpath(xPath))
        if cEle>0:
            ele=browser.find_elements_by_xpath(xPath)

    return ele      

def checkAllFields(browser):
    for col in range(1,4):
        if col!=2:
            for row in range(1,8):
                if (col==1 and row==6) or (col==1 and row==7) or (col==3 and row==5) or (col==3 and row==7):
                    pass    
                else:
                    ckCol=devuelveElemento('//*[@id="formCheckBox:gridColCheck"]/tbody/tr['+str(row)+']/td['+str(col)+']/div/div[2]/span',browser)
                    ckCol.click() 

def prepareNextQuery(strdates): 
    #strdates = 11/1997 for example
    chunks=strdates.split('/')
    month=int(chunks[0])
    year=int(chunks[1])
    #Case if month is december
    if month==12:
        year+=1
        month=1
    else:
        month+=1    
            
    strMonth=str(month).zfill(2)
    strYear=str(year)
    dateval=strMonth+'/'+strYear
    st="update test.cjf_control set page=1,fechaactual='"+str(dateval)+"' where id_control="+str(objControl.idControl)+";"
    bd.executeStatement(st)
    os.sys.exit(0) 

                        


    
                               
                                         