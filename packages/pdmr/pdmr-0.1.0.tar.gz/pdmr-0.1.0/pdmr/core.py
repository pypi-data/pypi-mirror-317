# pandas_multiprocess_runner/core.py
import pandas as pd
import time
import os
import concurrent.futures
from tqdm import tqdm
from .utils import save_checkpoint, load_checkpoint
from .exceptions import CheckpointError

class PandasMultiprocessRunner:
    def __init__(
        self,
        func,
        df,
        checkpoint_interval=100,
        output_dir="results",
        output_file_prefix="results_",
        max_workers=None,
        use_async=False
    ):
        self.func = func
        self.df = df
        self.checkpoint_interval = checkpoint_interval
        self.output_dir = output_dir
        self.output_file_prefix = output_file_prefix
        self.max_workers = max_workers or os.cpu_count()
        self.use_async = use_async

        os.makedirs(self.output_dir, exist_ok=True)

    def _process_row(self, index, *args):
        """Wraps the user-provided function with error handling."""
        try:
            result = self.func(index, *args)
            return {
                "index": index,
                "result": result,
                "error": None,
                "timestamp": time.time(),
            }
        except Exception as e:
            return {
                "index": index,
                "error": str(e),
                "timestamp": time.time(),
            }
    
    def _get_executor(self):
      """Returns the appropriate executor based on whether async is enabled."""
      if self.use_async:
          return concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)
      else:
          return concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers)

    def run(self, *args):
        """
        Runs the processing logic.

        Args:
            *args: Arguments to be passed to the user-defined function.

        Returns:
            pd.DataFrame: The DataFrame containing the results.
        """
        start_time = time.time()
        results = []
        processed_count = 0
        checkpoint_num = 0

        processed_indices, latest_checkpoint = load_checkpoint(
            self.output_dir, self.output_file_prefix
        )

        if latest_checkpoint >= 0:
            checkpoint_num = latest_checkpoint
            print(f"Resuming from checkpoint {checkpoint_num}")

        remaining_rows = self.df[~self.df.index.isin(processed_indices)]

        with self._get_executor() as executor:
            if self.use_async:
              futures = {
                executor.submit(self._process_row, row.Index, *[getattr(row, arg) for arg in args]): row
                for row in remaining_rows.itertuples()
              }
            else:
              futures = {
                executor.submit(self._process_row, row.Index, *[getattr(row, arg) for arg in args]): row
                for row in remaining_rows.itertuples()
              }

            for future in tqdm(
                concurrent.futures.as_completed(futures),
                total=remaining_rows.shape[0],
                desc="Processing rows",
            ):
                try:
                    result = future.result()
                    results.append(result)
                    processed_count += 1

                    if processed_count % self.checkpoint_interval == 0:
                        checkpoint_num += 1
                        save_checkpoint(
                            results,
                            checkpoint_num,
                            self.output_dir,
                            self.output_file_prefix,
                        )
                        results = []

                except Exception as e:
                    print(f"Error processing row: {e}")

        if results:
            checkpoint_num += 1
            save_checkpoint(
                results, checkpoint_num, self.output_dir, self.output_file_prefix
            )

        end_time = time.time()
        print(f"Total processing time: {end_time - start_time:.2f} seconds")

        # Combine Checkpoints
        try:
            final_df = self._combine_checkpoints()
            final_df.to_csv(
                os.path.join(self.output_dir, "final_results.csv"), index=False
            )
            print("Final results saved to final_results.csv")
            return final_df

        except CheckpointError as e:
            print(e)
            return None

    def _combine_checkpoints(self):
        """Combines checkpoint files into a single DataFrame."""
        try:
            all_results_df = pd.concat(
                [
                    pd.read_csv(os.path.join(self.output_dir, f))
                    for f in os.listdir(self.output_dir)
                    if f.startswith(self.output_file_prefix) and f.endswith(".csv")
                ],
                ignore_index=True,
            )
            all_results_df.sort_values("index", inplace=True)
            return all_results_df
        except Exception as e:
            raise CheckpointError(
                f"Error combining checkpoint files: {e}"
            )