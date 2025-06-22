import requests
from bs4 import BeautifulSoup
import csv
import argparse
import pandas as pd

def scrape_books(page_limit):
    book_data = []

    for page_num in range(1, page_limit + 1):
        url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
        print(f"Scraping {url} ...")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]

            raw_price = book.find("p", class_="price_color").text
            price = float(raw_price.replace("Â£", "").replace("£", ""))

            rating_tag = book.find("p", class_="star-rating")
            rating_classes = rating_tag.get("class", [])
            rating = rating_classes[1] if len(rating_classes) > 1 else "Unknown"

            book_data.append([title, price, rating])

    return book_data

def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Price (GBP)", "Rating"])
        writer.writerows(data)
    print(f"✅ Saved to {filename}")

def save_to_excel(data, filename):
    df = pd.DataFrame(data, columns=["Title", "Price (GBP)", "Rating"])
    df.to_excel(filename, index=False)
    print(f"✅ Saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="📚 Scrape book data from books.toscrape.com")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape (default: 1)")
    parser.add_argument("--format", choices=["csv", "excel"], default="csv", help="Output file format (csv or excel)")
    args = parser.parse_args()

    data = scrape_books(args.pages)

    if args.format == "csv":
        save_to_csv(data, "books_output.csv")
    elif args.format == "excel":
        save_to_excel(data, "books_output.xlsx")

if __name__ == "__main__":
    main()
