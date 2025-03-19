from app import app, db
from models import Product

def init_db():
    with app.app_context():
        # Clear existing products
        db.session.query(Product).delete()
        
        # Product data
        products = [
            {
                "name": "Ultra HD Smart TV 65\"",
                "price": 999.99,
                "description": "4K Ultra HD Smart LED TV with HDR and built-in voice assistant",
                "category": "Electronics",
                "stock": 15,
                "brand": "TechVision",
                "rating": 4.5,
                "discount": 10,
                "image_url": "static/images/tv.jpeg",
                "specifications": [
                    "65-inch 4K Display",
                    "HDR10+ Support",
                    "Smart TV Features",
                    "4 HDMI Ports",
                    "Built-in WiFi"
                ]
            },
            {
                "name": "Premium Wireless Headphones",
                "price": 249.99,
                "description": "Noise-cancelling wireless headphones with 30-hour battery life",
                "category": "Audio",
                "stock": 25,
                "brand": "SoundMaster",
                "rating": 4.8,
                "image_url": "static/images/headphone.jpeg",
                "specifications": [
                    "Active Noise Cancellation",
                    "Bluetooth 5.0",
                    "30-hour Battery Life",
                    "Quick Charge",
                    "Voice Assistant Compatible"
                ]
            },
            {
                "name": "Professional DSLR Camera",
                "price": 1299.99,
                "description": "24.2MP Digital SLR Camera with 18-55mm Lens Kit",
                "category": "Photography",
                "stock": 8,
                "brand": "PhotoPro",
                "rating": 4.7,
                "discount": 5,
                "image_url": "static/images/camera.jpeg",
                "specifications": [
                    "24.2MP APS-C Sensor",
                    "4K Video Recording",
                    "3-inch LCD Screen",
                    "Dual Memory Card Slots",
                    "Weather-Sealed Body"
                ]
            },
            {
                "name": "Smart Fitness Watch",
                "price": 199.99,
                "description": "Advanced fitness tracker with heart rate monitoring and GPS",
                "category": "Wearables",
                "stock": 30,
                "brand": "FitTech",
                "rating": 4.6,
                "image_url": "static/images/watch.jpeg",
                "specifications": [
                    "Heart Rate Monitor",
                    "Built-in GPS",
                    "5 ATM Water Resistance",
                    "7-day Battery Life",
                    "Sleep Tracking"
                ]
            },
            {
                "name": "Gaming Laptop",
                "price": 1499.99,
                "description": "High-performance gaming laptop with RTX 3070 GPU",
                "category": "Computers",
                "stock": 12,
                "brand": "GameMaster",
                "rating": 4.9,
                "discount": 15,
                "image_url": "static/images/laptop.jpeg",
                "specifications": [
                    "15.6\" 144Hz Display",
                    "RTX 3070 8GB GPU",
                    "16GB RAM",
                    "1TB NVMe SSD",
                    "RGB Keyboard"
                ]
            },
            {
                "name": "Wireless Earbuds",
                "price": 129.99,
                "description": "True wireless earbuds with active noise cancellation",
                "category": "Audio",
                "stock": 40,
                "brand": "SoundMaster",
                "rating": 4.4,
                "image_url": "static/images/buds.jpeg",
                "specifications": [
                    "Active Noise Cancellation",
                    "IPX4 Water Resistance",
                    "6-hour Battery Life",
                    "Wireless Charging Case",
                    "Touch Controls"
                ]
            }
        ]

        # Add products to database
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        # Commit changes
        db.session.commit()
        print("Database initialized with products!")

if __name__ == "__main__":
    init_db() 