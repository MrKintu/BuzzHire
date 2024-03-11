import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# Function to plot graphs for each dichotomy pair
def plot_graphs(user_responses, sex_info):
    # Example scatter plot (Replace with your data)
    for i in range(4):  # Plot for each dichotomy pair
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=user_responses[:, i], y=user_responses[:, i + 1], hue=sex_info)
        plt.xlabel('Response 1')
        plt.ylabel('Response 2')
        plt.title(f'Scatter Plot of Dichotomy Pair {i + 1}')
        plt.legend(title='Sex', loc='upper right')
        plt.show()

    # Example bar plots (Replace with your data)
    for i in range(4):  # Plot for each dichotomy pair
        plt.figure(figsize=(8, 6))
        sns.countplot(x=user_responses[:, i], hue=sex_info)
        plt.xlabel('Response')
        plt.ylabel('Number of Users')
        plt.title(f'Bar Graph of Dichotomy Pair {i + 1}')
        plt.legend(title='Sex', loc='upper right')
        plt.show()


# Function to plot radar charts for each individual's responses
def plot_radar_charts(user_responses):
    # Define personality types (Replace with your actual types)
    personality_types = ['INTJ', 'INTP', 'ENTJ', 'ENTP',
                         'INFJ', 'INFP', 'ENFJ', 'ENFP',
                         'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
                         'ISTP', 'ISFP', 'ESTP', 'ESFP']

    num_personalities = len(personality_types)
    angles = np.linspace(0, 2 * np.pi, num_personalities, endpoint=False).tolist()
    angles += angles[:1]  # Ensure the radar chart is closed

    # Plot radar chart for each user
    for i, user_response in enumerate(user_responses):
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, user_response, color='skyblue', alpha=0.5)
        ax.set_yticklabels([])
        ax.set_title(f'Radar Chart for User {i + 1}')

        # Add markers for each personality type
        ax.plot(angles, user_response, color='blue', linewidth=2, linestyle='solid')
        ax.fill(angles, user_response, color='blue', alpha=0.25)

        # Label each personality type
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(personality_types)

        plt.show()


# Example usage
if __name__ == "__main__":
    responses = np.random.randint(1, 8, size=(100, 4))  # Example user responses
    sex = np.random.choice(['Male', 'Female'], size=100)  # Example sex information
    plot_graphs(responses, sex)
    plot_radar_charts(responses)
