from playwright.sync_api import sync_playwright
from selectolax.lexbor import LexborHTMLParser
import csv
import time

# Function to navigate to Google Flights page and input departure and destination places
#Link shold be updated to the current desirable date and time. Also the currency should be updated to the US Dollar in the web page.
def get_page(page, from_place, to_place):
    page.goto('https://www.google.com/travel/flights?tfs=CBwQARobEgoyMDI1LTAxLTAxag0IAhIJL20vMDIxajM4GhsSCjIwMjUtMDEtMjJyDQgCEgkvbS8wMjFqMzhAAUgBcAGCAQsI____________AZgBAQ&tfu=KgIIAw&curr=USD')

    # Input departure place
    from_place_field = page.query_selector_all('.e5F5td')[0]
    from_place_field.click()
    time.sleep(1)
    from_place_field.type(from_place)
    time.sleep(1)
    page.keyboard.press('Enter')

    # Input destination place
    to_place_field = page.query_selector_all('.e5F5td')[1]
    to_place_field.click()
    time.sleep(1)
    to_place_field.type(to_place)
    time.sleep(1)
    page.keyboard.press('Enter')

    # Click on "Explore"
    page.query_selector('.MXvFbd .VfPpkd-LgbsSe').click()
    time.sleep(3)

    # Look for the "More flights" button
    more_flights_button = page.query_selector('.zISZ5c button')
    if more_flights_button:
        more_flights_button.click()
        time.sleep(2)
        parser = LexborHTMLParser(page.content())
        return parser
    else:
        print(f"More flights button not found for {from_place} to {to_place}.")
        return None

# Function to scrape flight data from Google Flights page
def scrape_google_flights(parser, from_place, to_place):
    lowest_price = float('inf')  # Initialize with positive infinity
    lowest_price_flight = None

    categories = parser.root.css('.zBTtmb')
    category_results = parser.root.css('.Rk10dc')

    for category, category_result in zip(categories, category_results):
        for result in category_result.css('.yR1fYc'):
            company = result.css_first('.Ir0Voe .sSHqwe').text()
            duration = result.css_first('.AdWm1c.gvkrdb').text()
            stops = result.css_first('.EfT7Ae .ogfYpf').text()
            emissions = result.css_first('.V1iAHe .AdWm1c').text()
            emission_comparison = result.css_first('.N6PNV').text()
            price_text = result.css_first('.U3gSDe .FpEdX span').text()
            Trip_type = result.css_first('.U3gSDe .N872Rd').text()

            # Convert price to float for comparison
            price = float(price_text.replace('$', '').replace(',', ''))

            # Update lowest price if found
            if price < lowest_price:
                lowest_price = price
                lowest_price_flight = {
                    'from': from_place,
                    'to': to_place,
                    'company': company,
                    'duration': duration,
                    'stops': stops,
                    'emissions': emissions,
                    'emission_comparison': emission_comparison,
                    'price': price_text,
                    'Trip_type': Trip_type
                }

    return lowest_price_flight

# Main function to orchestrate the scraping process
def run(playwright, states, countries):
    all_data = []

    browser = playwright.chromium.launch(headless=False)

    try:
        # Iterate through all combinations of departure and destination places
        for from_place in states:
            for to_place in countries:
                try:
                    page = browser.new_page()
                    parser = get_page(page, from_place, to_place)
                    
                    if parser:
                        lowest_price_flight = scrape_google_flights(parser, from_place, to_place)

                        if lowest_price_flight:
                            # Append the lowest price flight data to the list
                            all_data.append(lowest_price_flight)
                            print(f"Lowest price found for {from_place} to {to_place}: {lowest_price_flight['price']}")
                        else:
                            print(f"No flight data found for {from_place} to {to_place}.")
                    else:
                        print(f"Skipping {from_place} to {to_place} due to an error.")
                finally:
                    page.close()

                time.sleep(4)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        browser.close()

        # Save the data to CSV file
        if all_data:
            csv_columns = ['from', 'to', 'company', 'duration', 'stops', 'emissions', 'emission_comparison', 'price', 'Trip_type']
            csv_file = 'lowest_price_flights.csv'
            with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in all_data:
                    writer.writerow(data)
            print(f"Data saved to {csv_file}")
        else:
            print("No data found.")

if __name__ == "__main__":
    with sync_playwright() as playwright:
        # Complete lists of states and countries
        states = ['Toronto', 'Montréal', 'Vancouver']
        countries = ['Ireland', 'United Kingdom']

        run(playwright, states, countries)
