from nba_api.stats.endpoints import leaguedashplayerstats, PlayerGameLogs, PlayerCareerStats
import pandas as pd

####################################
# games_df

def get_games_df(season, player_id):

    game_log_base = PlayerGameLogs(season_nullable=season, season_type_nullable="Regular Season", player_id_nullable=player_id)
    game_log_base = game_log_base.get_data_frames()[0]
    game_log_base = game_log_base.sort_index(ascending=False).reset_index(drop=True)

    game_log_advanced = PlayerGameLogs(season_nullable=season, season_type_nullable="Regular Season", player_id_nullable=player_id, measure_type_player_game_logs_nullable='Advanced')
    game_log_advanced = game_log_advanced.get_data_frames()[0]
    game_log_advanced = game_log_advanced.sort_index(ascending=False).reset_index(drop=True)

    games_df = pd.merge(game_log_base, game_log_advanced, on=['SEASON_YEAR', 'PLAYER_ID', 'TEAM_ID','GAME_ID', 'GAME_DATE'], how='inner')

    columns_with_y = [col for col in games_df.columns if '_y' in col]
    games_df = games_df.drop(columns=columns_with_y)

    games_df.columns = [col.replace('_x', '') if '_x' in col else col for col in games_df.columns]

    games_df['GAME_DATE'] = pd.to_datetime(games_df['GAME_DATE'])

    return games_df

####################################
# players_df

def get_players_df(season):

    players_stats_base = leaguedashplayerstats.LeagueDashPlayerStats(season=season, per_mode_detailed="PerGame")
    players_stats_base = players_stats_base.get_data_frames()[0]

    players_stats_advanced = leaguedashplayerstats.LeagueDashPlayerStats(season=season, measure_type_detailed_defense='Advanced', per_mode_detailed='PerGame')
    players_stats_advanced = players_stats_advanced.get_data_frames()[0]

    players_df = pd.merge(players_stats_base, players_stats_advanced, on=['PLAYER_ID'], how='inner')

    columns_with_y = [col for col in players_df.columns if '_y' in col]
    players_df = players_df.drop(columns=columns_with_y)

    players_df.columns = [col.replace('_x', '') if '_x' in col else col for col in players_df.columns]

    return players_df

####################################
# carreer_df

def get_career_df(player_id):

    career = PlayerCareerStats(player_id=player_id, per_mode36='PerGame')
    career_df = career.get_data_frames()[0]

    return career_df