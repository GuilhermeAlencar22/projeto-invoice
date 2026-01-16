import os
import re
import json
from datetime import datetime
from typing import List, Dict, Any
import pdfplumber
from models import Invoice, Item

DB_PATH = "database.json"
PDF_DIR = "data/invoices"
def load_db(db_path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(db_path):
        return []
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def save_db(db_path: str, data: List[Dict[str, Any]]) -> None:
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def extract_text(pdf_path: str) -> str:
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join((page.extract_text() or "") for page in pdf.pages)


def extract_field(text: str, pattern: str) -> str | None:
    m = re.search(pattern, text, flags=re.IGNORECASE)
    return m.group(1).strip() if m else None


def extract_items(text: str) -> List[Item]:
    items = []
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    item_pattern = re.compile(r"^(.*?)\s+(\d+)\s+(\d+(?:\.\d+)?)$")
    for ln in lines:
        m = item_pattern.match(ln)
        if not m:
            continue
        product = m.group(1).strip()
        quantity = int(m.group(2))
        unit_price = float(m.group(3))

        try:
            items.append(Item(product=product, quantity=quantity, unit_price=unit_price))
        except Exception:
            pass

    return items


def parse_invoice(pdf_path: str) -> Invoice:
    text = extract_text(pdf_path)
    order_id = extract_field(text, r"Order\s*ID\s*[:#]?\s*(\d+)")
    customer_id = extract_field(text, r"Customer\s*ID\s*[:#]?\s*([A-Z0-9]+)")
    order_date_raw = extract_field(text, r"Order\s*Date\s*[:#]?\s*(\d{4}-\d{2}-\d{2})")

    if not order_id or not customer_id or not order_date_raw:
        raise ValueError("Não conseguiu extrair campos principais")

    order_date = datetime.strptime(order_date_raw, "%Y-%m-%d").date()
    items = extract_items(text)

    if not items:
        raise ValueError("Não conseguiu extrair")
    return Invoice(
        order_id=str(order_id),
        order_date=order_date,
        customer_id=customer_id,
        items=items
    )

def run_ingestion(pdf_dir: str = PDF_DIR, db_path: str = DB_PATH) -> Dict[str, Any]:
    db = load_db(db_path)
    existing_ids = {inv["order_id"] for inv in db}

    inserted = 0
    skipped = 0
    errors = 0

    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    pdf_files = [os.path.join(pdf_dir, f) for f in pdf_files]

    for pdf_path in pdf_files:
        try:
            invoice = parse_invoice(pdf_path)
            if invoice.order_id in existing_ids:
                skipped += 1
                continue
            db.append(invoice.model_dump(mode="json"))
            existing_ids.add(invoice.order_id)
            inserted += 1

        except Exception:
            errors += 1

    save_db(db_path, db)

    return {
        "found_pdfs": len(pdf_files),
        "inserted": inserted,
        "skipped_duplicates": skipped,
        "errors": errors
    }
