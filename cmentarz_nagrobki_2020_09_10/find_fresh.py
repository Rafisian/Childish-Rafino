import pandas as pd
import geopandas as gpd

zombies = pd.read_excel('F:\cmentarz\cmentarz_nagrobki_2020_09_10\Zmarli_2020_09_10.xlsx')
graves = gpd.read_file('F:\cmentarz\cmentarz_nagrobki_2020_09_10\cmentarz_nagrobki_2020_09_10_multipolygon.shp')
graves_poli = gpd.read_file('F:\cmentarz\cmentarz_nagrobki_2020_09_10\cmentarz_nagrobki_2020_09_10_multipolygon.shp')
zombies.sort_values(['DataZgonu'],ascending=[True])

#okrojenie warstwy zombies do trzech atrybutów - dla celów złączeniowych i pod kątem filtrowania
selected = zombies[['DpIdGrobu','NazwiskoImie','DataZgonu']]

## Zmiana geometrii warstwy graves na punktową (centroidy)

pts = graves.copy()
pts['geometry'] = pts['geometry'].centroid

## Stworzenie pól z koordynatami centroidów

pts['Lon'] = pts['geometry'].x
pts['Lat'] = pts['geometry']. y

## Stworzenie pola z połączonymi koordynatami - można skopiować i wlepić w google maps

pts['coords'] = pts['Lat'].astype(str) + ',' + pts['Lon'].astype(str)

## Konwersja graves na dataframe w celu przyłączenia koordynatów do denackich personaliów

graves = pd.DataFrame(pts)
result = selected.merge(graves[['idgrobu1','coords']],left_on='DpIdGrobu', right_on='idgrobu1')

## Kontrolny wydruk pięciu ostatnich pozycji

print(result[['NazwiskoImie','DataZgonu','coords']].tail(5))

## Przyłączenie kolumny z geometrią do dataframe'a z denatami

result = zombies.merge(graves_poli[['idgrobu1','geometry']],left_on='DpIdGrobu', right_on='idgrobu1')
# print(result[['NazwiskoImie','DataZgonu','geometry']].tail(5))

## Sortowanie zbioru w celu wyciągnięcia Leopoldów; zapis do geojsona

result = result[result['Imie1'] == 'Leopold']
result = gpd.GeoDataFrame(result, geometry='geometry')
result.to_file("F:\cmentarz\leopolds.geojson",driver='GeoJSON')