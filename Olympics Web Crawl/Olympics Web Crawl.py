import wikipedia
import xlsxwriter
import urllib
from bs4 import BeautifulSoup
from datetime import datetime

fopen = open('List of 2014 Winter Olympics medal winners.txt', 'r')
html_doc = fopen.read()

soup = BeautifulSoup(html_doc, 'html.parser')
workbook = xlsxwriter.Workbook('Athletes.xlsx')
worksheet = workbook.add_worksheet()

names = list()
country = list()
links = list()
sportsList = list()
athletes = list()
tables2014 = [2, 3, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2]
badAcros = ['SUI', 'USA', 'CAN', 'GER', 'RUS', 'WJR']
badNums = ['[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]', '[9]', '[10]', '[11]', '[12]', '[13]']   



def getSports():
    sportsList.clear()
    contents = soup.find(id='toc')
    for sport in contents.find_all('a'):
        sportsList.append(sport.string)
    sportsList.pop()
    sportsList.pop()

def printSports():
    for sport in sportsList:
        print(sport)
    


def printResults():
    for person in athletes:
        print("--- NEW ATHLETE ---")
        print(person.toString())
        print()


def countTags(tag):
    count = 0    
    for td in tag.find_all('a'):
        count = count + 1

def makeAthlete(tag, sport):
    index = 0
    name = ''
    country = ''
    DOB = ''
    description = ''
    title = ''
    image = ''
    for a in tag.find_all('a'):
        if(a.string in badAcros or a.string in badNums):
            print('Bad name for Individual Athlete')
            return
        else:
            if(index == 0):
                name = a.string
                title = a.get('title')
            else:
                country = a.string
            index = index + 1

    try:
        description = getDescription(title)
    except:
        print("Failed to find athlete's Wikipedia page: " + name)
        
    try:
        DOB = getDOB(title)
        date = datetime.strptime(DOB, '%Y-%m-%d')
        DOB = date.strftime('%m/%d/%Y')
    except:
        print("Failed to find athlete's DOB: " + name)
		
    try:
            image = getImage(title)
    except:
            print("Failed to find athlete's image: " + name)
    
    newAthlete = Athlete(name, country, sport, DOB, description, image)
    athletes.append(newAthlete)

	
def makeAthleteFromTeam(tag, sport, country):
    index = 0
    name = tag.string
    title = tag.get('title')
    description = ''
    DOB = ''
    image = ''

    if(name in badAcros or name in badNums):
        print('Bad name for Team Athlete')
        return
    
    try:
        description = getDescription(title)
    except:
        print("Failed to find athlete's Wikipedia page: " + name)

    try:
        DOB = getDOB(title)
        date = datetime.strptime(DOB, '%Y-%m-%d')
        DOB = date.strftime('%m/%d/%Y')
    except:
        print("Failed to find athlete's DOB: " + name)
		
    try:
            image = getImage(title)
    except:
            print("Failed to find athlete's image: " + name)
        
    newAthlete = Athlete(name, country, sport, DOB, description, image)
    athletes.append(newAthlete)

def makeTeam(tag, sport):
	index = 0
	country = ''

	for a in tag.find_all('a'):
		if(index == 0):
			country = a.string
		else:
			makeAthleteFromTeam(a, sport, country)
		index += 1
		
    

def getDOB(title):
    DOB = ''
    html = BeautifulSoup(wikipedia.WikipediaPage(title).html(), 'html.parser')
    try:
        DOB = html.find('span', class_="bday").string
    except:
        DOB = html.find('span', class_="dtstart bday").string
    
    return DOB


def getDescription(title):
    description = wikipedia.WikipediaPage(title).summary
    return description

def getImage(title):
    html = BeautifulSoup(wikipedia.WikipediaPage(title).html(), 'html.parser')

    a = html.find('a', class_="image")
    image = a.find('img').get('src')
    image = 'https:' + image
    return image

def writeToXlsx():
    row = 0
    col = 0
    for athlete in athletes:
    	worksheet.write(row, col, athlete.name)
    	worksheet.write(row, col+1, athlete.country)
    	worksheet.write(row, col+2, athlete.sport)
    	worksheet.write(row, col+3, athlete.DOB)
    	worksheet.write(row, col+4, athlete.description)
    	worksheet.write(row, col+5, athlete.image)
    	row += 1
    workbook.close()
    print('Done!')
		

class Athlete():

    def __init__(self, name, country, sport, DOB, description, image):
        self.name = name
        self.country = country
        self.sport = sport
        self.DOB = DOB
        self.description = description
        self.image = image

    def toString(self):
        return self.name + ', ' + self.country + ', ' + self.DOB + ', ' + self.sport



def athleteCrawl2010():
    getSports()
    namesStart = 0
    sport = ''
    index = 0
    startWord = 'References'

    
    for table in soup.find_all('table'):
            if(len(sportsList) == 0):
                break
            else:
                sport = sportsList.pop(0)
            for body in table.find_all('tbody'):
                for tr in body.find_all('tr'):
                    for td in tr.find_all('td'):
                        if(namesStart == 1):
                            
                            if(len(td.find_all('a')) == 2):
                                makeAthlete(td, sport)
                            else:
                                makeTeam(td, sport)
                            
                       
                        if(namesStart == 0):
                            for a in td.find_all('a'):
                                if(a.string == startWord):
                                    namesStart = 1
        
    print('Done! Number of athletes added: ' + str(len(athletes)))

def athleteCrawl2012():
    getSports()
    namesStart = 0
    sport = ''
    index = 0
    startWord = 'External Links'

    
    for table in soup.find_all('table'):
            if(len(sportsList) == 0):
                break
            else:
                sport = sportsList.pop(0)
            for body in table.find_all('tbody'):
                for tr in body.find_all('tr'):
                    for td in tr.find_all('td'):
                        if(namesStart == 1):
                            
                            if(len(td.find_all('a')) == 2):
                                makeAthlete(td, sport)
                            else:
                                makeTeam(td, sport)
                            
                       
                        if(namesStart == 0):
                            for a in td.find_all('a'):
                                if(a.string == startWord):
                                    namesStart = 1
        
    print('Done! Number of athletes added: ' + str(len(athletes)))
    

    

def athleteCrawl2014():
    getSports()
    namesStart = 0
    sport = ''
    index = 1
    tableNo = 0
    startWord = 'References'
    
    for table in soup.find_all('table'):
            if(len(sportsList) == 0):
                break
            else:
                if(index > tables2014[tableNo]):
                    sport = sportsList.pop(0)
                    tableNo += 1
                    index = 0
            for body in table.find_all('tbody'):
                for tr in body.find_all('tr'):
                    for td in tr.find_all('td'):
                        if(namesStart == 1):
                            
                            
                            if(len(td.find_all('a')) == 2):
                                makeAthlete(td, sport)
                            else:
                                makeTeam(td, sport)
                            
                       
                        if(namesStart == 0):
                            for a in td.find_all('a'):
                                if(a.string == startWord):
                                    namesStart = 1
            if(namesStart == 1):
                index += 1
        
    print('Done! Number of athletes added: ' + str(len(athletes)))

def chsrc(year):
    if(year == 2010):
        fopen = open('List of 2010 Winter Olympics medal winners.txt', 'r')
        html_doc = fopen.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
    elif(year == 2012):
        fopen = open('List of 2012 Summer Olympics medal winners.txt', 'r')
        html_doc = fopen.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
    elif(year == 2014):
        fopen = open('List of 2014 Winter Olympics medal winners.txt', 'r')
        html_doc = fopen.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
    else:
        print('Invalid year entered')
    

