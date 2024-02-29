# Google Flights Scraper

## Overview

This project provides a Python script for scraping flight data from Google Flights using the Playwright library. It enables users to find the lowest price flights between specified departure and destination places.

## Features

- Scrapes flight data such as company, duration, stops, emissions, price, and more from Google Flights.
- Supports specifying departure places (states) and destination places (countries).
- Saves the scraped data to a CSV file for further analysis.

## Code Overview

### 1. Google Flights Scraper Functions:

- `get_page(page, from_place, to_place)`: Navigates to the Google Flights webpage, inputs the departure and destination places, and retrieves the HTML content of the page for parsing.
- `scrape_google_flights(parser, from_place, to_place)`: Parses the HTML content using the Selectolax library to extract flight data such as company, duration, stops, emissions, and price. It then identifies the flight with the lowest price among the search results.

### 2. Main Function:

- `run(playwright, states, countries)`: Orchestrates the scraping process by iterating over all combinations of departure places (`states`) and destination places (`countries`). It launches a browser instance using Playwright, scrapes flight data for each combination, saves the data to a CSV file, and handles any errors that may occur during the process.

### 3. Error Handling:

- The script includes error handling mechanisms to catch and print any exceptions that may occur during the scraping process. This ensures graceful handling of errors without interrupting the overall execution of the script.

### 4. CSV Data Export:

- After scraping flight data for all combinations of departure and destination places, the script saves the collected data to a CSV file named `lowest_price_flights.csv`. This file contains columns for various flight attributes such as company, duration, stops, emissions, price, and price type.

### 5. Dependencies:

- The script relies on external libraries such as Playwright and Selectolax for browser automation and HTML parsing, respectively. These dependencies are specified in the `requirements.txt` file for easy installation.

### 6. Visual Studio Code Integration:

- The project is designed to be run and edited using Visual Studio Code, a popular integrated development environment (IDE) for Python development. Users can leverage features such as code editing, debugging, and version control directly within Visual Studio Code.

### 7. Adjustable Parameters:

- Users can customize the list of departure places (`states`) and destination places (`countries`) based on their preferences. They can also adjust the sleep intervals within the code to optimize the scraping process for their specific environment or network conditions.

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/edgeofmri/google-flights-scraper.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Open the project folder in Visual Studio Code:

```bash
code google-flights-scraper
```

## Usage

1. Modify the `states` and `countries` lists in the `main.py` file to specify the departure places and destination places, respectively.
2. Run the script by executing the `main.py` file. You can do this by clicking the "Run" button in Visual Studio Code or by running the following command in the terminal:

```bash
python main.py
```

3. Wait for the script to complete the scraping process. It will print the lowest price flights found for each combination of departure and destination places.
4. Once the scraping is finished, the scraped data will be saved to a CSV file named `lowest_price_flights.csv` in the project directory.

## Notes

- This script utilizes Playwright to automate the Chromium browser for scraping Google Flights data. Make sure to have a compatible version of Chromium installed on your system.
- Adjust the `time.sleep()` intervals in the code as needed to accommodate for slower internet connections or longer loading times on the Google Flights website.
