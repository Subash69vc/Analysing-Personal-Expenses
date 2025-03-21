from faker import Faker
import random
import pandas as pd
import datetime
import csv

# Initialize the faker object
fake = Faker()

categories = ['Groceries', 'Utility Bills', 'Insurance', 'Rent', 'EMI', 'Subscriptions', 'Investments', 'Transportation', 'Entertainment', 'Miscellaneous']
payment_modes = ['Credit Card', 'Debit Card', 'Net Banking', 'UPI', 'Wallet', 'Cash']
utility_bills = ['Electricity', 'Water', 'Gas', 'Internet', 'Mobile', 'DTH']
insurance = ['Health', 'Life', 'Vehicle', 'Home', 'Travel']
subscriptions = ['Amazon Prime', 'Netflix', 'Spotify', 'Apple Music', 'YouTube Premium', 'Disney+ Hotstar']
investments = ['Stocks', 'Mutual Funds', 'Fixed Deposits', 'Recurring Deposits', 'Savings Account']
transportation = ['Metro', 'Bus', 'Cab', 'Auto', 'Bike', 'Car']
entertainment = ['Movies', 'Concerts', 'Events', 'Clubs', 'Pubs', 'Restaurants']
miscellaneous = ['Shopping', 'Gifts', 'Donations', 'Charity', 'Taxes', 'Fees']
EMI = ['Home Loan', 'Car Loan', 'Personal Loan', 'Education Loan', 'Consumer Durable Loan']
groceries = ['Fruits', 'Vegetables', 'Snacks', 'Beverages', 'Cereals']  # Example for groceries

# Function to generate random data
def generate_data(num_generate=120):
    data = []
    
    start_date = datetime.date(2025, 3, 1)
    end_date = datetime.date(2025, 3, 17)

    for _ in range(num_generate):
        category = random.choice(categories)
        
        if category == 'Groceries':
            description = f"Bought {random.choice(groceries)}"
        elif category == 'Utility Bills':
            description = f"Paid for {random.choice(utility_bills)}"
        elif category == 'Insurance':
            description = f"Paid Premium for {random.choice(insurance)}"
        elif category == 'Rent':
            description = "House Rent"
        elif category == 'EMI':
            description = f"Paid a {random.choice(EMI)}"
        elif category == 'Subscriptions':
            description = f"Paid for {random.choice(subscriptions)}"
        elif category == 'Investments':
            description = f"Invested in {random.choice(investments)}"
        elif category == 'Transportation':
            description = f"{random.choice(transportation)} Fare"
        elif category == 'Entertainment':
            description = f"{random.choice(entertainment)} Expense"
        elif category == 'Miscellaneous':
            description = f"{random.choice(miscellaneous)} Expense"

        expense = {
            "Date": fake.date_between(start_date=start_date, end_date=end_date), # Generate date between 1st April 2024 and 31st March 2025
            "Category": category,
            "Payment Mode": random.choice(payment_modes),
            "Description": description,
            "Amount": round(random.uniform(100, 10000), 2),
            "Cashback":  round(random.uniform(0, 50), 0)
        }
        
        data.append(expense)
    
    return pd.DataFrame(data)

# Generate and display the data
march2025_expense = generate_data(148)
 

# convering the data to csv
march2025_expense.to_csv('march2025_expense.csv', index=False)


