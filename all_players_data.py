from nba_api.stats.endpoints import leaguedashplayerstats

season = "2024-25"

players_stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season)
all_players_df = players_stats.get_data_frames()[0]
