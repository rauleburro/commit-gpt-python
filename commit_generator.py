"""
commit_generator.py

This module provides functionality to generate and handle git commit messages using the OpenAI API. It retrieves the git diff, generates a commit message based on the diff, optionally allows the user to provide a custom commit prefix, combines the prefix and the generated message, copies the final commit message to the clipboard, prints the commit message to the screen, asks for user confirmation before performing the commit, and if confirmed, performs the git commit with the generated message.

Modules:
    os: Provides a way of using operating system dependent functionality.
    sys: Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
    subprocess: Allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
    pyperclip: A cross-platform clipboard module for Python.
    dotenv: Reads key-value pairs from a .env file and can set them as environment variables.
    openai: Provides access to the OpenAI API.

Functions:
    get_git_diff(): Obtains the changes with 'git diff --staged', excluding package-lock.json.
    generate_commit_message(diff): Generates a commit message using the OpenAI API.
    make_git_commit(message): Performs the Git commit.
    main(): Main function to generate and handle git commit messages.

"""
import os
import sys
import subprocess
import pyperclip
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from the .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OpenAI API Key not found. Please ensure it's configured in the .env file.")
    exit(1)

client = OpenAI(api_key=api_key)


def get_git_diff():
    """Obtains the changes with 'git diff --staged', excluding package-lock.json, pnpm-lock.yaml, yarn.lock, and .svg files."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--staged', '--', '.',
                ':(exclude)package-lock.json',
                ':(exclude)pnpm-lock.yaml',
                ':(exclude)yarn.lock',
                ':(exclude)*.svg'],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error obtaining diffs: {e}")
        return ""


def generate_commit_message(diff):
    """Generates a commit message using the OpenAI API."""
    if not diff:
        return "No changes found."

    prompt = f"""You are an assistant that generates clear and concise commit messages following GitHub standards.
You not only describe what was done, but also identify the changes and the affected files. The commit message must be in English.

Generate a commit message for the following diff:

{diff}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=10000
        )

        commit_message = response.choices[0].message.content.strip()
        return commit_message or "Failed to generate a commit message."
    except Exception as e:
        print(f"Error generating commit message: {e}")
        return "Error generating commit message."


def make_git_commit(message):
    """Performs the Git commit."""
    try:
        subprocess.run(['git', 'commit', '-m', message], check=True)
        print("✅ Commit successfully made.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error performing commit: {e}")


def main():
    """
    Main function to generate and handle git commit messages.

    This function performs the following steps:
    1. Retrieves the git diff.
    2. Generates a commit message based on the diff.
    3. Optionally, allows the user to provide a custom commit prefix.
    4. Combines the prefix and the generated message.
    5. Copies the final commit message to the clipboard.
    6. Prints the commit message to the screen.
    7. Asks for user confirmation before performing the commit.
    8. If confirmed, performs the git commit with the generated message.

    If there are no changes to commit, it prints a warning and exits.

    Args:
        None

    Returns:
        None
    """
    diff = get_git_diff()
    if not diff:
        print("⚠️ No changes to commit.")
        return

    generated_commit_message = generate_commit_message(diff)

    # Ask the user for a custom commit prefix
    commit_prefix = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

    # Combine the prefix and the generated message
    if commit_prefix:
        final_commit_message = f"{commit_prefix}\t{generated_commit_message}"
    else:
        final_commit_message = generated_commit_message

    # Copy final commit message to clipboard
    pyperclip.copy(final_commit_message)
    print("📋 Commit message copied to clipboard.")

    # Print the commit message to the screen
    print("\nGenerated commit message:")
    print("------------------------------------------------")
    print(final_commit_message)
    print("------------------------------------------------\n")

    # Confirm before performing the commit
    confirm = input(
        "Do you want to perform the commit? (y/n): ").strip().lower()
    if confirm == "y":
        make_git_commit(final_commit_message)
    else:
        print("❌ Commit cancelled.")


if __name__ == "__main__":
    main()
