# README.md

# Blockhouse SDK

The Blockhouse SDK is a Python library designed to facilitate the interaction with AWS S3 buckets. It provides a simple interface for uploading data from local storage to S3, making it easier to manage your cloud storage needs.

## Features

- Upload files to AWS S3 buckets
- Configure AWS credentials
- Handle errors with custom exceptions

## Installation

To install the Blockhouse SDK, you can use pip:

```bash
pip install blockhouse-sdk
```

## Usage

Here's a quick example of how to use the Blockhouse SDK to upload a file to S3:

```python
from blockhouse.client import BlockhouseClient

# Initialize the client
client = BlockhouseClient()

# Configure AWS credentials
client.configure(aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')

# Upload a file to S3
client.upload_to_s3('local_file.txt', 'your-bucket-name', 's3_file.txt')
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.