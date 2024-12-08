from nba_api.stats.endpoints import PlayerGameLog, PlayerEstimatedMetrics, PlayerGameLogs
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages

season = "2024-25"

def get_player_id(player_name: str = None):

    from nba_api.stats.static import players

    players_dict = players.get_players()
    player = next((player for player in players_dict if player['full_name'].lower() == player_name.lower()), None)
    player_id = player['id'] if player else None

    return player_id

def moving_avg(stat, ax, player_name: str = None):

    from datasets import games_df

    player_id = get_player_id(player_name)

    if (player_id != None):

        data = games_df
        data['GAME_DATE'] = pd.to_datetime(data['GAME_DATE'])
        data = data[data['PLAYER_ID'] == player_id]

        window_size = 10
        data[f'{stat}_Moving_Avg'] = data[stat].rolling(window=window_size).mean()

        last_avg = round(data[f'{stat}_Moving_Avg'].iloc[-1], 2)
        mean = round(data[stat].mean(), 2)
        perc_above = round(100*len(data[data[stat] > mean]) / len(data), 2)
        perc_under = round(100*len(data[data[stat] < mean]) / len(data), 2)
        perc_diff = round(100*(last_avg-mean)/mean, 2)

        ax.set_title(stat)
        ax.set_ylim(0, max(data[stat])*1.1)
        ax.tick_params(axis='x', size=6)
        ax.tick_params(axis='y', size=6)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax.scatter(data['GAME_DATE'], data[stat], color='gray', alpha=0.5, s=10)
        ax.plot(data['GAME_DATE'], data[f'{stat}_Moving_Avg'], color='blue', label=f'Moving Average: {last_avg} ({perc_diff}%)')
        ax.axhline(mean, color='red', alpha=0.5, ls='--', label=f'Mean: {mean}')
        ax.plot([], [], label=f'Above mean: {perc_above}%')
        ax.plot([], [], label=f'Under mean: {perc_under}%')
        ax.legend(fontsize=7, loc='upper left')

def rank_analysis(stat, ax, player_name: str = None):

    from datasets import players_df

    player_id = get_player_id(player_name)

    if (player_id != None):

        players_df = players_df[players_df['GP'] > players_df['GP'].max()/2].reset_index(drop=True)

        data_players = players_df[players_df['PLAYER_ID'] != player_id].reset_index(drop=True)
        data_player = players_df[players_df['PLAYER_ID'] == player_id].reset_index(drop=True)

        if 'PCT' in stat:
            ax.set_title(f'{stat.split("_")[0]}: {data_player[f"{stat}_RANK"].values[0]}º - {round(100*data_player[stat].values[0], 2)}%')
        else:
            ax.set_title(f'{stat}: {data_player[f"{stat}_RANK"].values[0]}º - {data_player[stat].values[0]}')
        ax.scatter([0] * len(data_players), data_players[stat], color='gray', alpha=0.3)
        ax.scatter([0], data_player[stat], color='red', s=150, marker='*')
        ax.scatter([0], players_df[stat].mean(), color='blue', s=200, marker='_')
        ax.tick_params(axis='x', size=6)
        ax.tick_params(axis='y', size=6)
        ax.spines['left'].set_visible(True)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_xticklabels([])
        ax.tick_params(bottom=False)
        ax.grid(True, axis='y', linestyle='dashed', linewidth=0.5)

def usg_ts_plot(season, player_name: str = None):

    '''
    If a player name is informed, it returns his USG vs TS chart.
    '''

    from datasets import players_advanced_stats_df

    pdf_name = f'{player_name}.pdf'

    if (player_name != None):

        player_id = get_player_id(player_name)

        with PdfPages(pdf_name) as pdf:

            df = players_advanced_stats_df
            df = df[df['GP'] >= 10]
            
            df_player = df[df['PLAYER_ID'] == player_id]
            
            if not df_player.empty:
                plt.suptitle('USG vs TS')
                plt.xlabel('USG Percentage')
                plt.ylabel('TS Percentage')
                plt.scatter(df['USG_PCT'], df['TS_PCT'], label='Rest of the league')
                plt.scatter(df_player['USG_PCT'], df_player['TS_PCT'], label=player_name)
                plt.legend(fontsize=7)
                plt.tight_layout()
                plt.show()
                #pdf.savefig()

def off_def_rating_plot(season, player_name: str = None):

    from datasets import players_advanced_stats_df

    pdf_name = f'{player_name}.pdf'

    if (player_name != None):

        player_id = get_player_id(player_name)

        with PdfPages(pdf_name) as pdf:

            df = players_advanced_stats_df
            df = df[df['GP'] >= 10]
            
            df_player = df[df['PLAYER_ID'] == player_id]

            import matplotlib.colors as mcolors

            norm = mcolors.Normalize(vmin=df['NET_RATING'].min(), vmax=df['NET_RATING'].max())
            colors = plt.cm.RdYlGn(norm(df['NET_RATING']))
            
            if not df_player.empty:
                plt.suptitle('NET RATING')
                plt.xlabel('DEF RATING')
                plt.ylabel('OFF RATING')
                plt.scatter(df['DEF_RATING'], df['OFF_RATING'], s=abs(df['NET_RATING'])*5, label='Rest of the league', c=colors, alpha=0.7)
                plt.scatter(df_player['DEF_RATING'], df_player['OFF_RATING'], s=abs(df_player['NET_RATING'])*5, label=f"{player_name}: {df_player['NET_RATING'].values[0]}", color='blue', alpha=0.7)
                plt.legend(fontsize=7)
                plt.tight_layout()
                plt.show()
                #pdf.savefig()

def scrape_player_image(player_name):

    import requests
    from bs4 import BeautifulSoup
    from io import BytesIO
    from PIL import Image
    import matplotlib.image as mpimg

    url = 'https://pt.wikipedia.org/wiki/'
    for i, name in enumerate(player_name.split(' ')):
        url = url + name if i == 0 else url + '_' + name

    response = requests.get(url)
    response.raise_for_status()
    main_page = BeautifulSoup(response.text, 'lxml')
    image_url = 'https:' + main_page.find_all('img', {'class': lambda x: x and 'mw-file-element' in x})[0].attrs['src']
    
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    
    return image

def get_player_info(player_name):

    from nba_api.stats.endpoints import commonplayerinfo

    player_id = get_player_id(player_name)

    if player_id:
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        data = player_info.get_normalized_dict()
        return data['CommonPlayerInfo'][0]