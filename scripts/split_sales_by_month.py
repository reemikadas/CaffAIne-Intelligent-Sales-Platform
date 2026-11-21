from pathlib import Path
import pandas as pd

# Define the Path Objects
source_file = Path("data/source/coffee_sales.csv")
output_directory = Path("data/monthly")
output_directory.mkdir(parents=True, exist_ok=True)

# Read the source file
sales = pd.read_csv(source_file)

# Inspect the Schema
# sales.info()

# Note: transaction_date and transaction_time are stored as 'Object'. Convert to 'datetime' data type.

# Convert to Datetime
sales["transaction_date"] = pd.to_datetime(sales["transaction_date"], format="%m/%d/%y", errors="raise")

# print(f"Transaction date after conversion: {sales["transaction_date"].dtype}")
# print(f"Minimum date: {sales["transaction_date"].min()}")
# print(f"Maximum date: {sales["transaction_date"].max()}")

total_output_rows = 0

for month, monthly_sales in sales.groupby(sales["transaction_date"].dt.to_period("M")):
    month_label = month.strftime("%Y_%m")
    output_file = output_directory / f"coffee_sales_{month_label}.csv"

    monthly_sales.to_csv(output_file, index=False)

    print(f"{output_file.name}: {len(monthly_sales):,} records")

    total_output_rows += len(monthly_sales)

if total_output_rows != len(sales):
    raise RuntimeError(
        f"Row-count mismatch: Source has {len(sales):,} records but monthly files contain {total_output_rows:,} records."
    )

print(f"Validation check passed: {total_output_rows:,} of {len(sales):,} records were written.")