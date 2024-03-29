import os
import secrets
import string

import matplotlib.pyplot as plt
import numpy as np


def GenerateChart(personality_percentages):
    # Define Chart titles
    titles = ['Introversion', 'Extroversion', 'Sensing', 'Intuition', 'Thinking', 'Feeling', 'Judging', 'Perceiving']

    # Number of categories
    num_categories = len(personality_percentages)

    # Define angles for radar chart
    angles = np.linspace(0, 2 * np.pi, num_categories, endpoint=False).tolist()

    # Make the plot close to a circle
    personality_percentages += [personality_percentages[0]]
    angles += angles[:1]

    # Create radar chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, personality_percentages, color='red', alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(titles)

    # Add percentage labels
    for angle, percentage in zip(angles, personality_percentages):
        ax.text(angle, percentage, f'{percentage:.4f}%', ha='center', va='center')

    # Add title to the chart
    ax.set_title('Personality Radar Chart', va='bottom')

    # Save the plot as an HD image
    alphabet = string.ascii_letters + string.digits
    secure_string = ''.join(secrets.choice(alphabet) for _ in range(16))
    current_directory = os.path.dirname(os.path.abspath(__file__))
    root_directory = current_directory
    while not os.path.exists(os.path.join(root_directory, 'manage.py')):
        root_directory = os.path.dirname(root_directory)
    image_path = f"{root_directory}\\media\\personalities\\{secure_string}.png"
    fig.savefig(image_path, dpi=300)  # Set DPI to 300 for HD image
    plt.close(fig)

    return image_path


# Example usage:
# personality_percentages = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]  # Example percentages
# image_path = generate_chart(personality_percentages)
