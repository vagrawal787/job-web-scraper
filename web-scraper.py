from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from datetime import datetime

import pandas as pd
import requests
import json

api_key = ""

openAiHeaders = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {}".format(api_key)
}

class JobPosting(object):
    def __init__(self, title, link):
        self.title = title
        self.link = link
    def to_dict(self):
        return {
            'title': self.title,
            'link': self.link
        }
def main(position, pages):

    with sync_playwright() as p:
        #launch browser and go to url
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.indeed.com/")
        page.wait_for_selector("div[role=search]")

        #input software engineer search and wait for results
        page.get_by_placeholder("Job title, keywords, or company").fill(position)
        page.get_by_role("button", name="Search").click()
        page.wait_for_selector("#mosaic-provider-jobcards > ul > li:nth-child(1)")

        #parse results
        counter = 0
        parsed = []
        while counter < pages:
            soup = BeautifulSoup(page.content(), features="html.parser")
            items = soup.select("#mosaic-provider-jobcards > ul > li")
            for item in soup.select("#mosaic-provider-jobcards > ul > li"):
                if item.select_one('div#mosaic-afterFifthJobResult') != None or item.select_one('div#mosaic-afterFifteenthJobResult') != None or item.select_one('div#mosaic-afterTenthJobResult') != None:
                    continue
                job_title = item.select_one('a span').text
                job_link = "https://www.indeed.com" + item.select_one('a').get("href")
                currId = item.select_one('a').get("id")
                page.click('a#{}'.format(currId))
                page.wait_for_selector('#jobDescriptionText')

                soup2 = BeautifulSoup(page.content(), features="html.parser")
                
                div_text = soup2.find("div", id="jobDescriptionText").get_text()
                ' '.join(div_text.split())
                keywords = ["years", "experience", "require", "qualification"]
                minIndex = len(div_text)
                for word in keywords:
                    currIndex = div_text.lower().find(word)
                    if currIndex > 0 and currIndex < minIndex:
                        if word == "years":
                            minIndex = currIndex - 5
                        else:
                            minIndex = currIndex
                if minIndex == len(div_text):
                    minIndex = 0
                div_text = div_text[minIndex:]
                aiData = {
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": "Does this job position require more than one year of experience as a {}? Respond with only one word, 'yes' or 'no'".format(position) + div_text}]
                }
                dumpData = json.dumps(aiData)
                response = requests.post('https://api.openai.com/v1/chat/completions', headers = openAiHeaders, data = dumpData)
                loadResponse = response.json()
                responseMessage = loadResponse['choices'][0]['message']['content']
                print("Position not matched: ", responseMessage)
                if "no" in str(responseMessage).lower():
                    jobPost = JobPosting(job_title, job_link)
                    parsed.append(jobPost)
                # FOR TEST PURPOSES    
                # break

            nextPage = page.get_by_test_id("pagination-page-next")
            if nextPage:
                nextPage.click()
                page.wait_for_selector("#mosaic-provider-jobcards > ul > li:nth-child(1)")
                counter += 1
            else:
                break


        # for job in parsed:
        #     print(job)

        jobDataframe = pd.DataFrame.from_records([j.to_dict() for j in parsed])

        jobDataframe.to_csv('{}_{}.csv'.format(position, datetime.now()))

        print("All jobs generated! Check your project directory for the csv file with results! Here's a little preview:")

        print(jobDataframe.head())
        
        page.wait_for_timeout(2000)
        browser.close()

if __name__ == '__main__':
    print("Thanks for using the entry-level job filter!")
    position = input("What role are you applying to? (e.g. software engineer, product manager, etc.): ")
    pages = int(input("How many pages of results do you want to filter? (Costs go up for more pages, about $2.00 per 1000 roles / about 12 roles per page). Please enter a number: "))

    print("Thanks! Generating jobs now, please hold on! P.S. don't interact with the popup browser, it'll do the work :)")
    main(position, pages)
