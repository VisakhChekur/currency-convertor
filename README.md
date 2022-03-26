# Currency Convertor

A simple CLI-based currency convertor using the <a href="https://www.currencyconverterapi.com/">Currency Convertor API</a>.

To view all the countries and their corresponding currencies, run the following command:

`python3 convertor.py -c list`

OR

`python3 convertor.py --command list`


To do a currency conversion, run the following command:

`python3 convertor.py <amount to convert> <currency code 1> <currency code 2>`

- `currency code 1` - currency code of the currency the amount is originally in
- `currency code 2` - currency code of the currency the amount is to be converted to
