import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker()
Faker.seed(42)

print("Starting E-commerce Dataset Generation...")
print("=" * 50)

# 1. CALENDAR TABLE
print("Creating Calendar Table...")
def create_calendar_table():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    calendar_data = {
        'Date': date_range,
        'Year': date_range.year,
        'Month': date_range.month,
        'MonthName': date_range.strftime('%B'),
        'Quarter': date_range.quarter,
        'QuarterName': ['Q' + str(q) for q in date_range.quarter],
        'WeekOfYear': date_range.isocalendar().week,
        'DayOfWeek': date_range.dayofweek + 1,  # 1=Monday, 7=Sunday
        'DayName': date_range.strftime('%A'),
        'IsWeekend': (date_range.dayofweek >= 5).astype(int),
        'IsHoliday': 0  # Simplified - you can enhance this
    }
    
    # Mark some holidays (simplified)
    calendar_df = pd.DataFrame(calendar_data)
    holiday_dates = ['2022-01-01', '2022-07-04', '2022-12-25', 
                     '2023-01-01', '2023-07-04', '2023-12-25',
                     '2024-01-01', '2024-07-04', '2024-12-25']
    
    calendar_df.loc[calendar_df['Date'].dt.strftime('%Y-%m-%d').isin(holiday_dates), 'IsHoliday'] = 1
    
    return calendar_df

# 2. CUSTOMERS TABLE
print("Creating Customers Table...")
def create_customers_table(num_customers=5000):
    customer_tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']
    tier_weights = [0.5, 0.3, 0.15, 0.05]
    
    countries = ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Australia', 'Japan']
    country_weights = [0.4, 0.15, 0.15, 0.1, 0.08, 0.07, 0.05]
    
    customers_data = []
    
    for i in range(1, num_customers + 1):
        country = np.random.choice(countries, p=country_weights)
        
        # Generate realistic data based on country
        if country == 'United States':
            city = fake.city()
            state = fake.state_abbr()
        elif country == 'Canada':
            city = fake.city()
            # Canadian provinces
            canadian_provinces = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'ON', 'PE', 'QC', 'SK', 'NT', 'NU', 'YT']
            state = random.choice(canadian_provinces)
        else:
            city = fake.city()
            state = fake.state()
        
        registration_date = fake.date_between(start_date='-3y', end_date='-30d')
        
        customer = {
            'CustomerID': i,
            'CustomerName': fake.name(),
            'Email': fake.email(),
            'Phone': fake.phone_number(),
            'City': city,
            'State': state,
            'Country': country,
            'PostalCode': fake.postcode(),
            'RegistrationDate': registration_date,
            'CustomerTier': np.random.choice(customer_tiers, p=tier_weights),
            'AgeGroup': np.random.choice(['18-25', '26-35', '36-45', '46-55', '56+'], 
                                       p=[0.15, 0.25, 0.25, 0.2, 0.15])
        }
        customers_data.append(customer)
    
    return pd.DataFrame(customers_data)

# 3. PRODUCTS TABLE
print("Creating Products Table...")
def create_products_table():
    categories = {
        'Electronics': {
            'subcategories': ['Smartphones', 'Laptops', 'Tablets', 'Headphones', 'Smartwatches', 'Gaming'],
            'brands': ['Apple', 'Samsung', 'Sony', 'Dell', 'HP', 'Microsoft', 'Nintendo'],
            'price_range': (50, 2000)
        },
        'Clothing': {
            'subcategories': ['Mens Wear', 'Womens Wear', 'Kids Wear', 'Shoes', 'Accessories'],
            'brands': ['Nike', 'Adidas', 'Zara', 'H&M', 'Levis', 'GAP', 'Uniqlo'],
            'price_range': (20, 300)
        },
        'Home & Garden': {
            'subcategories': ['Furniture', 'Kitchen', 'Bedding', 'Garden Tools', 'Decor'],
            'brands': ['IKEA', 'Home Depot', 'Wayfair', 'West Elm', 'Target', 'Walmart'],
            'price_range': (25, 1500)
        },
        'Books': {
            'subcategories': ['Fiction', 'Non-Fiction', 'Educational', 'Comics', 'Magazines'],
            'brands': ['Penguin', 'Harper', 'Random House', 'Scholastic', 'Marvel', 'DC'],
            'price_range': (10, 80)
        },
        'Sports': {
            'subcategories': ['Fitness', 'Outdoor', 'Team Sports', 'Water Sports', 'Winter Sports'],
            'brands': ['Nike', 'Adidas', 'Under Armour', 'Patagonia', 'North Face', 'Columbia'],
            'price_range': (15, 500)
        }
    }
    
    products_data = []
    product_id = 1
    
    for category, details in categories.items():
        # Generate 100-200 products per category
        num_products = random.randint(100, 200)
        
        for _ in range(num_products):
            subcategory = np.random.choice(details['subcategories'])
            brand = np.random.choice(details['brands'])
            
            # Generate realistic product names
            if category == 'Electronics':
                product_names = [f"{brand} {subcategory} Pro", f"{brand} {subcategory} Max", 
                               f"{brand} {subcategory} Standard", f"{brand} {subcategory} Lite"]
            elif category == 'Clothing':
                product_names = [f"{brand} {subcategory} Collection", f"{brand} Premium {subcategory}",
                               f"{brand} Classic {subcategory}", f"{brand} Sports {subcategory}"]
            else:
                product_names = [f"{brand} {subcategory}", f"{brand} Professional {subcategory}",
                               f"{brand} Deluxe {subcategory}", f"{brand} Basic {subcategory}"]
            
            product_name = random.choice(product_names)
            
            # Price logic
            min_price, max_price = details['price_range']
            list_price = round(np.random.uniform(min_price, max_price), 2)
            cost_price = round(list_price * np.random.uniform(0.4, 0.7), 2)  # 40-70% margin
            
            # Stock quantity
            stock_quantity = np.random.randint(0, 1000)
            
            product = {
                'ProductID': product_id,
                'ProductName': product_name,
                'Category': category,
                'SubCategory': subcategory,
                'Brand': brand,
                'CostPrice': cost_price,
                'ListPrice': list_price,
                'StockQuantity': stock_quantity,
                'Weight': round(np.random.uniform(0.1, 10), 2),
                'Dimensions': f"{np.random.randint(5,50)}x{np.random.randint(5,50)}x{np.random.randint(5,50)}cm",
                'LaunchDate': fake.date_between(start_date='-5y', end_date='-1m')
            }
            
            products_data.append(product)
            product_id += 1
    
    return pd.DataFrame(products_data)

# 4. ORDERS TABLE (Most Complex)
print("Creating Orders Table...")
def create_orders_table(customers_df, products_df, num_orders=50000):
    orders_data = []
    order_statuses = ['Completed', 'Shipped', 'Processing', 'Cancelled', 'Returned']
    status_weights = [0.7, 0.15, 0.08, 0.05, 0.02]
    
    # Create customer purchase patterns
    customer_purchase_probability = {}
    for _, customer in customers_df.iterrows():
        # Higher tier customers buy more frequently
        if customer['CustomerTier'] == 'Platinum':
            base_prob = 0.8
        elif customer['CustomerTier'] == 'Gold':
            base_prob = 0.6
        elif customer['CustomerTier'] == 'Silver':
            base_prob = 0.4
        else:
            base_prob = 0.2
        
        customer_purchase_probability[customer['CustomerID']] = base_prob
    
    for order_id in range(1, num_orders + 1):
        # Select customer (weighted by tier)
        customer = customers_df.sample(weights=[customer_purchase_probability.get(cid, 0.2) 
                                              for cid in customers_df['CustomerID']]).iloc[0]
        
        # Order date (more recent orders more likely)
        # Weight towards more recent dates
        days_back = int(np.random.exponential(100))  # Exponential distribution favors recent dates
        days_back = min(days_back, 1095)  # Cap at 3 years
        order_date = datetime.now() - timedelta(days=days_back)
        
        # Convert customer registration date to datetime if it's a date
        reg_date = customer['RegistrationDate']
        if hasattr(reg_date, 'date'):  # It's already a datetime
            reg_datetime = reg_date
        else:  # It's a date, convert to datetime
            reg_datetime = datetime.combine(reg_date, datetime.min.time())
            
        order_date = max(order_date, reg_datetime)  # Can't order before registration
        
        # Select products for this order (1-5 items)
        num_items = np.random.choice([1, 2, 3, 4, 5], p=[0.4, 0.3, 0.2, 0.07, 0.03])
        selected_products = products_df.sample(n=num_items)
        
        # Order-level information
        order_status = np.random.choice(order_statuses, p=status_weights)
        
        # Generate line items for this order
        order_total = 0
        for _, product in selected_products.iterrows():
            quantity = np.random.randint(1, 4)  # 1-3 quantity per item
            unit_price = product['ListPrice']
            
            # Apply discounts occasionally
            discount_rate = 0
            if np.random.random() < 0.2:  # 20% chance of discount
                discount_rate = np.random.uniform(0.05, 0.3)  # 5-30% discount
                unit_price = unit_price * (1 - discount_rate)
            
            line_total = round(unit_price * quantity, 2)
            order_total += line_total
            
            # Shipping cost (calculated at order level, but we'll add to first item)
            shipping_cost = 0
            if order_id == 1 or orders_data[-1]['OrderID'] != order_id:  # First item of order
                if order_total < 50:
                    shipping_cost = round(np.random.uniform(5, 15), 2)
                elif np.random.random() < 0.1:  # 10% chance of express shipping
                    shipping_cost = round(np.random.uniform(15, 25), 2)
            
            order_item = {
                'OrderID': order_id,
                'CustomerID': customer['CustomerID'],
                'ProductID': product['ProductID'],
                'OrderDate': order_date.strftime('%Y-%m-%d'),
                'Quantity': quantity,
                'UnitPrice': round(unit_price, 2),
                'TotalAmount': line_total,
                'DiscountAmount': round((product['ListPrice'] - unit_price) * quantity, 2),
                'ShippingCost': shipping_cost,
                'Status': order_status,
                'PaymentMethod': np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay'], 
                                                p=[0.5, 0.25, 0.15, 0.1]),
                'ShippingMethod': np.random.choice(['Standard', 'Express', 'Overnight'], 
                                                 p=[0.8, 0.15, 0.05])
            }
            
            orders_data.append(order_item)
        
        # Progress indicator
        if order_id % 5000 == 0:
            print(f"   Generated {order_id:,} orders...")
    
    return pd.DataFrame(orders_data)

# Generate all tables
print("\nGenerating all tables...")

# Create tables
calendar_df = create_calendar_table()
print(f"Calendar: {len(calendar_df):,} records")

customers_df = create_customers_table(5000)
print(f"Customers: {len(customers_df):,} records")

products_df = create_products_table()
print(f"Products: {len(products_df):,} records")

orders_df = create_orders_table(customers_df, products_df, 50000)
print(f"Orders: {len(orders_df):,} records")

# Data quality summary
print(f"\nDataset Summary:")
print(f"   Date Range: {calendar_df['Date'].min()} to {calendar_df['Date'].max()}")
print(f"   Revenue Range: ${orders_df['TotalAmount'].min():.2f} to ${orders_df['TotalAmount'].max():.2f}")
print(f"   Total Revenue: ${orders_df['TotalAmount'].sum():,.2f}")
print(f"   Avg Order Value: ${orders_df.groupby('OrderID')['TotalAmount'].sum().mean():.2f}")
print(f"   Categories: {', '.join(products_df['Category'].unique())}")
print(f"   Countries: {', '.join(customers_df['Country'].unique())}")

# Export to CSV files
print(f"\nExporting CSV files...")

calendar_df.to_csv('calendar.csv', index=False)
customers_df.to_csv('customers.csv', index=False)
products_df.to_csv('products.csv', index=False)
orders_df.to_csv('orders.csv', index=False)

print("All CSV files exported successfully!")
print(f"\nFiles created:")
print(f"   calendar.csv - {len(calendar_df):,} records")
print(f"   customers.csv - {len(customers_df):,} records") 
print(f"   products.csv - {len(products_df):,} records")
print(f"   orders.csv - {len(orders_df):,} records")

print(f"\nDataset generation complete!")
print(f"Your synthetic e-commerce dataset is ready for Power BI!")

# Display sample data
print(f"\nSample Data Preview:")
print(f"\nCustomers (first 3 rows):")
print(customers_df.head(3).to_string())

print(f"\nProducts (first 3 rows):")
print(products_df.head(3).to_string())

print(f"\nOrders (first 5 rows):")
print(orders_df.head(5).to_string())