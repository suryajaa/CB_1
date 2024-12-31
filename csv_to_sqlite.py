import sqlite3
import pandas as pd

# Specify the path to your CSV file and database
csv_file = "employee_data.csv"
sqlite_db = "employee.db"

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file)

# Connect to (or create) an SQLite database
conn = sqlite3.connect(sqlite_db)
cursor = conn.cursor()

# Write the data to a new SQLite table
table_name = "employee_info"
df.to_sql(table_name, conn, if_exists="replace", index=False)


# Step 1: Check the existing columns
print("Existing columns in the table:")
cursor.execute(f"PRAGMA table_info({table_name})")
columns = cursor.fetchall()
for col in columns:
    print(col)

# Step 2: Define the columns to keep
columns_to_keep = ["EmpID", "FirstName","LastName","StartDate", "Title", "Supervisor","ADEmail","BusinessUnit","EmployeeStatus","EmployeeType","PayZone","DepartmentType","Division","DOB","JobFunctionDescription","GenderCode","LocationCode","RaceDesc","MaritalDesc","Performance Score","Current Employee Rating"]  # Update with the columns you want to keep
df_filtered = df[columns_to_keep]

# Step 3: Create a new table with only the required columns
new_table_name = "employee_info_filtered"
df_filtered.to_sql(new_table_name, conn, if_exists="replace", index=False)

# Step 4: Verify the data in the new table
print(f"Data in the new table '{new_table_name}':")
cursor.execute(f"SELECT * FROM {new_table_name}")
for row in cursor.fetchall():
    print(row)

# Step 5: Replace the old table with the new one (optional)
cursor.execute(f"DROP TABLE {table_name}")
cursor.execute(f"ALTER TABLE {new_table_name} RENAME TO {table_name}")

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"Columns not in {columns_to_keep} have been removed.")
