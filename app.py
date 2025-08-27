from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

app = Flask(__name__)

# -------------------------
# Database configuration
# -------------------------
DATABASE_URI = os.environ.get(
    'DATABASE_URI',
    'postgresql://crmuser:crmpass@db:5432/crmdb'
)

engine = create_engine(DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# -------------------------
# Customer model
# -------------------------
class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer)
    address = Column(String(200))
    mother_name = Column(String(100))
    date_of_registration = Column(Date)
    gender = Column(String(10))
    email = Column(String(100))

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "age": self.age,
            "address": self.address,
            "mother_name": self.mother_name,
            "date_of_registration": str(self.date_of_registration),
            "gender": self.gender,
            "email": self.email
        }

# -------------------------
# Initialize database
# -------------------------
Base.metadata.create_all(engine)

# -------------------------
# Insert demo customers if table empty
# -------------------------
demo_customers = [
    {"name": "Xasan", "age": 28, "address": "1 Demo St", "mother_name": "Hodan", "gender": "Male", "email": "xasan@example.com"},
    {"name": "Siman", "age": 25, "address": "2 Demo St", "mother_name": "Faduma", "gender": "Female", "email": "siman@example.com"},
    {"name": "Samiir", "age": 30, "address": "3 Demo St", "mother_name": "Amina", "gender": "Male", "email": "samiir@example.com"}
]

with Session() as session:
    if session.query(Customer).count() == 0:
        for c in demo_customers:
            customer = Customer(
                name=c["name"],
                age=c["age"],
                address=c["address"],
                mother_name=c["mother_name"],
                date_of_registration=datetime.today().date(),
                gender=c["gender"],
                email=c["email"]
            )
            session.add(customer)
        session.commit()

# -------------------------
# Routes
# -------------------------
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "success", "message": "app is running"}), 200

@app.route('/customer', methods=['GET'])
def get_customers():
    session = Session()
    customers = session.query(Customer).all()
    session.close()
    return jsonify({
        "status": "success",
        "message": "Customers retrieved successfully",
        "customers": [c.to_dict() for c in customers]
    }), 200

@app.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    session = Session()
    customer = session.query(Customer).get(customer_id)
    session.close()
    if customer:
        return jsonify({"status": "success", "customer": customer.to_dict()}), 200
    return jsonify({"status": "error", "message": "Customer not found"}), 404

@app.route('/customer', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer = Customer(
        name=data['name'],
        age=data['age'],
        address=data['address'],
        mother_name=data['mother_name'],
        date_of_registration=datetime.strptime(data['date_of_registration'], "%Y-%m-%d").date(),
        gender=data['gender'],
        email=data['email']
    )
    session = Session()
    session.add(customer)
    session.commit()
    session.close()
    return jsonify({"status": "success", "customer": customer.to_dict()}), 201

@app.route('/customer/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    session = Session()
    customer = session.query(Customer).get(customer_id)
    if not customer:
        session.close()
        return jsonify({"status": "error", "message": "Customer not found"}), 404

    customer.name = data.get('name', customer.name)
    customer.age = data.get('age', customer.age)
    customer.address = data.get('address', customer.address)
    customer.mother_name = data.get('mother_name', customer.mother_name)
    if data.get('date_of_registration'):
        customer.date_of_registration = datetime.strptime(data['date_of_registration'], "%Y-%m-%d").date()
    customer.gender = data.get('gender', customer.gender)
    customer.email = data.get('email', customer.email)

    session.commit()
    session.close()
    return jsonify({"status": "success", "customer": customer.to_dict()}), 200

@app.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    session = Session()
    customer = session.query(Customer).get(customer_id)
    if not customer:
        session.close()
        return jsonify({"status": "error", "message": "Customer not found"}), 404
    session.delete(customer)
    session.commit()
    session.close()
    return jsonify({"status": "success", "message": "Customer deleted"}), 200

# -------------------------
# Run app
# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
