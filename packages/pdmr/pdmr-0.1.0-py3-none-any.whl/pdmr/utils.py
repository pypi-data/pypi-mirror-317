import pandas as pd
import os
from .exceptions import CheckpointError

def save_checkpoint(results_list, checkpoint_num, output_dir, output_file_prefix):
    """Saves the current results to a CSV file."""
    df_checkpoint = pd.DataFrame(results_list)
    output_filename = os.path.join(
        output_dir, f"{output_file_prefix}{checkpoint_num}.csv"
    )
    df_checkpoint.to_csv(output_filename, index=False)
    print(f"Checkpoint {checkpoint_num} saved to {output_filename}")

def load_checkpoint(output_dir, output_file_prefix):
    """Loads the latest checkpoint and returns processed indices."""
    processed_indices = set()
    latest_checkpoint = -1
    for filename in os.listdir(output_dir):
        if filename.startswith(output_file_prefix) and filename.endswith(".csv"):
            try:
                checkpoint_number = int(filename[len(output_file_prefix) : -4])
                if checkpoint_number > latest_checkpoint:
                    latest_checkpoint = checkpoint_number

                df_checkpoint = pd.read_csv(os.path.join(output_dir, filename))
                processed_indices.update(df_checkpoint["index"].tolist())
            except Exception as e:
                print(f"Error processing checkpoint file {filename}: {e}")
                # You might want to raise an exception here to stop the process
                # if a checkpoint file is corrupted.

    return processed_indices, latest_checkpoint