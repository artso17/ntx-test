import os
import json
import asyncio
import httpx
import time
from bs4 import BeautifulSoup
from polars import DataFrame
from tqdm import tqdm 


# Define url
base_url = 'https://www.fortiguard.com'
url_template = base_url + '/encyclopedia?type=ips&risk={level}&page={page}'

# Define output directory to store all results
output_directory = "datasets"


# Define retries to all AsincClient if raise an error or timeout
transport = httpx.AsyncHTTPTransport(retries=3)

# Define fetch_data function
async def fetch_data(level, page):
    """
    Fetch data in the given level and page
    """

    # Open connection to httpx.AsyncClient 
    async with httpx.AsyncClient(transport=transport) as client:
        # Specify the destination url
        url = url_template.format(level=level, page=page)
        try:
            # Retrieve the data from url
            response = await client.get(url, timeout=20.0)
            
            # Raise the status response
            response.raise_for_status()

            # Parse the html
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title and link
            titles = [i.a.text for i in soup.find_all('div', class_='title')]
            links = [base_url+i.a['href'] for i in soup.find_all('div', class_='title')]

            return titles, links
        except httpx.HTTPError as e:
            return [], []

# Define scrape_levels function
async def scrape_levels(level,pages):
    all_titles = []
    all_links = []
    skipped_pages = []
    for page in tqdm(range(1,pages+1),desc = f'level {level}'):

        titles,links = await fetch_data(level,page)
        if titles == []:
            skipped_pages.append({'level':level,'page': page})
        all_titles.extend(titles)
        all_links.extend(links)
    df = DataFrame({'title':all_titles,'link':all_links})
    filename = f"{output_directory}/forti_lists_{level}.csv"
    df.write_csv(filename)

    skipped_filename = f"{output_directory}/skipped.json"
    with open(skipped_filename, 'w') as json_file:
        json.dump(skipped_pages, json_file)

# Define main function
async def main():

    '''
    Write the desc 
    '''

    # Make directory
    os.makedirs(output_directory, exist_ok=True)
    tasks = []

    for level in range(1,6):
        tasks.append(asyncio.create_task(scrape_levels(level,5)))

    for task in tasks:
        await task
    print('The Process Finished')


if __name__ == "__main__":
    asyncio.run( main())