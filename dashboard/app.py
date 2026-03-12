from flask import Flask, render_template, jsonify
import pandas as pd
import psutil
from sklearn.ensemble import IsolationForest

app = Flask(__name__)

def load_data():

    df = pd.read_csv("data/transactions.csv")

    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    return df

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/categories")
def categories():
    return render_template("categories.html")

@app.route("/revenue")
def revenue():
    return render_template("revenue.html")

@app.route("/anomalies")
def anomalies():
    return render_template("anomalies.html")

@app.route("/performance")
def performance():
    return render_template("performance.html")

@app.route("/transactions_by_category")
def transactions_by_category():
    return render_template("transactions_by_category.html")

@app.route("/data")
def data():

    df = load_data()

    total_transactions = len(df)
    total_revenue = df["Amount"].sum()
    avg_transaction = df["Amount"].mean()

    category_sales = df.groupby("Category")["Amount"].sum().to_dict()

    transaction_counts = df["Category"].value_counts().to_dict()

    mean = df["Amount"].mean()
    std = df["Amount"].std()

    df["Z_score"] = (df["Amount"] - mean) / std

    z_anomalies = df[df["Z_score"].abs() > 3]

    model = IsolationForest(
        contamination=0.03,
        random_state=42
    )

    X = df[["Amount"]]

    model.fit(X)

    df["ML_Anomaly"] = model.predict(X)

    ml_anomalies = df[df["ML_Anomaly"] == -1]

    anomalies = pd.concat([z_anomalies, ml_anomalies]).drop_duplicates()

    anomaly_data = anomalies[["Transaction_ID","Amount","Category"]].to_dict(orient="records")

    revenue_trend = df.tail(30)["Amount"].tolist()

    if "Timestamp" in df.columns:
        revenue_time = df.tail(30)["Timestamp"].astype(str).tolist()
    else:
        revenue_time = list(range(len(revenue_trend)))

    performance = {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent
    }

    if "Timestamp" in df.columns:
        recent_transactions = df.tail(10)[
            ["Transaction_ID","Amount","Category","Timestamp"]
        ].to_dict(orient="records")
    else:
        recent_transactions = df.tail(10)[
            ["Transaction_ID","Amount","Category"]
        ].to_dict(orient="records")


    return jsonify({
        "total_transactions": total_transactions,
        "total_revenue": round(total_revenue,2),
        "avg_transaction": round(avg_transaction,2),
        "category_sales": category_sales,
        "transaction_counts": transaction_counts,
        "anomalies": anomaly_data,
        "revenue_trend": revenue_trend,
        "revenue_time": revenue_time,
        "performance": performance,
        "recent_transactions": recent_transactions
    })

if __name__ == "__main__":
    app.run(debug=True)