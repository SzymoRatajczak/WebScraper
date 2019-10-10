import requests
from bs4 import BeautifulSoup
from urllib.request import URLError,HTTPError
import csv
from urllib.request import  urlopen,urlretrieve
from pdfminer.layout import LAParams
from pdfminer.converter import  TextConverter
from pdfminer.pdfinterp import process_pdf,PDFResourceManager
from io import StringIO,BytesIO
from zipfile import ZipFile


class WebScraper():
    def __init__(self,url,l,url_pdf,url_docx):
        self.url=url
        self.l=l
        self.pdf=url_pdf
        self.docx=url_docx

    def get_IMG(self):
        try:
            res=urlopen(self.url)
            bs=BeautifulSoup(res.read(),"html.parser")
            images=bs.find_all("img")
            counter=0
            for i in images:
                urlretrieve(i["data-src"],"picture"+str(counter)+".jpg")
                counter+=1
        except URLError as e:
            print("URL error:",e)
        except HTTPError as e:
            print("HTTP error :",e)

    def get_PDF(self):
        res=urlopen(self.pdf)
        resource=PDFResourceManager()
        IO=StringIO()
        lparam=LAParams()
        device=TextConverter(resource,IO,laparams=lparam)

        process_pdf(resource,device,res)

        content=IO.getvalue()
        print(content)
        device.close()


    def get_DOCX(self):
        res=urlopen(self.docx).read()
        document=BytesIO(res)
        document=ZipFile(document)
        xml_content=document.read("word/document.xml")

        bs=BeautifulSoup(xml_content,"xml")
        docx=bs.find_all("w:t")
        for i in docx:
            print(i)






    def get_links(self):
        try:
            res=requests.get(self.url)
            bs=BeautifulSoup(res.text,"html.parser")
            links=bs.find_all("a")
            for i in links:
                if "href" in i.attrs:
                    self.l.append(i.attrs["href"])
            WebScraper.Write_CSV(self)
            WebScraper.Write_TXT(self)
        except HTTPError as e:
            print("HTTP error:",e)
        except URLError as e:
            print("URL error:",e)


    def Write_TXT(self):
        file=open("Links_list.txt","w")
        file.write(str(self.l))
        file.close()

    def Read_TXT(self):
        file=open("Links_list.txt","r")
        for i in enumerate(file):
            print(i)


    def Write_CSV(self):
        file=open("Links_list.csv","w")
        writer=csv.writer(file)
        writer.writerow(self.l)
        file.close()

    def Read_CSV(self):
        file=open("Links_list.csv","r")
        reader=csv.reader(file)
        for i in reader:
            print(i)



l=[]
url=""
url_pdf=""
url_docx=""
scraper=WebScraper(url,l,url_pdf,url_docx)
scraper.get_DOCX()