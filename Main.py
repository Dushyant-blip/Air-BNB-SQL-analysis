import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Step 1: Load the CSV file
df = pd.read_csv("listings.csv")

# Step 2: Connect to SQLite database
conn = sqlite3.connect("airbnb.db")
cursor = conn.cursor()

# Step 3: Save dataframe to SQLite table
df.to_sql("listings", conn, if_exists="replace", index=False)
print("✅ Data imported into 'listings' table!\n")

# Step 4: Query top-rated listings with non-null prices
query = """
SELECT review_scores_rating, price 
FROM listings 
WHERE review_scores_rating = 4.95 AND price IS NOT NULL;
"""
cursor.execute(query)
results = cursor.fetchall()

# Step 5: Clean price strings and convert to float
cleaned_data = []
for rating, price in results:
    try:
        price_num = float(price.replace('$', '').replace(',', '').strip())
        cleaned_data.append((rating, price_num))
    except:
        continue

# Step 6: Print cleaned results
print(f"🔹 Number of valid entries: {len(cleaned_data)}")
for entry in cleaned_data[:10]:
    print(entry)

# Step 7: Plot histogram
prices = [price for _, price in cleaned_data]
plt.figure(figsize=(10, 6))
plt.hist(prices, bins=15, color='skyblue', edgecolor='black')
plt.title("Price Distribution of Listings with 4.95 Review Score")
plt.xlabel("Price ($)")
plt.ylabel("Number of Listings")
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 8: Close DB
conn.close()
