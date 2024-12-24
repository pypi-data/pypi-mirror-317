# Watermarking Language Models via a Frequency Based Constrained Decoding Mechanism

Constrained Decoding has often been used as a technique to ensure robust structured outputs by language models, but in this project we explore its usage in the setting of watermarking language model responses as an inference-time technique. A user can ensure that each sliding window of a given size has a maximum frequency of a certain token adhering to user input. Users can simply create dictionaries of constraints on token frequencies, and language model responses will adhere to these in any given sliding window in the response.

## Installation

You can get started with this project by cloning the repository or installing the package via pip.

### Clone the Repository

```sh
git clone https://github.com/ajuneja23/constrainedFrequencyDecodingWatermark.git
cd constrainedFrequencyDecodingWatermark
```

### Install via pip

```sh
pip install constraint-watermark
```

## Usage

After installation, you can use the constrained decoding mechanism to watermark language model responses. Create dictionaries of constraints on token frequencies, and the language model will adhere to these constraints in any given sliding window in the response.

## Example

Here is a simple example to demonstrate how to use the constrained watermarking:

```python
from constraint-watermark import ConstrainedDecoder

# Define your constraints
constraints = {
    "token1": 2,
    "token2": 1,
    # Add more tokens and their frequency constraints if needed
}

# Initialize the constrained decoder
decoder = ConstrainedDecoder(
    model_name="gpt2",  # Replace with your model name or path
    constraints_dict=constraints,
    device="cpu",  # Replace with "cuda" or "mps" if available
    window_size=50,  # Set the window size if needed
)

# Generate a response with constraints
response = decoder.decode(prompt="Your input text here", max_new_toks=50)
print(response)
```

## Contributing

We welcome contributions to improve this project. Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
