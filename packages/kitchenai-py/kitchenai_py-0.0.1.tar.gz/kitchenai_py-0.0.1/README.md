# KitchenAIWrapper SDK

The `KitchenAIWrapper` SDK is a Python wrapper around the `kitchenai-python-sdk`, providing a simplified interface for interacting with the KitchenAI API. This wrapper handles common tasks and offers additional functionality, such as streaming queries.

## Requirements

- Python 3.11+

## Installation

### Using pip

If the package is hosted on a repository, you can install it directly using:

```sh
pip install kitchenai-py
```

### Using Setuptools

Alternatively, you can install the package using Setuptools:

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

## Usage

### Importing the Package

After installation, import the package in your Python script:

```python
from kitchenai_py import KitchenAIWrapper
```

### Getting Started

Here's a quick example to get you started with the `KitchenAIWrapper`:

```python
from kitchenai_py import KitchenAIWrapper

# Initialize the wrapper
wrapper = KitchenAIWrapper(host="http://localhost")

# Perform a query
response = wrapper.query("example_label", "example_query", stream=True)

# Print the response
print(response)
```

## API Methods

### `query(label, query, stream=False, metadata=None)`

- **label**: The label for the query.
- **query**: The query string.
- **stream**: (Optional) Boolean flag to enable streaming. Default is `False`.
- **metadata**: (Optional) Additional metadata for the query.

## Error Handling

The wrapper includes basic error handling for API exceptions. If an error occurs during an API call, it will print an error message to the console.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

## Author

Your Name or Organization