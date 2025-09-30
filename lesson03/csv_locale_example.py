import csv
import pandas as pd

# Example data with float values
data = [
    ["name", "value"],
    ["foo", 1.23],  # float value
    ["bar", 4.56],
]


def comma_to_dot(value):
    """Convert a string with comma as decimal separator to float."""
    try:
        if (
            value.replace(",", ".")
            .replace("-", "")
            .replace("e", "")
            .replace("E", "")
            .isdigit()
        ):
            return float(value.replace(",", "."))
        else:
            return value
    except ValueError:
        return None


def dot_to_comma(value):
    """Convert a float to string with comma as decimal separator."""
    try:
        if isinstance(value, float):
            return str(value).replace(".", ",")
        else:
            return value
    except ValueError:
        return None


# --- Using csv module: write and read with semicolon delimiter ---
with open("temp/example_semicolon.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerows([dot_to_comma(item) for item in row] for row in data)

with open("temp/example_semicolon.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    for row in reader:
        row = [comma_to_dot(item) for item in row]
        print("csv.reader:", row)

# --- Using pandas: read and save with custom delimiter and decimal ---
df = pd.DataFrame({"name": ["foo", "bar"], "value": [1.23, 4.56]})

# Save with semicolon delimiter and comma as decimal separator
df.to_csv("temp/example_pandas_locale.csv", sep=";", decimal=",", index=False)

# Read with matching settings
df2 = pd.read_csv("temp/example_pandas_locale.csv", sep=";", decimal=",")
print("pandas read_csv:\n", df2)
