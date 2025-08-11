from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# ---------------- CONFIG ----------------
DB_NAME = "mseet_39142088_mseet_39142088_"       # Change here
DB_USER = "mseet_39142088"       # Change here
DB_PASSWORD = "Faisal7788"   # Change here
DB_HOST = "	sql300.hstn.me"  # Change here

# Flask app setup
app = Flask(__name__)
CORS(app)

# MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- MODELS ----------------
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.Text, nullable=True)
    image1 = db.Column(db.String(500), nullable=True)
    image2 = db.Column(db.String(500), nullable=True)
    image3 = db.Column(db.String(500), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': float(self.price),
            'description': self.description,
            'images': [i for i in (self.image1, self.image2, self.image3) if i]
        }

# Create table if not exists
with app.app_context():
    db.create_all()

# ---------------- ROUTES ----------------
@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    product = Product(
        title=data.get('title'),
        price=data.get('price', 0.0),
        description=data.get('description'),
        image1=(data.get('images') or [None])[0] if len(data.get('images') or []) > 0 else None,
        image2=(data.get('images') or [None])[1] if len(data.get('images') or []) > 1 else None,
        image3=(data.get('images') or [None])[2] if len(data.get('images') or []) > 2 else None
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

if __name__ == "__main__":
    app.run(debug=True)
