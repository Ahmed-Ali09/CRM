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
# Insert demo customers if empty
# -------------------------
session = Session()
if session.query(Customer).count() == 0:
    demo_customers = [
        Customer(name="Xasan", age=28, address="1 Demo St", mother_name="Hodan",
                 date_of_registration=datetime.now().date(), gender="Male", email="xasan@example.com"),
        Customer(name="Siman", age=25, address="2 Demo St", mother_name="Faduma",
                 date_of_registration=datetime.now().date(), gender="Female", email="siman@example.com"),
        Customer(name="Samiir", age=30, address="3 Demo St", mother_name="Amina",
                 date_of_registration=datetime.now().date(), gender="Male", email="samiir@example.com")
    ]
    session.add_all(demo_customers)
    session.commit()
session.close()

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

# -------------------------
# Run app
# -------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
