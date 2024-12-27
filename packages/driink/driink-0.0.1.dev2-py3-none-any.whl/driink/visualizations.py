from tqdm import tqdm


def display_progress(percent, drank, goal):
    bar_length = 100  # Total length of the progress bar
    current = int(percent)  # The current progress value
    with tqdm(total=bar_length, bar_format="{l_bar}{bar}|") as pbar:
        pbar.set_description(f"{drank} ml / {goal} ml")
        pbar.update(current)
