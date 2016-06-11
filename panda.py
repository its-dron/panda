import requests
from bs4 import BeautifulSoup as bs
import re
import Config
import sys

def main(argv):
    if len(argv) != 2:
        print "Usage: panda.py USERNAME PASSWORD"
        exit(-1)

    USERNAME = argv[0]
    PASSWORD = argv[1]
    
    print "Logging in with username: " + USERNAME

    LOGIN_DATA = {'username': USERNAME,
                  'password': PASSWORD,
                  'f'       : 'Verify' }
    LOGIN_URL = "http://www.pandamagazine.com/index.php"

    PROGRESS_URL = "http://www.pandamagazine.com/index.php?f=Progress&iss="

    # regex to match only non-alphanumeric characters
    NON_ALPHANUMERIC = re.compile('[\W_]+')

    r = requests.post(LOGIN_URL, data=LOGIN_DATA)
    html = r.content
    cookies = r.cookies

    if "input type=password" in html:
        print "Unable to log in. Check your username and password"
        exit(-1)

    issueNames = map(lambda x: x.text, bs(html, "html.parser").select("b a"))
    issues = set(re.findall("&iss=(\d+)", html))

    if len(issues) == 0:
        print "Unable to find any issues. Do you own any?"
        exit(-1)

    print "Found " + str(len(issues)) + " issues. Parsing answers..."
    for issue, name in zip(issues, issueNames):
        print "Getting answers for " + name
        progress = requests.get(PROGRESS_URL + issue, cookies=cookies).content
        soup = bs(progress, "html.parser")
        
        answerTable = soup.findAll("table")[3]
        puzzles = answerTable.findAll("tr")

        if len(puzzles) == 0:
            print "No puzzles found? Weird"
            continue

        template = ""
        with open('template.html', 'r') as f:
            template = f.read()

        answerString = ""
        puzzleString = ""
        for i in range(1,len(puzzles)):    
            p = puzzles[i]
            parts = p.findAll("td")
            answered = len(parts[1].text) > 1
            
            answerStringLine = "answers[" + str(i-1) + "] = \""
            if answered:
                answerStringLine += parts[1].text
            else:
                print " - You haven't answered puzzle " + parts[0].text + "!"
            answerStringLine += "\";\n"
            answerString += answerStringLine

            if answered:
                puzzleString += "<option>" + parts[0].text + "</option>\n"
            else:
                puzzleString += "<option disabled>" + parts[0].text + " (Answer not known)</option>\n"

        template = template.replace("%1", answerString)
        template = template.replace("%2", name)
        template = template.replace("%3", puzzleString)

        fname = NON_ALPHANUMERIC.sub('', name) + ".html"
        with open(fname, 'w') as f:
            f.write(template)

if __name__ == "__main__":
    main(sys.argv[1:])
