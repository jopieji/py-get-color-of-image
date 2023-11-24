import requests

url = "https://api-football-v1.p.rapidapi.com/v3/standings"
headers = {
    'X-RapidAPI-Key': '',  # Replace with your RapidAPI key
}

league_ids = [39, 140, 78, 88, 135, 61, 94, 253]
url_list = []
for league_id in league_ids:
    params = {'season': '2022', 'league': league_id}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        standings_data = response.json()
        teams = standings_data['response'][0]['league']['standings'][0]

        for team in teams:
            team_name = team['team']['id']
            team_logo_url = team['team']['logo']
            url_list.append(team_logo_url)
            print(f"logo url for {team_name}: {team_logo_url}")
    else:
        print(f"Failed to retrieve data for League ID {league_id}")
