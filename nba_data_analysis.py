from nba_api.stats.endpoints import PlayerGameLog
from nba_api.stats.static import players
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

player_name = "Jarrett Allen"

players_dict = players.get_players()
player = next((player for player in players_dict if player['full_name'].lower() == player_name.lower()), None)
player_id = player['id'] if player else None

if player_id:
    # Obter dados jogo a jogo
    game_log = PlayerGameLog(player_id=player_id, season="2024-25", season_type_all_star="Regular Season")
    data = game_log.get_data_frames()[0]

    data = data.sort_index(ascending=False).reset_index(drop=True)

    data['GAME_DATE'] = pd.to_datetime(data['GAME_DATE'])

    window_size = 5
    for column in data.columns[6:-2]:
        data[f'{column}_Moving_Avg'] = data[column].rolling(window=window_size).mean()
    data['PLUS_MINUS_Moving_Sum'] = data['PLUS_MINUS'].rolling(window=window_size).sum()

    print(data.head())

    column = 0
    row = 0
    columns = ['PTS','AST','REB','STL','BLK','TOV']
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(18,9))
    for i in range(len(columns)):
        last_avg = round(data[f'{columns[i]}_Moving_Avg'].iloc[-1],2)
        mean = round(data[columns[i]].mean(),2)
        ax[row,column].set_title(columns[i])
        ax[row,column].set_ylim(0, max(data[columns[i]])*1.1)
        ax[row,column].tick_params(axis='x', size=6)
        ax[row,column].tick_params(axis='y', size=6)
        ax[row,column].xaxis.set_major_locator(mdates.MonthLocator())
        ax[row,column].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax[row,column].scatter(data['GAME_DATE'], data[columns[i]], color='gray', alpha=0.5, label=columns[i])
        #ax[row,column].scatter(data['GAME_DATE'], data[columns[i]])
        ax[row,column].plot(data['GAME_DATE'], data[f'{columns[i]}_Moving_Avg'], color='blue', label=f'Moving Average: {last_avg}')
        #ax[row,column].scatter(data['GAME_DATE'], data[f'{columns[i]}_Moving_Avg'])
        ax[row,column].axhline(mean, color='red', alpha=0.5, ls='--', label=f'Mean: {mean}')
        ax[row,column].legend()
        if i % 2 == 0:
            row = 1
        else:
            row = 0
            column += 1
    plt.suptitle('Last 5 Games Moving Average')
    plt.tight_layout()
    plt.show()

pass