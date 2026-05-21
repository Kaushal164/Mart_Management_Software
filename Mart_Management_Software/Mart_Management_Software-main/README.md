# Nepal Mart Management Software

A comprehensive mart/retail management system built with **Django** (Python) for businesses in Nepal. Features product management, shopping cart, order processing with billing, inventory tracking, and an admin dashboard with sales reports.

## Features

### Customer-Facing
- **Product Catalog** - Browse products by category, search, filter by price, sort by name/price/date
- **Shopping Cart** - Add/remove/update items, quantity validation against stock
- **Checkout & Billing** - Order placement with 13% VAT calculation (Nepal standard), multiple payment methods
- **User Accounts** - Registration, login, profile management, order history
- **Order Tracking** - View order status and details

### Admin/Staff Dashboard
- **Overview Dashboard** - Revenue stats, today's sales, weekly trends, low stock alerts, top products
- **Inventory Management** - Stock levels, add/remove/adjust stock, movement tracking, low stock filtering
- **Sales Reports** - Date range filtering, daily breakdown, top products, payment method analysis
- **Order Management** - Search/filter orders, update status & payment status

### Nepal-Specific
- Currency: **NPR (Rs.)** throughout the system
- **13% VAT** calculation on all orders
- Payment methods: Cash, eSewa, Khalti, Bank Transfer, Card
- Timezone: Asia/Kathmandu
- Sample products: Wai Wai, DDC Milk, Frozen Momos, Tokla Tea, etc.

## Tech Stack

- **Backend:** Django 4.2+ (Python)
- **Database:** SQLite (default, easily switchable to PostgreSQL)
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **Image Handling:** Pillow

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Kaushal164/Mart_Management_Software.git
cd Mart_Management_Software
```

### 2. Create virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 5. Seed sample data (optional but recommended)
```bash
python3 manage.py seed_data
```
This creates:
- 8 product categories
- 39 sample products with Nepal-specific items
- Admin user: `admin` / `admin123`

### 6. Run the development server
```bash
python3 manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |

## Project Structure

```
Mart_Management_Software/
├── mart_management/     # Main Django project settings & URLs
├── products/            # Product catalog, categories, inventory models
├── cart/                # Shopping cart functionality
├── orders/              # Order processing, checkout, billing
├── accounts/            # User registration, login, profiles
├── dashboard/           # Admin dashboard, reports, inventory mgmt
├── templates/           # HTML templates (Bootstrap 5)
├── static/              # CSS, JS, images
├── media/               # Uploaded product/category images
├── requirements.txt     # Python dependencies
└── manage.py            # Django management script
```

## Key URLs

| URL | Description |
|-----|-------------|
| `/` | Homepage with featured products |
| `/products/` | Product listing with search & filters |
| `/cart/` | Shopping cart |
| `/orders/checkout/` | Checkout page |
| `/accounts/login/` | User login |
| `/accounts/register/` | User registration |
| `/dashboard/` | Admin dashboard (staff only) |
| `/dashboard/inventory/` | Inventory management |
| `/dashboard/sales/` | Sales reports |
| `/dashboard/orders/` | Order management |
| `/admin/` | Django admin panel |

## Screenshots

The application uses a green-themed Bootstrap 5 design with responsive layout for both desktop and mobile devices.

## License

This project is open source and available for educational and commercial use.
