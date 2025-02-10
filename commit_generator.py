import sys
from dotenv import load_dotenv
import pyperclip
import os
import subprocess
from openai import OpenAI

# Load environment variables from the .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OpenAI API Key not found. Please ensure it's configured in the .env file.")
    exit(1)

client = OpenAI(api_key=api_key)


def get_git_diff():
    """Obtains the changes with 'git diff --staged', excluding package-lock.json."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--staged', '--', '.',
                ':(exclude)package-lock.json'],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error obtaining diffs: {e}")
        return ""


def generate_commit_message(diff, api_key):
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
    diff = get_git_diff()
    if not diff:
        print("⚠️ No changes to commit.")
        return

    generated_commit_message = generate_commit_message(diff, api_key)

    # Ask the user for a custom commit prefix
    commit_prefix = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

    # Combine the prefix and the generated message
    if commit_prefix:
        final_commit_message = f"{commit_prefix}\n\n{generated_commit_message}"
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
