import pandas as pd

def load_colors(file_path):
    return pd.read_csv(file_path)

def get_color_name(R, G, B, df):
    min_distance = float('inf')
    closest_color = "Unknown"
    for _, row in df.iterrows():
        dist = abs(R - row["R"]) + abs(G - row["G"]) + abs(B - row["B"])
        if dist < min_distance:
            min_distance = dist
            closest_color = row["color_name"]
    return closest_color
