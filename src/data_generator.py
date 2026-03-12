import pandas as pd
import random
import time
from datetime import datetime

categories = ["Food","Electronics","Clothing","Travel","Bills"]

transaction_count = 0
next_anomaly = random.randint(10,20)

while True:

    transaction_count += 1

    if transaction_count == next_anomaly:
        amount = round(random.uniform(5000,15000),2)
        print("⚠️ Anomaly Transaction Generated")
        next_anomaly += random.randint(10,20)
    else:
        amount = round(random.uniform(10,1000),2)

    transaction = {
        "Transaction_ID": random.randint(100000,999999),
        "Customer_ID": random.randint(1000,5000),
        "Amount": amount,
        "Category": random.choice(categories),
        "Timestamp": datetime.now()
    }

    df = pd.DataFrame([transaction])
    df.to_csv("data/transactions.csv",mode="a",header=False,index=False)

    print("Transaction added:",transaction)

    time.sleep(2)