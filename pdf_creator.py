from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

from functions import scrape_player_image, get_player_info, moving_avg

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

    pag1 = plt.figure(figsize=(8.5, 11))
    gs = gridspec.GridSpec(5, 1)

    ax1 = pag1.add_subplot(gs[0, 0]) 
    ax1.text(0.5, 1, player_name, fontsize=24, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    if player_team[-1] == 's':
        ax1.text(0.5, 0.5, f"{player_team}' {player_position}", fontsize=20, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    else:
        ax1.text(0.5, 0.5, f"{player_team}'s {player_position}", fontsize=20, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    ax1.text(0.5, 0.2, f'{player_height}" - {player_weight} lbs', fontsize=20, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    ax1.set_axis_off()

    ax2 = pag1.add_subplot(gs[1:, 0])
    image = scrape_player_image(player_name)
    ax2.imshow(image)
    ax2.set_axis_off()

    pdf.savefig(pag1)
    plt.close(pag1)

    #########################################
    # Second page

    plt.figure(figsize=(8.5, 11))

    plt.text(0.5, 1, 'Defense Stats - Rank', fontsize=24, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    plt.gca().set_axis_off()

    pdf.savefig()
    plt.close()

    #########################################
    # Third page

    pag2 = plt.figure(figsize=(8.5, 11))

    plt.text(0.5, 1, 'Defense Stats - Rank', fontsize=24, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')
    gs = gridspec.GridSpec(7, 2)
    ax = pag2.add_subplot(gs[0, :])
    ax.set_axis_off()

    moving_avg('2024-25', ['REB','DREB','OREB','STL','BLK','PF'], pdf, pag2, gs, player_name)

    #########################################
    # Fourth page

    pag3 = plt.figure(figsize=(8.5, 11))
    gs = gridspec.GridSpec(9, 2)

    ax1 = pag3.add_subplot(gs[0, :])
    ax1.text(0.5, 1, 'Defense Stats', fontsize=24, fontname='Times New Roman', color='black', horizontalalignment='center', fontweight='bold')

    pdf.savefig(pag3)
    plt.close(pag3)