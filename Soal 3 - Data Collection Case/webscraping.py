import os
import json
import asyncio
import httpx
from bs4 import BeautifulSoup
from polars import DataFrame
from tqdm import tqdm 


# Define url
base_url = 'https://www.fortiguard.com'
url_template = base_url + '/encyclopedia?type=ips&risk={level}&page={page}'

# Define output directory to store all results
output_directory = "datasets"

# Define the maximum number of pages for each level
max_pages = [5, 5, 5, 5, 5] 

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
            response = await client.get(url, timeout=10.0)
            
            # Raise the status response
            response.raise_for_status()

            # Parse the html
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title and link
            titles = [i.a.text for i in soup.find_all('div', class_='title')]
            links = [base_url+i.a['href'] for i in soup.find_all('div', class_='title')]

            return titles, links
        except Exception as e:
            print(f"Error fetching data for level {level}, page {page}: {e}")
            return [], []

# Define scrape_levels function
async def scrape_levels(levels):
    '''
    This function run several steps:
    1.  loops through levels and pages 
        then run the fetch_data function each loop
    2.  Write all data to csv files based on its level
    3.  Write skipped data to json file
    '''
    all_titles = []
    all_links = []
    skipped_pages = []

    # Loop through levels
    for level, max_page in enumerate(levels, start=1):
        level_titles = []
        level_links = []
        
        # loop through page
        for page in tqdm(range(1, max_page + 1), desc=f"Level {level}"):
        # for page in range(1, max_page + 1):
            
            # Fetch all data asynchronously
            titles, links = await fetch_data(level, page)

            # Append level and page to skipped_pages if title is null
            if not titles:
                skipped_pages.append({'level':level,'page': page})

            # Extend all data with their level groups
            level_titles.extend(titles)
            level_links.extend(links)

        # Create data frame from all pages each level
        df = DataFrame({'title':level_titles,'link':level_links})
        print(f'level = {level}',df.head())

        # Write the data frame to csv file in the specific directory
        filename = f"{output_directory}/forti_lists_{level}.csv"
        df.write_csv(filename)
    
    # write the skipped pages to json file in the specific directory
    skipped_filename = f"{output_directory}/skipped.json"
    with open(skipped_filename, 'w') as json_file:
        json.dump(skipped_pages, json_file)
    print('<==== skipped.json process completed ====>')

# Define main function
async def main():

    '''
    This function used to run several steps:
    1. Make directory if not exist
    2. Run scrape_levels async function then read it as polars dataframe. 
    '''

    # Make directory
    os.makedirs(output_directory, exist_ok=True)

    # Run scrape_levels function
    levels = max_pages
    await scrape_levels(levels)


if __name__ == "__main__":
    asyncio.run( main())