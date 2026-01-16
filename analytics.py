import json
import re
import pandas as pd
DB_PATH = "database.json"
def split_product_code(product_str: str) -> dict:
    match = re.match(r"^(\d+)\s+(.*)$", product_str.strip())
    if match:
        return {"codigo": int(match.group(1)), "nome": match.group(2).strip()}
    return {"codigo": None, "nome": product_str.strip()}

def run_analytics(db_path: str = DB_PATH):
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {"mensagem": "database.json não encontrado ou vazio"}

    df = pd.DataFrame(data)

    df_items = df.explode("items", ignore_index=True)
    df_items = df_items[df_items["items"].notna()]

    items_norm = pd.json_normalize(df_items["items"])
    df_items = pd.concat([df_items.drop(columns=["items"]), items_norm], axis=1)

    df_items["line_total"] = df_items["quantity"] * df_items["unit_price"]

    invoice_totals = df_items.groupby("order_id")["line_total"].sum()
    media_total = round(float(invoice_totals.mean()), 2)

    produto_mais_frequente_raw = df_items["product"].value_counts().index[0]
    produto_mais_frequente = split_product_code(produto_mais_frequente_raw)

    total_por_produto_series = (
        df_items.groupby("product")["line_total"]
        .sum()
        .sort_values(ascending=False)
    )

    total_gasto_por_produto = []
    for product_name, total in total_por_produto_series.items():
        info = split_product_code(product_name)
        total_gasto_por_produto.append({
            "codigo": info["codigo"],
            "produto": info["nome"],
            "total_gasto": round(float(total), 2)
        })
    products_list_df = (
        df_items[["product", "unit_price"]]
        .drop_duplicates()
        .sort_values(by=["product"])
    )
    lista_produtos = []
    for _, row in products_list_df.iterrows():
        info = split_product_code(row["product"])
        lista_produtos.append({
            "codigo": info["codigo"],
            "produto": info["nome"],
            "preco_unitario": round(float(row["unit_price"]), 2)
        })

    return {
        "media_valor_total_faturas": media_total,
        "produto_mais_frequente": produto_mais_frequente,
        "total_gasto_por_produto": total_gasto_por_produto,
        "lista_produtos_preco_unitario": lista_produtos
    }
