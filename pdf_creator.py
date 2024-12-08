from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

from functions import scrape_player_image, get_player_info, moving_avg, rank_analysis

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

    ax2 = pag.add_subplot(gs[1:, 0])
    image = scrape_player_image(player_name)
    ax2.imshow(image)
    ax2.set_axis_off()

    pdf.savefig(pag)
    plt.close(pag)

    #########################################
    # Second page

    pag = plt.figure(figsize=(8.5, 11))

    gs = gridspec.GridSpec(10, 4)

    plt.text(0.5, 1, 'Defense Stats - Rank', fontsize=24, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    plt.gca().set_axis_off()

    ax = pag.add_subplot(gs[1:, 0])
    rank_analysis('REB', ax, player_name)

    ax = pag.add_subplot(gs[1:, 1])
    rank_analysis('STL', ax, player_name)

    ax = pag.add_subplot(gs[1:, 2])
    rank_analysis('BLK', ax, player_name)

    ax = pag.add_subplot(gs[1:, 3])
    rank_analysis('PF', ax, player_name)

    pdf.savefig()
    plt.close()

    #########################################
    # Third page

    pag = plt.figure(figsize=(8.5, 11))
    gs = gridspec.GridSpec(10, 2)

    plt.text(0.5, 1, 'Defense Stats - Over Time', fontsize=24, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    plt.gca().set_axis_off()

    ax = pag.add_subplot(gs[1:4, 0])
    moving_avg('REB', ax, player_name)

    ax = pag.add_subplot(gs[1:4, 1])
    moving_avg('OREB', ax, player_name)

    ax = pag.add_subplot(gs[4:7, 0])
    moving_avg('DREB', ax, player_name)

    ax = pag.add_subplot(gs[4:7, 1])
    moving_avg('STL', ax, player_name)

    ax = pag.add_subplot(gs[7:, 0])
    moving_avg('BLK', ax, player_name)

    ax = pag.add_subplot(gs[7:, 1])
    moving_avg('PF', ax, player_name)

    plt.subplots_adjust(hspace=0.8, wspace=0.2)

    pdf.savefig()
    plt.close()

    #########################################
    # Fourth page

    pag = plt.figure(figsize=(8.5, 11))
    gs = gridspec.GridSpec(9, 2)

    ax1 = pag.add_subplot(gs[0, :])
    ax1.text(0.5, 1, 'Defense Stats', fontsize=24, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')

    pdf.savefig(pag)
    plt.close(pag)