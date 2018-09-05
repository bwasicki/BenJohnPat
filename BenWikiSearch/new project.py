import time
import wikipedia
import xlsxwriter
from bs4 import BeautifulSoup

excel = xlsxwriter.Workbook('doc1.xlsx')
sheet = excel.add_worksheet()

wikipage = wikipedia.WikipediaPage('British Empire')

wikipages = list()
titles = list()
words = list()
nums = list()

def search():
    page_title = ''
    while page_title != "!!!":
        page_title = input('Please Enter a valid Wikipedia Page. If done, Enter "!!!" ')
        if page_title != "!!!":
            try:
                wikipage = wikipedia.WikipediaPage(page_title)
                titles.append(page_title)
            except:
                print('Not a valid Page')
    titles.sort()
    for title in titles:
        wikipage = wikipedia.WikipediaPage(title)
        wikipages.append(wikipage)
    word = ''
    while word != "!!!":
        word = input('Please enter word to search. If done, Enter "!!!" ')
        if word != "!!!":
            words.append(word)
    time_s = time.time()
    words.sort()
    for wikipage in wikipages:
        for word in words:
            plainText = getPlainText(wikipage).get_text()
            num = plainText.lower().split().count(word.lower())
            nums.append(num)
    writeToExcel() 
    time_e=time.time()
    print('time elapsed: ', time_e-time_s)

def writeToExcel():
    print('writing to excel...')
    row=1
    col=1
    sheet.write(0, 0, 'page')
    sheet.write(0, 1, 'word')
    sheet.write(0, 2, 'count')
    for wikiIndex in range(0, len(wikipages)):
        sheet.write(wikiIndex*len(words)+1,0,wikipages[wikiIndex].title)
        for col in range(1, 2):
            for row in range(1, len(words)+1):
                sheet.write(wikiIndex*len(words)+row, col, words[row-1] )
                sheet.write(wikiIndex*len(words)+row, col+1, nums[wikiIndex*len(words)+row-1])
    
    excel.close()
    print('written.')
    
def getPlainText(page):
    return BeautifulSoup(page.html(), 'html.parser')
