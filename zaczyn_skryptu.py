import pandas as pd

file_location = "F:\cmentarz\cmentarz_nagrobki_2020_09_10\Zmarli_2020_09_10.xlsx"
df = pd.read_excel(file_location)
sorted = df.sort_values(by = 'DataZgonu', ascending=False)

sorted = sorted[~sorted.DataZgonu.isnull()]
sorted = sorted[~sorted.NazwiskoImie.isnull()]

fresh = sorted.head(5)
print(fresh[['NazwiskoImie','DataZgonu']])