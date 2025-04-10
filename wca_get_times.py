'''
Buscar todos los competidores apuntados al torneo y sacar sus tiempo medios y best
'''
import requests
from bs4 import BeautifulSoup


base_url = "https://www.worldcubeassociation.org/competitions/SpanishChampionship2024/registrations"
base_url = "https://www.worldcubeassociation.org/competitions/URJCOpen2025/registrations"
base_url = "https://www.worldcubeassociation.org/competitions/GetafeOpen2025/registrations"

input_file = 'getafe_2025_4.html'
# response = requests.get(base_url) # requiere auth???
with open(input_file, "r", encoding="utf-8") as f:
    html_content = f.read()
# soup = BeautifulSoup(response.text, 'html.parser')
soup = BeautifulSoup(html_content, 'lxml')

links = soup.find_all('a', href=lambda href: href and "persons" in href)

# Extract and print the href values
hrefs = [link['href'] for link in links][1:]

person_base_url = 'https://www.worldcubeassociation.org'
data = []
for person in hrefs:
    try:
        url = person_base_url + person
        person_reponse = requests.get(url)
        soup = BeautifulSoup(person_reponse.text, 'html.parser')
        single_value = soup.find('a', {"class": "plain"}, href="/results/rankings/333/single").text.strip()
        average_value = soup.find('a', {"class": "plain"}, href="/results/rankings/333/average").text.strip()
        data.append([person.split("/")[-1], single_value, average_value])
    except Exception as e:
        print(f"ERROR con person: {person}")

def mm_ss_to_s(o):
    """Pasar minutos segundos decimales a segundos con decimales
    Input - O:
        1:34.43 --> 94.43
    """
    if o == '':
        return 10000
    if ":" in o:
        m = o.split(":")[0]
        s = o.split(":")[1]
    else:
        m = 0
        s = o
    if "." in s:
        ms = s.split(".")[1]
        s = s.split(".")[0]
    else:
        ms = 0
    return float(m)*60 + float(s) + float(ms)/100

new_data = []
for d in data:
    new_data.append([d[0], mm_ss_to_s(d[1]), mm_ss_to_s(d[2])])


import pandas as pd
df = pd.DataFrame(new_data)
df.columns = ["person", "single", "average"]

output_file = f'{input_file.replace(".", "_")}.csv'
df.to_csv(output_file)
df["single"] = df["single"].astype(float)
type(df["single"][3])
print(f'Mediana single: {df["single"].quantile(0.5)}')
print(f'75% single: {df["single"].quantile(0.75)}')
print(f'75% average: {df["average"].quantile(0.75)}')

for i in range(1, 100, 5):
    print(f'{i}% average: {df["average"].quantile(i/100)}')

for i in range(1, 100, 5):
    print(f'{i}% single: {df["single"].quantile(i/100)}')
