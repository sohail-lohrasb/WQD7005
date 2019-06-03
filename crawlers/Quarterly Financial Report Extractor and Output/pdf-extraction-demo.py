import PyPDF2
import re

pdfName = 'C:\\Users\\Kavish\\Dropbox\\_Master of Data Science - UM\\WQD7005 - Data Mining\\Assignment\\Milestone 2\\wip\\KESMI.pdf'
reader = PyPDF2.PdfFileReader(pdfName)

search_items = []
for i in range(reader.getNumPages()):
    page = reader.getPage(i)
    page_content = page.extractText()
    
    pattern = 'Revenue([\s\S]*?)Other items of income'
    result = re.findall(pattern, page_content, re.MULTILINE)
    search_items.append(result)

clean_data = []
data = search_items[0][0].split('\n')
for i in data:
    if i.strip() != '':
        clean_data.append(i.strip().strip('\(%\)').replace(',',''))
        
names = ['Current Year Quarter','Preceding Year Quarter','% Change','Current Year to Date','Preceding Year to Date','% Change']

file = open("pdf-demo-output.txt","a+")
file.write(','.join(names)+'\n')
file.write(','.join(clean_data))
file.close()