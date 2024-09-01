import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

# Function to scrape jobs from LinkedIn
def scrape_jobs(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        st.error("Failed to retrieve the page. Please check the URL.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs_data = []

    # Find job cards
    job_cards = soup.find_all('div', class_='job-search-card')

    for job in job_cards:
        title = job.find('h3', class_='base-search-card__title').text.strip() if job.find('h3', class_='base-search-card__title') else 'N/A'
        company = job.find('h4', class_='base-search-card__subtitle').text.strip() if job.find('h4', class_='base-search-card__subtitle') else 'N/A'
        location = job.find('span', class_='job-search-card__location').text.strip() if job.find('span', class_='job-search-card__location') else 'N/A'
        link = job.find('a', class_='base-card__full-link')['href'] if job.find('a', class_='base-card__full-link') else 'N/A'

        jobs_data.append({
            'title': title,
            'company': company,
            'location': location,
            'link': link
        })

    return jobs_data

# Streamlit UI
st.title("LinkedIn Job Scraper")

url = st.text_input("Enter LinkedIn Jobs Page URL:")

if st.button("Scrape Jobs"):
    if url:
        with st.spinner("Scraping..."):
            jobs = scrape_jobs(url)

        if jobs:
            # Convert to DataFrame
            df = pd.DataFrame(jobs)

            # Show the DataFrame on the UI
            st.write(df)

            # Download buttons and options
            csv = df.to_csv(index=False).encode('utf-8')
            json_data = df.to_json(orient='records')

            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='linkedin_jobs.csv',
                mime='text/csv'
            )

            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name='linkedin_jobs.json',
                mime='application/json'
            )
    else:
        st.error("Please enter a valid LinkedIn jobs page URL.")