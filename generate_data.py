from __future__ import annotations

import argparse
import csv
import json
import random
import re
import uuid
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path 

GENERATOR_VERSION = "1.0.0"
IST = timezone(timedelta(hours=5, minutes=30))

STORES = [
    ("S01", "Jaipur"), ("SO2", "Delhi"), ("S03", "Delhi"), ("SO4", "Mumbai"),
    ("S05", "Bengaluru"), ("S06", "Hyderabad"), ("S07", "Pune"), 
    ("S08", "Chennai"), ("S09", "Kolkata"),
]
CITY_PINCODES = {
    "Jaipur": ["302001", "302017", "302020"],
    "Delhi": ["110001", "110016"], ["110024"],
    "Bengaluru": ["560001", "560034", "560102"],
    "Hyderabad": ["500001", "500032", "500081"],
    "Pune": ["411001", "411045"],
    "Chennai": ["600001", "600042"],
    "Kolkata": ["700001", "700091"],
}

STORES_BY_CITY: dict[str, list[str]] = defaultdict(list)
for _sid, _city in STORES:
    STORES_BY_CITY[_city].append(_sid)
CITITES = sorted(CITY_PINCODES)

_PRODUCT_SEED = [
     ("Toned Milk 500ml", "Dairy & Eggs", 30), ("Curd 400g", "Dairy & Eggs", 45),
    ("Paneer 200g", "Dairy & Eggs", 90), ("Eggs 6 pack", "Dairy & Eggs", 60),
    ("Onion 1kg", "Fruits & Vegetables", 40), ("Tomato 500g", "Fruits & Vegetables", 30),
    ("Banana 6 pcs", "Fruits & Vegetables", 50), ("Apple 4 pcs", "Fruits & Vegetables", 140),
    ("Potato Chips 52g", "Snacks", 20), ("Namkeen Mix 200g", "Snacks", 55),
    ("Biscuits 75g", "Snacks", 25), ("Instant Noodles 70g", "Snacks", 14),
    ("Cola 750ml", "Beverages", 40), ("Tea 250g", "Beverages", 130),
    ("Cold Coffee 200ml", "Beverages", 60), ("Atta 5kg", "Staples", 250),
    ("Basmati Rice 1kg", "Staples", 80), ("Toor Dal 1kg", "Staples", 160),
    ("Sunflower Oil 1L", "Staples", 140), ("Bath Soap 4 pack", "Personal Care", 150),
    ("Shampoo 180ml", "Personal Care", 170), ("Toothpaste 150g", "Personal Care", 95),
    ("Dish Wash 500ml", "Household", 110), ("Detergent 1kg", "Household", 120),
    ("Floor Cleaner 1L", "Household", 175),
]
PRODUCTS = [
    (f"P{i + 1:03d}", name, cat, float(mrp)) for i, (name, cat, mrp) in enumerate(_PRODUCT_SEED)
]

TIERS = ["bronze", "silver", "gold"]
PAYMENT_METHODS = ["upi", "card", "cod", "wallet"]
PAYMENT_WEIGHTS = [0.60, 0.15, 0.15, 0.10]
STATUSES = ["delivered", "cancelled", "rejected_out_of_stock"]
STATUS_WEIGHTS = [0.92, 0.05, 0.03]
PROMISED_MINUTES = [10, 15, 20]
PROMISED_WEIGHTS = [0.30, 0.50, 0.20]
DEVICES = ["android", "ios", "web"]
DEVICE_WEIGHTS = [0.62, 0.28, 0.10]
COUPONS = ["WELCOME50", "FRESH10", "SNACKTIME", "WEEKEND15"]

HOUR_WEIGHTS = [1, 1, 1, 1, 1, 2, 3, 5, 7, 6, 5, 5, 6, 6, 5, 5, 6, 8, 10, 11, 10, 8, 5, 2]

P_SEARCH, P_VIEW, P_CART, P_CHECKOUT, P_ORDER = 0.60, 0.80, 0.35, 0.55, 0.85
OVERALL_CONVERSION = P_VIEW * P_CART * P_CHECKOUT * P_ORDER

PINCODE_RULE = re.compile(r"^[1-9][0-9]{5}$")
BAD_PINCODES = ["000000", "12345", "ABCDEF", "", "9999999"]

def is_valid_pincode(value: object) -> bool:
    return isinstance(value, str) and bool(PINCODE_RULE.match(value))

