from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import time

from functions import scrape_player_image, get_player_info, moving_avg, rank_analysis, career_analysis

season = '2024-25'

player_name = 'Draymond Green'

player_info = get_player_info(player_name)
player_team = player_info['TEAM_CITY'] + ' ' + player_info['TEAM_NAME']
player_country = player_info['COUNTRY']
player_height = player_info['HEIGHT']
player_weight = player_info['WEIGHT']
player_jersey = player_info['JERSEY']
player_position = player_info['POSITION']

pdf_name = f'{player_name}.pdf'
with PdfPages(pdf_name) as pdf:

    #########################################
    # First page

    pag = plt.figure(figsize=(8.5, 11))
    gs = gridspec.GridSpec(5, 1)

    ax1 = pag.add_subplot(gs[0, 0]) 
    ax1.text(0.5, 1, player_name, fontsize=24, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    if player_team[-1] == 's':
        ax1.text(0.5, 0.5, f"{player_team}' {player_position}", fontsize=20, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    else:
        ax1.text(0.5, 0.5, f"{player_team}'s {player_position}", fontsize=20, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    ax1.text(0.5, 0.2, f'{player_height}" - {player_weight} lbs', fontsize=20, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    ax1.set_axis_off()

    # ax2 = pag.add_subplot(gs[1:, 0])
    # image = scrape_player_image(player_name)
    # ax2.imshow(image)
    # ax2.set_axis_off()

    pdf.savefig(pag)
    plt.close(pag)

    ##################################
    #########################################
    # Second page

    pag = plt.figure(figsize=(8.5, 11))

    gs = gridspec.GridSpec(10, 4)

    plt.text(0.5, 1, 'Defense Stats - Rank', fontsize=24, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    plt.gca().set_axis_off()

    ax = pag.add_subplot(gs[1:, 0])
    rank_analysis(season, 'REB', ax, player_name)

    ax = pag.add_subplot(gs[1:, 1])
    rank_analysis(season, 'STL', ax, player_name)

    ax = pag.add_subplot(gs[1:, 2])
    rank_analysis(season, 'BLK', ax, player_name)

    ax = pag.add_subplot(gs[1:, 3])
    rank_analysis(season, 'PF', ax, player_name)

    pdf.savefig()
    plt.close()

    #########################################
    # Second page

    pag = plt.figure(figsize=(8.5, 11))

    gs = gridspec.GridSpec(20, 2)

    plt.text(0.5, 1, 'Defense Stats - Rank', fontsize=24, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    plt.gca().set_axis_off()

    ax = pag.add_subplot(gs[1:10, 0])
    rank_analysis(season, 'REB', ax, player_name)
    time.sleep(1)

    ax = pag.add_subplot(gs[10:14, 0:])
    moving_avg(season, 'REB', ax, player_name)
    time.sleep(1)

    ax = pag.add_subplot(gs[14:, 0:])
    career_analysis('REB', ax, player_name)
    time.sleep(1)

    pag.subplots_adjust(left=0.10, right=0.95, top=0.95, bottom=0.05, hspace=0.2)

    pdf.savefig()
    plt.close()

    #########################################
    # Third page

    # pag = plt.figure(figsize=(8.5, 11))
    # gs = gridspec.GridSpec(11, 2)

    # plt.text(0.5, 1, 'Defense Stats - Over Time', fontsize=24, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    # plt.gca().set_axis_off()

    # ax = pag.add_subplot(gs[2:5, 0])
    # moving_avg(season, 'REB', ax, player_name)

    # ax = pag.add_subplot(gs[2:5, 1])
    # moving_avg(season, 'OREB', ax, player_name)

    # ax = pag.add_subplot(gs[5:8, 0])
    # moving_avg(season, 'DREB', ax, player_name)

    # ax = pag.add_subplot(gs[5:8, 1])
    # moving_avg(season, 'STL', ax, player_name)

    # ax = pag.add_subplot(gs[8:, 0])
    # moving_avg(season, 'BLK', ax, player_name)

    # ax = pag.add_subplot(gs[8:, 1])
    # moving_avg(season, 'PF', ax, player_name)

    # handles = [plt.Line2D([], [], color='blue', ls='solid', label=f'10 days Moving Average'),
    #            plt.Line2D([], [], color='red', alpha=0.5, ls='--', label=f'Average')]
    # ax = pag.add_subplot(gs[1:2, 0:])
    # ax.legend(handles=handles, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.05))
    # ax.set_axis_off()

    # plt.subplots_adjust(hspace=0.8, wspace=0.2)

    # pdf.savefig()
    # plt.close()

    # #########################################
    # # Fourth page

    # pag = plt.figure(figsize=(8.5, 11))

    # gs = gridspec.GridSpec(10, 4)

    # plt.text(0.5, 1, 'Offense Stats - Rank', fontsize=24, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    # plt.gca().set_axis_off()

    # ax = pag.add_subplot(gs[1:, 0])
    # rank_analysis(season, 'PTS', ax, player_name)

    # ax = pag.add_subplot(gs[1:, 1])
    # rank_analysis(season, 'AST', ax, player_name)

    # ax = pag.add_subplot(gs[1:, 2])
    # rank_analysis(season, 'TOV', ax, player_name)

    # ax = pag.add_subplot(gs[1:, 3])
    # rank_analysis(season, 'FG_PCT', ax, player_name)

    # pdf.savefig()
    # plt.close()

    # #########################################
    # # Fifth page

    # pag = plt.figure(figsize=(8.5, 11))
    # gs = gridspec.GridSpec(11, 2)

    # plt.text(0.5, 1, 'Offense Stats - Over Time', fontsize=24, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    # plt.gca().set_axis_off()

    # ax = pag.add_subplot(gs[2:5, 0])
    # moving_avg(season, 'PTS', ax, player_name)

    # ax = pag.add_subplot(gs[2:5, 1])
    # moving_avg(season, 'AST', ax, player_name)

    # ax = pag.add_subplot(gs[5:8, 0])
    # moving_avg(season, 'TOV', ax, player_name)

    # ax = pag.add_subplot(gs[5:8, 1])
    # moving_avg(season, 'FG_PCT', ax, player_name)

    # ax = pag.add_subplot(gs[8:, 0])
    # moving_avg(season, 'FG3_PCT', ax, player_name)

    # ax = pag.add_subplot(gs[8:, 1])
    # moving_avg(season, 'FT_PCT', ax, player_name)

    # handles = [plt.Line2D([], [], color='blue', ls='solid', label=f'10 days Moving Average'),
    #            plt.Line2D([], [], color='red', alpha=0.5, ls='--', label=f'Average')]
    # ax = pag.add_subplot(gs[1:2, 0:])
    # ax.legend(handles=handles, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.05))
    # ax.set_axis_off()

    # plt.subplots_adjust(hspace=0.8, wspace=0.2)

    # pdf.savefig()
    # plt.close()