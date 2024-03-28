import matplotlib.pyplot as plt
import mpld3
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
        ax.text(angle, percentage, f'{percentage}%', ha='center', va='center')

    # Add title to the chart
    ax.set_title('Personality Radar Chart', va='bottom')

    # Show the plot
    return plt.show()
