import requests
from bs4 import BeautifulSoup
import cssutils
from collections import defaultdict
import sys

def get_stylesheets(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    stylesheets = []

    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href")
        if href.startswith("http"):
            stylesheets.append(href)
        else:
            stylesheets.append(url + href)

    return stylesheets

def extract_font_and_color(css_rules):
    fonts = defaultdict(int)
    colors = defaultdict(int)

    for rule in css_rules:
        if isinstance(rule, cssutils.css.CSSStyleRule):
            style = rule.style

            if "font-family" in style:
                font = style["font-family"]
                fonts[font] += 1

            if "color" in style:
                color = style["color"]
                colors[color] += 1

    return fonts, colors

def calculate_percentage(dictionary):
    total = sum(dictionary.values())
    percentage_dict = {k: (v / total) * 100 for k, v in 
dictionary.items()}
    return percentage_dict

def main(url):
    stylesheets = get_stylesheets(url)

    fonts = defaultdict(int)
    colors = defaultdict(int)

    for stylesheet in stylesheets:
        response = requests.get(stylesheet)
        parsed_css = cssutils.parseString(response.content)
        temp_fonts, temp_colors = extract_font_and_color(parsed_css)
        
        for font, count in temp_fonts.items():
            fonts[font] += count
        for color, count in temp_colors.items():
            colors[color] += count

    font_percentage = calculate_percentage(fonts)
    color_percentage = calculate_percentage(colors)

    print("Fonts and their percentage usage:")
    for font, percentage in font_percentage.items():
        print(f"{font}: {percentage:.2f}%")

    print("\nColors and their percentage usage:")
    for color, percentage in color_percentage.items():
        print(f"{color}: {percentage:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    main(url)

