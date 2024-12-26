import unittest
import pandas as pd
import os
import shutil
from pdmr.core import PandasMultiprocessRunner
from pdmr.utils import save_checkpoint, load_checkpoint
import ast
import time
# Define sum_columns outside the test method
def sum_columns(index, A, B):
    return {"sum": A + B}

def strip_result(result: str):
    result = result.replace("'", "\"")
    return ast.literal_eval(result)
    

class TestPandasMultiprocessRunner(unittest.TestCase):
    def setUp(self):
        self.test_output_dir = "test_results"
        os.makedirs(self.test_output_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_output_dir)

    def test_run_with_and_without_checkpoint(self):
        # Test DataFrame with columns A and B
        test_df = pd.DataFrame(
            {"Index": [0, 1, 2, 3, 4], "A": [10, 20, 30, 40, 50], "B": [1, 2, 3, 4, 5]}
        ).set_index("Index")

        # --- Test without checkpoint ---
        runner_no_checkpoint = PandasMultiprocessRunner(
            sum_columns,
            test_df,
            checkpoint_interval=10,  # Set a large interval so no checkpoint is saved
            output_dir=self.test_output_dir,
            output_file_prefix="no_checkpoint_",
        )
        result_df_no_checkpoint = runner_no_checkpoint.run("A", "B")
        
        # Verify results
        self.assertEqual(len(result_df_no_checkpoint), 5)
        for i in test_df.index:
            self.assertEqual(
                strip_result(result_df_no_checkpoint[result_df_no_checkpoint['index'] == i]['result'].to_list()[0])['sum'],
                test_df.loc[i, "A"] + test_df.loc[i, "B"],
            )

        # --- Test with checkpoint ---

        # First, create an incomplete run and save a checkpoint
        runner_with_checkpoint_incomplete = PandasMultiprocessRunner(
            sum_columns,
            test_df,
            checkpoint_interval=2,  # Checkpoint every 2 rows
            output_dir=self.test_output_dir,
            output_file_prefix="with_checkpoint_"
        )

        # Create incomplete result list
        incomplete_results = []
        for i in range(2):
          incomplete_results.append(runner_with_checkpoint_incomplete._process_row(test_df.index[i], test_df.loc[test_df.index[i],'A'], test_df.loc[test_df.index[i],'B']))
        save_checkpoint(incomplete_results, 0, self.test_output_dir, "with_checkpoint_")

        # Now, create a new runner to simulate resuming from the checkpoint
        runner_with_checkpoint_resumed = PandasMultiprocessRunner(
            sum_columns,
            test_df,
            checkpoint_interval=2,
            output_dir=self.test_output_dir,
            output_file_prefix="with_checkpoint_"
        )

        result_df_with_checkpoint = runner_with_checkpoint_resumed.run("A", "B")
        # Verify results
        self.assertEqual(len(result_df_with_checkpoint), 5)
        

        for i in test_df.index:
            self.assertEqual(
                strip_result(result_df_with_checkpoint.loc[i, "result"])["sum"],
                test_df.loc[i, "A"] + test_df.loc[i, "B"],
            )