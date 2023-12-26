import math
import os
import pickle
from collections import defaultdict
import plotly.graph_objs as go


def build_presentation_data():
    base_dir = 'context_pickles'
    word_frequencies = defaultdict(lambda: defaultdict(int))
    for username in os.listdir(base_dir):
        user_dir = os.path.join(base_dir, username)
        if os.path.isdir(user_dir):
            for file in os.listdir(user_dir):
                if file.endswith('.pkl'):
                    file_path = os.path.join(user_dir, file)
                    with open(file_path, 'rb') as f:
                        words = pickle.load(f)
                        if words is not None:
                            for word in words:
                                word_frequencies[username][word] += 1
    # sort the words by frequency for each user
    for username in word_frequencies:
        word_frequencies[username] = dict(sorted(word_frequencies[username].items(), key=lambda x: x[1], reverse=True))
    return word_frequencies


def build_knowledge_graph(word_frequencies, limit_words):
    # Collect all unique words from all users and find global max frequency for each word
    global_word_freq = {}
    for user, words in word_frequencies.items():
        for word, freq in words.items():
            if word not in global_word_freq or global_word_freq[word] < freq:
                global_word_freq[word] = freq

    # Limit the number of words
    for user, words in word_frequencies.items():
        if len(words) > limit_words:
            word_frequencies[user] = dict(sorted(words.items(), key=lambda item: item[1], reverse=True)[:limit_words])
    print(word_frequencies)

    # Define the radius for users and words
    user_layer_radius = 100
    word_layer_radius = 150

    # Calculate positions
    def calculate_positions(user_words_dict, inner_radius, outer_radius):
        users = list(user_words_dict.keys())
        total_users = len(users)
        user_positions = {}
        word_positions = {}
        angle_gap = 2 * math.pi / total_users

        for i, user in enumerate(users):
            angle = i * angle_gap
            user_positions[user] = (inner_radius * math.cos(angle), inner_radius * math.sin(angle))
            words = user_words_dict[user]
            for j, word in enumerate(words):
                if word not in word_positions:
                    word_angle = angle + angle_gap * (j - len(words) / 2) / len(words)
                    word_positions[word] = (outer_radius * math.cos(word_angle), outer_radius * math.sin(word_angle))

        return user_positions, word_positions

    user_positions, word_positions = calculate_positions(word_frequencies, user_layer_radius, word_layer_radius)

    # Create edges
    edge_x = []
    edge_y = []
    for user, words in word_frequencies.items():
        user_x, user_y = user_positions[user]
        for word in words:
            word_x, word_y = word_positions[word]
            edge_x.extend([user_x, word_x, None])
            edge_y.extend([user_y, word_y, None])

    # User trace
    user_trace = go.Scatter(
        x=[pos[0] for pos in user_positions.values()],
        y=[pos[1] for pos in user_positions.values()],
        mode='markers+text',
        text=list(user_positions.keys()),
        marker=dict(size=50, color='orange'))

    # Word trace
    max_global_freq = max(global_word_freq.values())
    word_trace = go.Scatter(
        x=[pos[0] for pos in word_positions.values()],
        y=[pos[1] for pos in word_positions.values()],
        mode='markers+text',
        text=list(word_positions.keys()),
        marker=dict(size=[10 + 100 * (global_word_freq[word] / max_global_freq) for word in global_word_freq.keys()],
                    color='red'))

    # Edge trace
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create the figure
    fig = go.Figure(data=[edge_trace, user_trace, word_trace],
                    layout=go.Layout(
                        title='Workforce Context - Knowledge Graph',
                        showlegend=False,
                        hovermode='closest',
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    save_path = f"context_knowledge_graphs/KG_{limit_words}.html"
    fig.write_html(save_path)
    print(f"Knowledge graph is saved to {save_path} successfully.")
    # clean the figure
    fig = None
    return


if __name__ == "__main__":
    freqs = build_presentation_data()
    build_knowledge_graph(freqs, 20)
