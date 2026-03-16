"""
OffreSolaire scraping utilities.

This module defines simple web scrapers for a selection of solar kit vendors.  Each
scraper retrieves public product data such as the kit name, current price,
estimated power (kWc) and battery capacity when available.  The results can
then be inserted into the database defined in `schema.sql`.

Note:  The scrapers are designed to run from a trusted environment where
network access is permitted.  In this sandbox some sites may be unreachable,
so the functions are primarily illustrative and may need adjustments in
production.

Dependencies:
  - requests
  - beautifulsoup4
  - python-dateutil (optional)

Usage:
  from scraper import fetch_materfrance, fetch_monkitsolaire
  offers = fetch_materfrance()
  for offer in offers:
      print(offer)

Each function returns a list of dictionaries with the following keys:
  - title: Name of the kit
  - price: Price as a float in euros
  - link: URL to the product page
  - power_kwc: Nominal power of the kit (kWc) if parsed else None
  - battery_kwh: Battery capacity (kWh) if parsed else None
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

@dataclass
class Offer:
    title: str
    price: float
    link: str
    power_kwc: Optional[float] = None
    battery_kwh: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "price": self.price,
            "link": self.link,
            "power_kwc": self.power_kwc,
            "battery_kwh": self.battery_kwh,
        }


def _parse_price(text: str) -> Optional[float]:
    """Extract a float price from a string containing a price with French
    formatting (e.g. "1 529,00 €").  Returns None if no price found."""
    if not text:
        return None
    # Remove non‑digit separators except comma and dot
    cleaned = text.strip()
    # Replace non-breaking spaces with normal space
    cleaned = cleaned.replace('\u202f', ' ').replace('\xa0', ' ')
    # Extract number part
    match = re.search(r"([0-9][0-9\s.,]+)", cleaned)
    if not match:
        return None
    number_str = match.group(1)
    # Remove spaces and thousands separators
    number_str = number_str.replace(' ', '').replace('\xa0', '').replace(',', '.')
    try:
        return float(number_str)
    except ValueError:
        return None


def _parse_power_kwc(text: str) -> Optional[float]:
    """Extract the power in kWc from a kit name or description.
    Searches for patterns like "1000W" or "1 kWc" and returns the
    equivalent float in kilowatts-peak.  Returns None if not found."""
    if not text:
        return None
    text_lower = text.lower().replace(',', '.').replace(' ', '')
    # Pattern: e.g. 1000w, 1000wc, 1kwc
    match = re.search(r"(\d+(?:\.\d+)?)(k?w)c?", text_lower)
    if match:
        value = float(match.group(1))
        # If no explicit unit given, treat numbers >100 as watts and convert to kW
        if 'k' in match.group(0):
            # Already kW
            return value
        # Value appears to be W
        return value / 1000.0
    return None


def fetch_materfrance() -> List[Offer]:
    """Scrape Mater France's plug‑and‑play kit listings.

    The page lists multiple products with names and prices.  This function
    returns a list of Offer objects for all listed products.
    """
    url = "https://materfrance.fr/categorie-produit/kits-plug-and-play/"
    offers: List[Offer] = []
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching Mater France page: {e}")
        return offers
    soup = BeautifulSoup(resp.text, "html.parser")
    # Each product card is within article.product or li.product
    product_elems = soup.select("li.product, article.product")
    for elem in product_elems:
        # Title is often in h3 or h2 tag or a tag with class 'woocommerce-loop-product__title'
        title_elem = elem.select_one(".woocommerce-loop-product__title, h2, h3")
        if not title_elem:
            continue
        title = title_elem.get_text(strip=True)
        # Link is in <a href="..."><img> or similar
        link_elem = elem.find("a", href=True)
        link = link_elem["href"] if link_elem else url
        # Price is in span.price or span.woocommerce-Price-amount
        price_elem = elem.select_one("span.price, .woocommerce-Price-amount")
        price = None
        if price_elem:
            # Remove nested <del> old prices
            # Choose the last <span class="woocommerce-Price-amount">
            # Some products show sale prices with <del> and <ins>
            ins_price = price_elem.find("ins")
            if ins_price:
                amount = ins_price.get_text()
            else:
                amount = price_elem.get_text()
            price = _parse_price(amount)
        power_kwc = _parse_power_kwc(title)
        offers.append(Offer(title=title, price=price or 0.0, link=link, power_kwc=power_kwc))
    return offers


def fetch_monkitsolaire() -> List[Offer]:
    """Scrape Mon Kit Solaire's plug‑and‑play kit listings.

    Returns a list of Offer objects.
    """
    url = "https://www.monkitsolaire.fr/213-kit-solaire-plug-and-play"
    offers: List[Offer] = []
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching Mon Kit Solaire page: {e}")
        return offers
    soup = BeautifulSoup(resp.text, "html.parser")
    # The site uses product-miniature class for each product card
    product_elems = soup.select("div.product-miniature")
    for elem in product_elems:
        # Title in h2.product-title or a[data-qa="product-name"]
        title_elem = elem.select_one("h2.product-title a, a.product-name")
        if not title_elem:
            continue
        title = title_elem.get_text(strip=True)
        link = title_elem["href"]
        # Price is inside span.price, may include crossed-out old price
        price_elem = elem.select_one("span.price")
        price = None
        if price_elem:
            # Choose the first number string in the price element
            amount = price_elem.get_text()
            price = _parse_price(amount)
        power_kwc = _parse_power_kwc(title)
        offers.append(Offer(title=title, price=price or 0.0, link=link, power_kwc=power_kwc))
    return offers


if __name__ == "__main__":
    # Example usage: fetch offers and print them
    print("Fetching Mater France offers...")
    mf_offers = fetch_materfrance()
    for offer in mf_offers[:5]:
        print(offer.to_dict())
    print("Fetching Mon Kit Solaire offers...")
    mks_offers = fetch_monkitsolaire()
    for offer in mks_offers[:5]:
        print(offer.to_dict())