import os
import requests
from tabulate import tabulate

# constants
API_KEY = os.environ.get("CURRENCY_CONVERTOR_API")
BASE_URL = "https://free.currconv.com/"

# ----- getting all countries and printing their details -----


def print_countries_and_currencies():
    """Prints the countries, their currency name and the currency code."""
    countries = get_all_countries()
    if countries:
        output = create_output_list(countries)
        header_row = ["COUNTRY", "CURRENCY", "CURRENCY CODE"]
        print(tabulate(output, headers=header_row, tablefmt="grid",
                       showindex=range(1, len(countries) + 1)))


def get_all_countries():
    """Gets a list of all the countries."""
    endpoint = f"api/v7/countries?apiKey={API_KEY}"
    response = requests.get(BASE_URL + endpoint)
    if response.status_code != 200:
        display_error(response.status_code)
        return None
    data = response.json()['results']
    return list(data.items())


def create_output_list(countries):
    output = []
    for country in countries:
        details = country[1]
        country_name = details['name']
        currency = details['currencyName']
        currency_code = details['currencyId']
        output.append([country_name, currency, currency_code])
    return sorted(output)


# ----- converts the currency and displays it -----
def convert_currency(amt_to_convert, codes):

    rates = get_exchange_rate(codes)
    if rates:
        converted_amt = get_converted_amt(amt_to_convert, codes, rates)
        print_converted_currency(amt_to_convert, converted_amt, codes)


def get_exchange_rate(codes):
    """Gets the exchange rate for the given currency codes."""
    query = f"{codes[0]}_{codes[1]},{codes[1]}_{codes[0]}"
    endpoint = f"api/v7/convert?q={query}&compact=ultra&apiKey={API_KEY}"
    response = requests.get(BASE_URL + endpoint)

    # error handling
    if response.status_code != 200:
        display_error(error_type="response error", error=response.status_code)
        return None
    elif not response.json():
        display_error("invalid input")
        return None

    return response.json()


def get_converted_amt(amount, codes, exchange_rate):
    """Converts the currency from the given amount based on the exchange rate. The amount is converted FROM the first currency code TO the second currency code. That is, if codes is [USD, INR] and amount is 10, then the returned value would be the value of 10 USD in INR."""

    key = f"{codes[0]}_{codes[1]}"
    rate = exchange_rate[key]
    return amount * rate


def print_converted_currency(amt_to_convert, converted_amt, codes):
    """Prints the converted amount in a formatted manner."""
    amt_to_convert = format_amount(int(amt_to_convert))
    converted_amt = format_amount(int(converted_amt))
    output = f"{amt_to_convert} {codes[0]} = {converted_amt} {codes[1]}"

    print("-"*len(output))
    print(output)
    print("-"*len(output))


def format_amount(amt):
    """Format the given amount in human readable format. That is 1000 would become 1,000."""
    amt = str(amt)
    formatted_amt = ""
    i = 1
    for char in amt[::-1]:
        if i % 4 == 0:
            formatted_amt += ","
            i += 1
        formatted_amt += char
        i += 1
    return formatted_amt[::-1]


def display_error(error_type, error=None):
    if error_type == "response error":
        print(f"\nError: {error}")
    else:
        print("\nInvalid currency codes.")
