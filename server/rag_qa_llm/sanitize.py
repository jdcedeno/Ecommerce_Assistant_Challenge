import pandas as pd

df = pd.read_csv("./data/Product_Information_Dataset.csv",
                           encoding="utf-8",
                           sep=",",
                           quotechar='"',
                           dtype=str)

# print(df.head(30))
print(df.info())

df = df.dropna()

df.to_csv("./data/product_data_clean.csv", index=False)