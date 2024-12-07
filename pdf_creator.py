from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from functions import scrape_player_image, get_player_info

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