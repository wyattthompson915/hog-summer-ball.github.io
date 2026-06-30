from bs4 import BeautifulSoup
import requests
import pandas as pd

### CAPE COD HITTING

columns = [
    "Player", "Team", "G", "AB", "R", "H", "2B", "3B", "HR",
    "RBI", "BB", "SO", "SB", "CS", "AVG", "OBP", "SLG", "OPS"
]

headers = {"User-Agent": "Mozilla/5.0"}

teams = [
    "bourne",
    "",
    "chatham",
    "cotuit",
    "falmouth",
    "harwich",
    "hyannis",
    "orleans",
    "wareham",
    "yarmouth-dennis"
]

all_data = []

for team in teams:
    url = f"https://www.capecodleague.com/brewster/stats/{team}?playerPool=ALL"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("table tbody tr")

    for row in rows:
        # Get the player name
        th = row.find("th")
        if th:
            link = th.find("a")
            player = link.get("aria-label") if link else th.get_text(" ", strip=True)
        else:
            player = ""

        # Get the rest of the stats
        stats = [td.get_text(strip=True) for td in row.find_all("td")]

        if stats:
            all_data.append([player] + stats)

df = pd.DataFrame(all_data, columns=columns)

arkansas_players = [
    "Tye Briscoe",
    "Mark Brissey",
    "L Cornelison",
    "Cooper Dossett",
    "Steele Eaves",
    "Colin Fisher",
    "Jackson Kircher",
    "Peyton Lee",
    "Jordan Martin",
    "C Turner",
    "Nolan Traeger",
    "C Rutenbar"
]

ark_df = df[df['Player'].isin(arkansas_players)]

### CAPE COD PICHING

columns = [
    "Player", "Team", "W", "L", "ERA", "G", "GS", "CG", 
    "SHO", "SV", "SVO", "IP", "H", "R", "ER", "HR", "HB",
    "BB", "SO", "WHIP", "AVG"
]

headers = {"User-Agent": "Mozilla/5.0"}

teams = [
    "bourne",
    "",
    "chatham",
    "cotuit",
    "falmouth",
    "harwich",
    "hyannis",
    "orleans",
    "wareham",
    "yarmouth-dennis"
]

all_data = []

for team in teams:
    url = f"https://www.capecodleague.com/brewster/stats/pitching/{team}?playerPool=ALL"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("table tbody tr")

    for row in rows:
        # Get the player name
        th = row.find("th")
        if th:
            link = th.find("a")
            player = link.get("aria-label") if link else th.get_text(" ", strip=True)
        else:
            player = ""

        # Get the rest of the stats
        stats = [td.get_text(strip=True) for td in row.find_all("td")]

        if stats:
            all_data.append([player] + stats)

df_pitching = pd.DataFrame(all_data, columns=columns)
df_pitching = df_pitching.drop(columns=['CG', 'SHO', 'SVO'])
make_numeric = ['SO', 'IP', 'BB']
for col in make_numeric:
    df_pitching[col] = pd.to_numeric(df_pitching[col])
df_pitching['k/9'] = round((df_pitching['SO'] / df_pitching['IP']) * 9,2)
df_pitching['k/bb'] = round(df_pitching['SO'] / df_pitching['BB'],2)

df_pitching

ark_df_pitching = df_pitching[df_pitching['Player'].isin(arkansas_players)]

### CALIFORNIA COLLEGIATE LEAGUE

columns = [
    'Rk', 'Name', 'Team', 'gp', 'ab', 'h', 'rbi',
    'bb', '2b', '3b', 'hr', 'xbh', 'k', 'avg', 'obp',
    'slg', 'hbp', 'sf', 'sh', 'hdp', 'go', 'fo', 'go/fo', 'pa'
]

headers = {"User-Agent": "Mozilla/5.0"}

all_data = []

url = f"https://calsummerball.com/sports/bsb/2026/players?pos=h&sort=avg"
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# Grab only the FIRST table on the page (the main hitting table)
first_table = soup.select("table")[0]
rows = first_table.select("tbody tr")

for row in rows:
    stats = [td.get_text(strip=True) for td in row.find_all("td")]

    if stats:
        all_data.append(stats)

df_ccl = pd.DataFrame(all_data, columns=columns)
df_ccl['Name'] = df_ccl['Name'].str.replace(r'\s+', ' ', regex=True).str.strip()

ark_ccl = df_ccl[(df_ccl['Name'].isin(arkansas_players))]




### now we gotta scrape Cornelison separately 
all_data = []

columns = [
    'Rk', 'Name', 'Team', 'gp', 'ab', 'h', 'rbi',
    'bb', '2b', '3b', 'hr', 'xbh', 'k', 'avg', 'obp',
    'slg', 'hbp', 'sf', 'sh', 'hdp', 'go', 'fo', 'go/fo', 'pa'
]

url = "https://calsummerball.com/sports/bsb/2026/players/lukecornelisonegb6"
res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(res.text, "html.parser")

table = soup.select("table")[0]
rows = table.find_all("tr")

stat_map = {
    'Games': 'G', 'Plate appearances': 'PA', 'At Bats': 'AB',
    'Runs': 'R', 'Hits': 'H', 'Doubles': '2B', 'Triples': '3B',
    'Home Runs': 'HR', 'Runs Batted In': 'RBI', 'Total bases': 'TB',
    'Walks': 'BB', 'Hit by pitch': 'HBP', 'Strikeouts': 'SO',
    'Sacrifice Flies': 'SF', 'Sacrifice Hits': 'SH',
    'Hit into double play': 'HDP', 'Stolen Bases': 'SB',
    'Caught Stealing': 'CS', 'Batting Average': 'AVG',
    'On Base Percentage': 'OBP', 'Slugging Percentage': 'SLG'
}

player_stats = {'Player': 'L Cornelison', 'Team': 'CCL'}

for row in rows:
    tds = [td.get_text(strip=True) for td in row.find_all("td")]
    if len(tds) < 2:
        continue
    label = tds[0]
    val = tds[1].replace('-', '0')  # overall value
    if label in stat_map:
        player_stats[stat_map[label]] = val

cornelison = pd.DataFrame([player_stats])

cornelison = cornelison[['Player', 'Team', 'G', 'AB', 'H', 'RBI', 'BB', '2B', '3B', 
                         'HR', 'SO', 'AVG', 'SLG', 'OBP']]
table8 = soup.select("table")[8]
headers = ['era', 'w', 'l', 'app', 'gs', 'sv', 'ip', 'h', 'r', 'er', 'bb', 'k', 'k/9', 'hr', 'whip', 'bf', 'wp', 'hbp']

rows = table8.find_all("tr")
data_rows = [row for row in rows if row.find_all("td") and any(td.get_text(strip=True) for td in row.find_all("td"))]

tds = [td.get_text(strip=True) for td in data_rows[0].find_all("td")]

cornelison_pitching = dict(zip(headers, tds))
cornelison_pitching['Player'] = 'L Cornelison'
cornelison_pitching['Team'] = 'Santa Barbara Foresters'
cornelison_pitching = {k: (0 if v == '-' else v) for k, v in cornelison_pitching.items()}

cornelison_pitching_df = pd.DataFrame([cornelison_pitching])

# Rename to match Cape Cod pitching columns
cornelison_pitching_df = cornelison_pitching_df.rename(columns={
    'app': 'G', 'gs': 'GS', 'sv': 'SV', 'ip': 'IP',
    'h': 'H', 'r': 'R', 'er': 'ER', 'bb': 'BB',
    'k': 'SO', 'hr': 'HR', 'whip': 'WHIP',
    'w': 'W', 'l': 'L', 'era': 'ERA',
    'bf': 'BF', 'wp': 'WP', 'hbp': 'HB'
})

cornelison_pitching_df = cornelison_pitching_df[['Player', 'Team', 'W', 'L', 'ERA', 'G', 'GS', 'SV', 'IP', 'H', 'R', 'ER', 'HR', 'HB', 'BB', 'SO', 'WHIP', 'k/9']]
for col in make_numeric:
    cornelison_pitching_df[col] = pd.to_numeric(cornelison_pitching_df[col])
cornelison_pitching_df['k/bb'] = round(cornelison_pitching_df['SO'] / cornelison_pitching_df['BB'],2)




ark_ccl = ark_ccl.rename(columns={
    'Name': 'Player',
    'gp': 'G',
    'ab': 'AB',
    'h': 'H',
    'rbi': 'RBI',
    'bb': 'BB',
    '2b': '2B',
    '3b': '3B',
    'hr': 'HR',
    'k': 'SO',
    'avg': 'AVG',
    'obp': 'OBP',
    'slg': 'SLG'
})
ark_ccl = ark_ccl.drop(columns=['Rk', 'xbh', 'hbp', 'sf', 'sh', 'hdp', 'go', 'fo', 'go/fo', 'pa'])
cornelison.loc[0, 'Team'] = 'Santa Barbara Foresters'
ark_ccl = pd.concat([ark_ccl, cornelison])
ark_ccl['OBP'] = pd.to_numeric(ark_ccl['OBP'])
ark_ccl['SLG'] = pd.to_numeric(ark_ccl['SLG'])
ark_ccl['OPS'] = ark_ccl['OBP'] + ark_ccl['SLG']
ark_ccl = ark_ccl.replace('-', 0).infer_objects(copy=False)

print(ark_ccl)


ark_df.to_json(
    "data/batters.json",
    orient="records",
    indent=2
)

ark_df_pitching.to_json(
    "data/pitchers.json",
    orient="records",
    indent=2
)

ark_ccl.to_json(
    "data/batters_ccl.json",
    orient="records",
    indent=2
)

cornelison_pitching_df.to_json(
    "data/pitchers_ccl.json",
    orient="records",
    indent=2
)


# MLB draft league
# maginnis, hering, 
