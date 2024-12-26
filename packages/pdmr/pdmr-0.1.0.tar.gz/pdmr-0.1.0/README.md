# pandas_multiprocess_runner

A library for running functions on Pandas DataFrames with multiprocessing and checkpointing, supporting both synchronous and asynchronous execution.

## Installation

```bash
pip install pdmr
```

## Usage
```python
from pdmr import PandasMultiprocessRunner
import pandas as pd

# Example usage with your inference logic:
def my_inference_function(index, prompt, response_a, response_b):
    # ... your inference logic using get_response and construct_prompt ...
    return {
        "result": inference_result,
        "other_data": "example"
    }

# Sample DataFrame (replace with your 'train' DataFrame)
data = {
    "Index": range(5),
    "prompt": ["prompt1", "prompt2", "prompt3", "prompt4", "prompt5"],
    "response_a": ["response_a1", "response_a2", "response_a3", "response_a4", "response_a5"],
    "response_b": ["response_b1", "response_b2", "response_b3", "response_b4", "response_b5"]
}
df = pd.DataFrame(data).set_index('Index')

runner = PandasMultiprocessRunner(
    my_inference_function,
    df,
    checkpoint_interval=2,
    output_dir="my_results",
    use_async=False  # or True for asynchronous
)
results_df = runner.run("prompt", "response_a", "response_b")

print(results_df)
```

```tree
pandas_multiprocess_runner/
├── pandas_multiprocess_runner/
│   ├── __init__.py
│   ├── core.py         # Core logic for processing and checkpointing
│   ├── utils.py        # Helper functions (e.g., for checkpointing)
│   └── exceptions.py   # Custom exception classes
├── tests/
│   ├── __init__.py
│   └── test_core.py    # Unit tests for core.py
├── setup.py           # Package metadata and installation
├── README.md          # Project description and usage instructions
├── requirements.txt   # Project dependencies
└── examples.py        # Example usage of the library
```