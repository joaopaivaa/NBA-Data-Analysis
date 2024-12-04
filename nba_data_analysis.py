from nba_api.stats.endpoints import PlayerGameLog

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages

season = "2024-25"

def moving_avg_analysis(season, team_abb: str = None, player_name: str = None):

    from all_players_data import all_players_df

    '''
    If a player name is informed, it returns only his moving average chart
    If a team abbreviation is informed, it returns its players moving average charts
    If nothing is informed, it returns the moving average charts for player with more than 10 games played'''

    if (player_name == None) and (team_abb == None):
        all_players_df = all_players_df[all_players_df['GP'] > 10].reset_index(drop=True)
        pdf_name = 'Multiple Players - Moving Average Analysis.pdf'
    elif player_name != None:
        all_players_df = all_players_df[all_players_df['PLAYER_NAME'] == player_name].reset_index(drop=True)
        pdf_name = f'{player_name} - Moving Average Analysis.pdf'
    elif team_abb != None:
        all_players_df = all_players_df[(all_players_df['TEAM_ABBREVIATION'] == team_abb) & (all_players_df['GP'] > 10)].reset_index(drop=True)
        pdf_name = f'{team_abb} - Moving Average Analysis.pdf'

    with PdfPages(pdf_name) as pdf:

        for i in range(len(all_players_df)):

            player_name = all_players_df['PLAYER_NAME'][i]
            player_id = all_players_df['PLAYER_ID'][i]

            game_log = PlayerGameLog(player_id=player_id, season=season, season_type_all_star="Regular Season")

            data = game_log.get_data_frames()[0]
            data = data.sort_index(ascending=False).reset_index(drop=True)
            data['GAME_DATE'] = pd.to_datetime(data['GAME_DATE'])

            window_size = 10
            for column in data.columns[6:-2]:
                data[f'{column}_Moving_Avg'] = data[column].rolling(window=window_size).mean()
            data['PLUS_MINUS_Moving_Sum'] = data['PLUS_MINUS'].rolling(window=window_size).sum()

            column = 0
            row = 0
            columns = ['PTS','AST','REB','STL','BLK','TOV']
            fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(18,9))
            for i in range(len(columns)):
                last_avg = round(data[f'{columns[i]}_Moving_Avg'].iloc[-1],2)
                mean = round(data[columns[i]].mean(),2)
                perc_above = round(100*len(data[data[columns[i]] > mean]) / len(data), 2)
                perc_under = round(100*len(data[data[columns[i]] < mean]) / len(data), 2)
                perc_diff = round(100*(last_avg-mean)/mean, 2)
                ax[row,column].set_title(columns[i])
                ax[row,column].set_ylim(0, max(data[columns[i]])*1.1)
                ax[row,column].tick_params(axis='x', size=6)
                ax[row,column].tick_params(axis='y', size=6)
                ax[row,column].xaxis.set_major_locator(mdates.MonthLocator())
                ax[row,column].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
                ax[row,column].scatter(data['GAME_DATE'], data[columns[i]], color='gray', alpha=0.5, label=columns[i])
                ax[row,column].plot(data['GAME_DATE'], data[f'{columns[i]}_Moving_Avg'], color='blue', label=f'Moving Average: {last_avg} ({perc_diff}%)')
                ax[row,column].axhline(mean, color='red', alpha=0.5, ls='--', label=f'Mean: {mean}')
                ax[row,column].plot([], [], label=f'Above mean: {perc_above}%')
                ax[row,column].plot([], [], label=f'Under mean: {perc_under}%')
                ax[row,column].legend(fontsize=6)
                if i % 2 == 0:
                    row = 1
                else:
                    row = 0
                    column += 1
            plt.suptitle(f'Last {window_size} Games Moving Average: {player_name}')
            plt.tight_layout()
            pdf.savefig()

moving_avg_analysis(season,'GSW')