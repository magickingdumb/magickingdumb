import os
import pandas as pd

path = r"C:\Users\tross\OneDrive\Desktop\SSS"
dataframes = []

for file in os.listdir(path):
    dataframes.append(pd.read_excel(os.path.join(path, file)))

result = pd.concat(dataframes, axis=0, ignore_index=True)
result.to_excel("all_invoices_extracted.xlsx", index=False)
