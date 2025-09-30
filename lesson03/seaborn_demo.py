# Import necessary libraries
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

PATH = "datasets/concrete_compressive_strength/Concrete_Data.csv"

# Load the Concrete dataset
dataset = pd.read_csv(PATH)

dataset.rename(
    columns={
        "Cement (component 1)(kg in a m^3 mixture)": "cement",
        "Blast Furnace Slag (component 2)(kg in a m^3 mixture)": "slag",
        "Fly Ash (component 3)(kg in a m^3 mixture)": "fly_ash",
        "Water  (component 4)(kg in a m^3 mixture)": "water",
        "Superplasticizer (component 5)(kg in a m^3 mixture)": "superplasticizer",
        "Coarse Aggregate  (component 6)(kg in a m^3 mixture)": "coarse_aggregate",
        "Fine Aggregate (component 7)(kg in a m^3 mixture)": "fine_aggregate",
        "Age (day)": "age",
        "Concrete compressive strength(MPa, megapascals) ": "strength",
    },
    inplace=True,
)

x_axis = "coarse_aggregate"
y_axis = "strength"
hue = "age"

# # Cap the age at 28 (marking everything above 28 as 28)
# dataset["age"] = dataset["age"].apply(lambda x: 28 if x > 28 else x)
# dataset = dataset[(250 < dataset["cement"]) & (dataset["cement"] < 450)]

# # Let's check the unique values in the age column after capping
# print("Unique age values after capping:", sorted(dataset["age"].unique()))

# -------------------------------
# 1. Visualization using Seaborn
# -------------------------------
# plt.figure(figsize=(8, 6))
# sns.histplot(data=dataset, x=x_axis, bins=30, kde=True)
# plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(data=dataset, x=x_axis, y=y_axis, hue=hue, palette="flare")
plt.title("Concrete Compressive Strength (Seaborn)")
plt.show()


# -------------------------------
# 2. Visualization using Plotly
# -------------------------------
# fig = px.scatter(
#     dataset,
#     x="cement",
#     y="strength",
#     color="age",
#     size_max=15,
#     title="Concrete Compressive Strength (Plotly)",
# )
# fig.show()
