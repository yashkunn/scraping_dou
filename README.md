# DOUBot: Scraping and Analysis of Job Vacancies from Dou.ua

## Project Description

This project collects job vacancy data from the [jobs.dou.ua](https://jobs.dou.ua) website in the Python category, processes the data, and analyzes the frequency of technology mentions within job descriptions. The project uses `Scrapy` and `Selenium` for data scraping, along with `Pandas` and `Matplotlib` for data analysis and visualization.

### Key Components
- **Job Vacancy Scraper**: `dou_spider.py` collects job titles, company names, salary information, job descriptions, and technologies listed.
- **Technology Analysis**: Analyzes the frequency of each technology mentioned in job postings.
- **Visualization**: Generates a chart to display the technology frequencies for easy interpretation.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yashkunn/scraping_dou.git
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

    Key dependencies include:
    - `Scrapy`: for web scraping.
    - `Selenium`: for browser automation.
    - `webdriver_manager`: for automatic installation of the Chrome driver.
    - `Pandas`, `Matplotlib`, `Seaborn`: for data processing and visualization.

## Usage

1. **Run the Scraper**:
    Execute `dou_spider.py` to scrape data from Dou.ua:
    ```bash
    scrapy crawl dou -o vacancy.csv
    ```

    The scraper will open the job listings page, click the "More" button to load additional vacancies, and collect details for each job.

2. **Analyze Data**:
    To analyze and visualize the collected data, open the `analysis_vacancies.ipynb` Jupyter Notebook and run all cells. The notebook will generate a chart showing the frequency of each technology mentioned in the job descriptions.


## Project Structure

- `dou_spider.py` – main script for scraping with `Scrapy` and `Selenium`.
- `analyze_technologies.py` – script for data analysis and visualization.
- `requirements.txt` – list of dependencies.
- `vacancy.csv` – collected job data (automatically generated after running the scraper).

## Technical Details

- **Scrapy** is used to manage data collection and parse HTML pages.
- **Selenium** automates clicking the "More" button to load all job listings.
- **Pandas** is used for data processing, counting technology mentions.
- **Matplotlib and Seaborn** are used to create visualizations.

## Notes

- To run Selenium with Chrome, make sure Chrome is installed on your machine.