import pandas as pd
import numpy as np
import time

last_count = 0

while True:
    try:
        df = pd.read_csv("data/transactions.csv")

        current_count = len(df)

        if current_count != last_count:

            total_revenue = df["Amount"].sum()
            avg_transaction = df["Amount"].mean()

            category_sales = df.groupby("Category")["Amount"].sum()

            # ---- Anomaly Detection ----
            mean = df["Amount"].mean()
            std = df["Amount"].std()

            df["Z_score"] = (df["Amount"] - mean) / std
            anomalies = df[df["Z_score"].abs() > 3]

            print("\n------ BUSINESS KPIs ------")
            print("Total Transactions:", current_count)
            print("Total Revenue:", round(total_revenue,2))
            print("Average Transaction:", round(avg_transaction,2))

            print("\nSales by Category:")
            print(category_sales)

            print("\nAnomalies Detected:", len(anomalies))

            if len(anomalies) > 0:
                print(anomalies[["Transaction_ID","Amount","Category","Z_score"]])

            last_count = current_count

    except:
        print("Waiting for data...")

    time.sleep(5)