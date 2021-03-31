from requests_html import HTMLSession
import pandas as pd
from datetime import datetime
import time

start_time = time.time()

# Search results for Python Programmer
#URL = 'https://www.indeed.com/jobs?q=Python+Programmer&l=Holyoke%2C+MA&ts=1612964348768&rq=1&rsIdx=1&fromage=last&newcount=4'
# Search results for Programmer
#URL = 'https://www.indeed.com/jobs?q=Programmer&l=Holyoke%2C+MA&rqf=1'
# Search results for Data Science
#URL = 'https://www.indeed.com/jobs?q=data+science&l=Holyoke%2C+MA'
# Search for Data Scientist
#URL = 'https://www.indeed.com/jobs?q=data+scientist&l=Holyoke%2C+MA'

search_term = 'Data Engineer'
ma_town = 'Boston'
# Dynamic link for __ jobs in Holyoke:
URL = f'https://www.indeed.com/jobs?q={search_term.replace(" ","+")}&l={ma_town}%2C+MA'

headers = {
    'User-Agent' : 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.197 Safari/537.36',
    'Accept-Language' : 'en-US,en;q=0.9',
    'Referer' : 'https://google.com',
    'DNT' : '1',
}


s = HTMLSession()

def get_pages(main_url): # Pass in URL
    next_button_exists = True
    pages = [main_url]
    URL = main_url # to start with; it will change as it iterates
    counter=1
    while next_button_exists:
        print(f"\nGetting link to page #{counter}...")
        r = s.get(URL, headers=headers) 
        try:
            next_page = r.html.find('div.pagination a[aria-label=Next]',first=True).absolute_links
            print(f"Next page: {next_page}")
            print(f"Appending list: {next_page}\n")
            pages.append(list(next_page)[0])
            URL = list(next_page)[0]
            counter+=1

            # TESTING THIS LINE OF CODE
            #if counter > 9:
            #    break 
            # END OF TEST CODE

        except:
            print(f"Link {counter} does not exist; list contains {counter} links")
            next_button_exists=False
            break
    print("")
    for page in pages:
        print(page)
    return pages # A list of links to all pages of results

def jobs_on_page(current_page):
    r = s.get(current_page)
    titles = r.html.find('h2.title') # All job cards on a page
    return titles # Return all job card elements on page so next function can extract links

def link_grabber(titles):
    links=[]    
    for title in titles:
        #print(title.text)
        #print(f"https://www.indeed.com{title.find('a[href]',first=True).attrs['href']}")
        #print('')
        links.append(f"https://www.indeed.com{title.find('a[href]',first=True).attrs['href']}")

    print("There are " + str(len(links)) + " links on page.")
    return links

def get_job_data(links):
    job_list = []
    for link in links:
        r = s.get(link)

        title = r.html.find('div.jobsearch-JobInfoHeader-title-container h1',first=True).text
        comp_info = r.html.find('div.jobsearch-CompanyInfoWithoutHeaderImage',first=True).text.replace("\n"," | ")

        # Try to get SALARY and JOB TYPE information; if none is provided
        # use 'Not Provided'
        salary = 'Not Provided' # In case none is provided
        job_type = 'Not Provided' # In case none is provided
        job_details = r.html.find('div.jobsearch-JobDescriptionSection-sectionItem')
        for i in range(len(job_details)):
            if job_details[i].find('div.jobsearch-JobDescriptionSection-sectionItemKey.icl-u-textBold',first=True).text.lower() == 'salary':
                salary = job_details[i].find('div.jobsearch-JobDescriptionSection-sectionItem span',first=True).text
            if job_details[i].find('div.jobsearch-JobDescriptionSection-sectionItemKey.icl-u-textBold',first=True).text.lower() == 'job type':
                job_type = job_details[i].find('div.jobsearch-JobDescriptionSection-sectionItem div')[1].text

        # Try to get QUALIFICATIONS as a list; if none is provided
        # the list will only include 'Not Provided'
        try:
            quals = r.html.find('#qualificationsSection ul li.icl-u-xs-block.jobsearch-ReqAndQualSection-item--title')
            quals_list = []

            for i in range(len(quals)):
                quals_bullets = quals[i].find('ul li p')
                for j in range(len(quals_bullets)):
                    quals_list.append(quals_bullets[j].text)
            quals_list[0] # Will trigger the error/Except if needed
            
        except:
            quals_list = ['Not Provided'] # In case none is provided

        # Try to get JOB DESCRIPTION
        try:
            fulldescrip = r.html.find('#jobDescriptionText',first=True).text.replace('\n',' ')
        except:
            fulldescrip = 'Description not provided'

        # Get job posting metadata (including how old the posting is)
        metadata = r.html.find('div.jobsearch-JobMetadataFooter',first=True).text.replace('\n', ' | ')


        # Create a dictionary for each job
        job = {
            'Title': title,
            'Company_Info': comp_info,
            'Salary': salary,
            'Job_Type': job_type,
            'Qualifications': quals_list,
            'Description': fulldescrip,
            'MetaData': metadata,
            'Link': link
        }

        job_list.append(job)
    return job_list

# Figure out how many pages of data; get links to each
pages = get_pages(URL)

# For each page of data, get all jobs on page
# ...and get all the links for those jobs
all_links = []
for page in pages:
    titles = jobs_on_page(page)
    links = link_grabber(titles)
    all_links.append(links)
# To make a list of lists into a single 'flattened list'
# (ref this stack overflow: https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists)
flat_list = [item for sublist in all_links for item in sublist]

# Once a full list of individual job links is ready, get the job data
results = get_job_data(flat_list)
for result in results:
    print(result)
    print("")


#========Exporting=====================================
print("\nExporting data to CSV...")
df = pd.DataFrame(results)
date_for_filename = str(datetime.now().date())
filename = f'indeed-{search_term.replace(" ","")}-{ma_town} ({date_for_filename}).csv'
df.to_csv(filename)
print(f"\nExport Complete!\nFilename: {filename}")
print(f"Runtime: {'%.2f' %(time.time() - start_time)} seconds")
