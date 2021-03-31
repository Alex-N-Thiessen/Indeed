#==================================================================================
# Web Scraper to collect data from Indeed.com and create a CSV
#==================================================================================

from requests_html import HTMLSession

# Link to search results
#URL = 'https://www.indeed.com/jobs?q=Python+Programmer&l=Holyoke%2C+MA&ts=1612964348768&rq=1&rsIdx=1&fromage=last&newcount=4'
# Another link to some search results (testing pagination)
URL = 'https://www.indeed.com/q-Programmer-l-Holyoke,-MA-jobs.html?from=relatedQueries&saIdx=4&rqf=1&parentQnorm=Python+Programmer'

# Link to an actual job posting (i.e. details on right-hand side of screen)
#URL = 'https://www.indeed.com/viewjob?cmp=Smoothstack&t=Entry+Level+Software+Developer&jk=5f913bcfecb065a5&sjdu=P79yvCsiQGT8ISk6zglRD4q_wAYZYdF0BncIJkxvh-Nl6j1yqqV4r2HBCVzSSUrQdQyF_kKxCzQF1rsD4XAgrQ&adid=327153611&ad=-6NYlbfkN0ChdE_-3s9UeG5xYsqO3th9AddXeBq2OieSfAM8evhI-HUZpuQaiuzQc33v7SXoh9w3fOChrNSzJcTy_8FRa1fReeWPVBneE_KlwgXb7y7fGoIHaC7p9LpFA06OT38qWHnNSgBvaugOt4l03p-04Usoo0OS7OghwSPnTnHzoDbZ8vcDd3ZzbHOr8bGn7W3XlvNuQAY_jFOlA8UrXMoIbAYqwKazgx2uiaARIk1J1n-Q1GU_twcYzUHUoNm3tjSu8xLgGNs3BZXaZTIfB8CmkEHG_k_KDCwkF8hGfGmAL27kHOpaPAkbvQKW1elNoRPON9I%3D&pub=4a1b367933fd867b19b072952f68dceb&vjs=3'
s = HTMLSession()
#r = s.get(URL)

next_button_exists = True
pages = [URL]
counter=1
while next_button_exists:
    print(f"\nGetting link #{counter}...")
    r = s.get(URL)
    try:
        next_page = r.html.find('div.pagination a[aria-label=Next]',first=True).absolute_links
        print(f"Next page: {next_page}")
        print(f"Appending list: {next_page}\n")
        pages.append(list(next_page)[0])
        URL = list(next_page)[0]
        counter+=1
    except:
        print(f"Link {counter} does not exist; list contains {counter} links")
        next_button_exists=False
        break
print("")
for page in pages:
    print(page)



# LIBRARY OF ELEMENTS
# 'Title': r.html.find('div.jobsearch-JobInfoHeader-title-container h1',first=True).text

# https://www.indeed.com/jobs?q=data%20science&l=Holyoke%2C%20MA&ts=1612964348768&rq=1&rsIdx=1&fromage=last&newcount=4&advn=2925777763912502&vjk=dde1ac6850c075cf
