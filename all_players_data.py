from nba_api.stats.endpoints import leaguedashplayerstats

season = "2024-25"

players_stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season)
players_stats_df = players_stats.get_data_frames()[0]

players_advanced_stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season,
                                                                     measure_type_detailed_defense='Advanced',  # Estatísticas avançadas
                                                                     per_mode_detailed='PerGame')
players_advanced_stats_df = players_advanced_stats.get_data_frames()[0]
