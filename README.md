# Commit-GPT-Python

`Commit-GPT-Python` is a Python script that automatically generates commit messages based on the staged changes in your Git repository using the OpenAI API. 

The script combines a custom commit prefix (provided as a command-line argument) with a generated message, producing a clear and concise commit message that follows GitHub standards.

## Features

- Automatic Diff Retrieval: Retrieves the staged changes (excluding `package-lock.json`) using Git.
- AI-Powered Commit Messages: Utilizes the OpenAI API to generate a commit message by analyzing the diff.
- Custom Commit Prefix: Allows you to prepend a custom commit prefix by passing it as a command-line argument.
- Clipboard Support: Copies the final commit message to your clipboard for ease of use.
- Interactive Confirmation: Displays the complete commit message and asks for confirmation before performing the commit.

## Requirements

- Python: Version 3.7 or later (Python 3.8+ is recommended).
- Git: Installed and configured on your system.
- OpenAI API Key: A valid API key from `OpenAI` (https://openai.com/).

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/commit-gpt-python.git
cd commit-gpt-python
```

2.  Create and activate a virtual environment (venv):

    - On macOS/Linux:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    - On Windows:

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Set up your OpenAI API Key:
    Create a `.env` file in the root directory of the project and add the following line (replace `your_openai_api_key_here` with your actual API key):

    ```bash
    OPENAI_API_KEY=your_openai_api_key_here
    ```

2.  Ensure you have staged changes in your Git repository.

## Usage

Run the script by passing your custom commit prefix as a command-line argument. For example:

`python generate_commit.py “Fix: Corrected typo in README”`

The script will:

- Retrieve the staged changes using `git diff –staged` (excluding `package-lock.json`).
- Generate a commit message using the OpenAI API.
- Combine your custom prefix with the generated message.
- Copy the final commit message to your clipboard.
- Display the complete commit message in the terminal.
- Ask for confirmation before executing the Git commit.

## License

This project is licensed under the `MIT License`. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests with improvements or bug fixes.

## Disclaimer

This project leverages the OpenAI API to generate commit messages. Please be aware that using the OpenAI API may incur costs, and heavy or unmonitored usage could result in unexpectedly high bills. It is your responsibility to monitor your API usage and associated expenses. Always review the generated commit message before confirming the commit, and use the API responsibly.