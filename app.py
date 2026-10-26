# from flask import Flask, jsonify, request, render_template
# import json, sqlite3
# from pathlib import Path

# BASE = Path(__file__).resolve().parent
# DB_PATH = BASE / 'giftmatch.db'
# SEED_PATH = BASE / 'seed_products.json'
# app = Flask(__name__)


# def connect():
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn


# def init_db():
#     with connect() as db:
#         db.execute('''CREATE TABLE IF NOT EXISTS products (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             image TEXT NOT NULL DEFAULT '',
#             category TEXT NOT NULL DEFAULT 'gift',
#             occasions TEXT NOT NULL DEFAULT '[]',
#             price REAL,
#             quality TEXT NOT NULL DEFAULT 'standard',
#             delivery_days INTEGER NOT NULL DEFAULT 7,
#             description TEXT NOT NULL DEFAULT '',
#             personalize INTEGER NOT NULL DEFAULT 0,
#             details TEXT NOT NULL DEFAULT '',
#             active INTEGER NOT NULL DEFAULT 1,
#             created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
#         )''')
#         count = db.execute('SELECT COUNT(*) FROM products').fetchone()[0]
#         if count == 0 and SEED_PATH.exists():
#             products = json.loads(SEED_PATH.read_text(encoding='utf-8'))
#             for p in products:
#                 db.execute('''INSERT INTO products
#                     (id,name,image,category,occasions,price,quality,delivery_days,description,personalize,details)
#                     VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
#                     (p['id'], p['name'], p.get('image',''), p.get('category','gift'),
#                      json.dumps(p.get('occasions',[])), p.get('price'), p.get('quality','standard'),
#                      p.get('delivery_days',7), p.get('description',''), int(p.get('personalize',False)),
#                      p.get('details','')))


# def serialize(row):
#     p = dict(row)
#     p['occasions'] = json.loads(p['occasions'] or '[]')
#     p['personalize'] = bool(p['personalize'])
#     p.pop('active', None)
#     p.pop('created_at', None)
#     return p


# @app.get('/')
# def home():
#     return render_template('index.html')


# @app.get('/api/products')
# def get_products():
#     with connect() as db:
#         rows = db.execute('SELECT * FROM products WHERE active=1 ORDER BY id').fetchall()
#     return jsonify([serialize(row) for row in rows])


# @app.get('/api/products/<int:product_id>')
# def get_product(product_id):
#     with connect() as db:
#         row = db.execute('SELECT * FROM products WHERE id=? AND active=1', (product_id,)).fetchone()
#     if row is None:
#         return jsonify({'error': 'Product not found'}), 404
#     return jsonify(serialize(row))


# @app.post('/api/products')
# def add_product():
#     data = request.get_json(silent=True) or {}
#     if not str(data.get('name','')).strip():
#         return jsonify({'error': 'Product name is required'}), 400
#     with connect() as db:
#         cur = db.execute('''INSERT INTO products
#             (name,image,category,occasions,price,quality,delivery_days,description,personalize,details)
#             VALUES (?,?,?,?,?,?,?,?,?,?)''', (
#             str(data['name']).strip(), data.get('image',''), data.get('category','gift'),
#             json.dumps(data.get('occasions',[])), data.get('price'), data.get('quality','standard'),
#             int(data.get('delivery_days',7)), data.get('description',''),
#             int(bool(data.get('personalize',False))), data.get('details','')))
#         row = db.execute('SELECT * FROM products WHERE id=?', (cur.lastrowid,)).fetchone()
#     return jsonify(serialize(row)), 201


# @app.put('/api/products/<int:product_id>')
# def update_product(product_id):
#     data = request.get_json(silent=True) or {}
#     allowed = {'name','image','category','occasions','price','quality','delivery_days','description','personalize','details'}
#     with connect() as db:
#         existing = db.execute('SELECT * FROM products WHERE id=? AND active=1', (product_id,)).fetchone()
#         if existing is None:
#             return jsonify({'error': 'Product not found'}), 404
#         current = serialize(existing)
#         current.update({k:v for k,v in data.items() if k in allowed})
#         db.execute('''UPDATE products SET name=?,image=?,category=?,occasions=?,price=?,quality=?,delivery_days=?,description=?,personalize=?,details=? WHERE id=?''',
#             (current['name'],current['image'],current['category'],json.dumps(current['occasions']),current['price'],current['quality'],current['delivery_days'],current['description'],int(bool(current['personalize'])),current['details'],product_id))
#         row = db.execute('SELECT * FROM products WHERE id=?', (product_id,)).fetchone()
#     return jsonify(serialize(row))


# @app.delete('/api/products/<int:product_id>')
# def delete_product(product_id):
#     with connect() as db:
#         cur = db.execute('UPDATE products SET active=0 WHERE id=? AND active=1', (product_id,))
#     if cur.rowcount == 0:
#         return jsonify({'error': 'Product not found'}), 404
#     return jsonify({'deleted': True, 'id': product_id})


# if __name__ == '__main__':
#     init_db()
#     print('GiftMatch is running at http://127.0.0.1:5000')
#     app.run(host='127.0.0.1', port=5000, debug=False)








from flask import Flask, jsonify, request, render_template
import json
from pathlib import Path
from threading import Lock

BASE = Path(__file__).resolve().parent
SEED_PATH = BASE / "seed_products.json"

app = Flask(__name__)
file_lock = Lock()


def load_products():
    """Load products directly from seed_products.json."""
    if not SEED_PATH.exists():
        return []

    with file_lock:
        with SEED_PATH.open("r", encoding="utf-8") as file:
            products = json.load(file)

    if not isinstance(products, list):
        raise ValueError("seed_products.json must contain a JSON array")

    return products


def save_products(products):
    """Save product changes back to seed_products.json."""
    with file_lock:
        temp_path = SEED_PATH.with_suffix(".tmp")
        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(products, file, indent=2, ensure_ascii=False)
        temp_path.replace(SEED_PATH)


def serialize(product):
    """Return a consistent product object."""
    return {
        **product,
        "occasions": product.get("occasions", []),
        "personalize": bool(product.get("personalize", False)),
    }


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/products")
def get_products():
    products = load_products()
    return jsonify([
        serialize(product)
        for product in products
        if product.get("active", True)
    ])


@app.get("/api/products/<int:product_id>")
def get_product(product_id):
    products = load_products()

    for product in products:
        if (
            product.get("id") == product_id
            and product.get("active", True)
        ):
            return jsonify(serialize(product))

    return jsonify({"error": "Product not found"}), 404


@app.post("/api/products")
def add_product():
    data = request.get_json(silent=True) or {}

    if not str(data.get("name", "")).strip():
        return jsonify({"error": "Product name is required"}), 400

    products = load_products()

    numeric_ids = [
        p["id"] for p in products
        if isinstance(p.get("id"), int)
    ]
    new_id = max(numeric_ids, default=0) + 1

    product = {
        "id": new_id,
        "name": str(data["name"]).strip(),
        "image": data.get("image", ""),
        "category": data.get("category", "gift"),
        "occasions": data.get("occasions", []),
        "price": data.get("price"),
        "quality": data.get("quality", "standard"),
        "delivery_days": data.get("delivery_days", 7),
        "description": data.get("description", ""),
        "personalize": bool(data.get("personalize", False)),
        "details": data.get("details", ""),
        "active": True,
    }

    products.append(product)
    save_products(products)

    return jsonify(serialize(product)), 201


@app.put("/api/products/<int:product_id>")
def update_product(product_id):
    data = request.get_json(silent=True) or {}

    allowed = {
        "name", "image", "category", "occasions", "price",
        "quality", "delivery_days", "description",
        "personalize", "details"
    }

    products = load_products()

    for product in products:
        if (
            product.get("id") == product_id
            and product.get("active", True)
        ):
            product.update({
                key: value
                for key, value in data.items()
                if key in allowed
            })

            if not str(product.get("name", "")).strip():
                return jsonify({
                    "error": "Product name is required"
                }), 400

            save_products(products)
            return jsonify(serialize(product))

    return jsonify({"error": "Product not found"}), 404


@app.delete("/api/products/<int:product_id>")
def delete_product(product_id):
    products = load_products()

    for product in products:
        if (
            product.get("id") == product_id
            and product.get("active", True)
        ):
            product["active"] = False
            save_products(products)

            return jsonify({
                "deleted": True,
                "id": product_id
            })

    return jsonify({"error": "Product not found"}), 404


if __name__ == "__main__":
    print("GiftMatch is running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
