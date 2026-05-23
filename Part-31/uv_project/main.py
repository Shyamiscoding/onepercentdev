# 1. MODULE — importing from a single .py file in the same folder
from my_module import print_separator, format_currency, greet

# 2. PACKAGE — importing from a folder (my_package/) that has __init__.py
from my_package import clean_text, count_words, reverse_words

# 3. LIBRARY — importing a third-party package installed via uv
import requests


def demo_module():
    print_separator("MODULE Demo")
    print(greet("Learner"))
    print(f"Price: {format_currency(49999)}")


def demo_package():
    print_separator("PACKAGE Demo")
    raw_text = "  Python Is AMAZING for Building REAL Projects  "
    print(f"Original:  '{raw_text}'")
    print(f"Cleaned:   '{clean_text(raw_text)}'")
    print(f"Words:     {count_words(raw_text)}")
    print(f"Reversed:  '{reverse_words(raw_text.strip())}'")


def demo_library():
    print_separator("LIBRARY Demo (requests)")
    url = "https://httpbin.org/get"
    print(f"Fetching data from: {url}")
    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    data = response.json()
    print(f"Your IP:     {data.get('origin', 'unknown')}")
    print(f"\nOne line of code (requests.get) fetched live data from the internet.")
    print(f"The 'requests' library handled all the networking for us.")


if __name__ == "__main__":
    print_separator("Module vs Package vs Library")
    print("This project is managed with UV.\n")
    print("  1. MODULE  → my_module.py        (a single file you wrote)")
    print("  2. PACKAGE → my_package/          (a folder you organized)")
    print("  3. LIBRARY → requests             (installed via: uv add requests)\n")

    demo_module()
    demo_package()
    demo_library()
