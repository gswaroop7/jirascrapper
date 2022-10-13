import requests
import json
from bs4 import BeautifulSoup

session = requests.Session()
userid = '<USERID>'
token = '<TOKEN>'
HOST = '<your_jira/confluence_host>'
session.auth = (userid, token)

#this script is initially written for atlassian
file_location = "<FULLPATH>"

def scrape_confluence(base_url, file_location):
	request_string = base_url+"?expand=body.view"
	resp = session.get(request_string)
	jout = json.loads(resp.text)
	response = jout['body']['view']['value']
	doc = BeautifulSoup(response, "html.parser", from_encoding='utf-8')
	print(doc.original_encoding)
	#print (doc.prettify('latin-1'))
	res = doc.find_all(["p"])
	for data in res:
		#print (data.prettify('latin-1'))
		all = data.get_text()
		#print (all)
		if (len(all) > 2):
			problem = all
			break

	ticket_number = HOST+"/pages/viewpage.action?pageId="+jout['id']
	ticket_summary = jout['title']
	ticket_description = problem
	ticket_solution = problem
    
	ticket_details = (ticket_number, ticket_summary, ticket_description, ticket_solution)
	try:
        	with open(file_location,"a") as f:
	        	f.write(','.join(ticket_details))
        		f.write("\n")
	except Exception as e:
        	return str(e)
	
	
def get_confluence_data():
	request_string = HOST+"/rest/api/search?cql=space=DNEPE3%20AND%20label=%22kb-troubleshooting-article%22%20AND%20text~%22citrix%22"

	resp = session.get(request_string)
	json.loads(resp.text)
	jout = json.loads(resp.text)
	jlist= jout['results']
	idarr = []
	for jsl in jlist:
		apiurl = jsl['content']['_links']['self']
		idarr.append(apiurl)
	return idarr

base_urls = get_confluence_data()
for base_url in base_urls:
        res = scrape_confluence(base_url, file_location)
        if (res):
            print ("Faliure")
        else:
            print ("Good")
