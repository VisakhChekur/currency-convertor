import argparse
from currency import convert_currency, print_countries_and_currencies


def add_args(parser):
    # amount
    parser.add_argument(
        "amt",
        help="the amount you want to enter",
        type=float)
    # first currency code
    parser.add_argument(
        "code_1",
        help="currency code of the amount you want to convert from")
    # second currency code
    parser.add_argument(
        "code_2",
        help="currency code of the amount you want to convert to")


def get_args(parser):
    args = parser.parse_args()
    codes = [args.code_1.upper(), args.code_2.upper()]
    return args.amt, codes


def main():
    parser = argparse.ArgumentParser()
    # command
    parser.add_argument(
        "-c", "--command",
        help="enter the command you want to perform",
        default="convert",
        choices=["list", "convert"])

    args = parser.parse_known_args()

    if args[0].command == "list":
        print_countries_and_currencies()
    else:
        convert_parser = argparse.ArgumentParser()
        add_args(convert_parser)
        amt, codes = get_args(convert_parser)
        convert_currency(amt, codes)


if __name__ == "__main__":
    main()
