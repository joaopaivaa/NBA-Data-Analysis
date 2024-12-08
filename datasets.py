from nba_api.stats.endpoints import leaguedashplayerstats, PlayerGameLogs
import pandas as pd

season = "2024-25"

####################################
# games_df

game_log_base = PlayerGameLogs(season_nullable=season, season_type_nullable="Regular Season")
game_log_base = game_log_base.get_data_frames()[0]
game_log_base = game_log_base.sort_index(ascending=False).reset_index(drop=True)

game_log_advanced = PlayerGameLogs(season_nullable=season, season_type_nullable="Regular Season", measure_type_player_game_logs_nullable='Advanced')
game_log_advanced = game_log_advanced.get_data_frames()[0]
game_log_advanced = game_log_advanced.sort_index(ascending=False).reset_index(drop=True)

games_df = pd.merge(game_log_base, game_log_advanced, on=['SEASON_YEAR', 'PLAYER_ID', 'TEAM_ID','GAME_ID', 'GAME_DATE'], how='inner')

columns_with_y = [col for col in games_df.columns if '_y' in col]
games_df = games_df.drop(columns=columns_with_y)

games_df.columns = [col.replace('_x', '') if '_x' in col else col for col in games_df.columns]

####################################
# players_df

players_stats_base = leaguedashplayerstats.LeagueDashPlayerStats(season=season, per_mode_detailed="PerGame")
players_stats_base = players_stats_base.get_data_frames()[0]

players_stats_advanced = leaguedashplayerstats.LeagueDashPlayerStats(season=season, measure_type_detailed_defense='Advanced', per_mode_detailed='PerGame')
players_stats_advanced = players_stats_advanced.get_data_frames()[0]

players_df = pd.merge(players_stats_base, players_stats_advanced, on=['PLAYER_ID'], how='inner')

columns_with_y = [col for col in players_df.columns if '_y' in col]
players_df = players_df.drop(columns=columns_with_y)

players_df.columns = [col.replace('_x', '') if '_x' in col else col for col in players_df.columns]
