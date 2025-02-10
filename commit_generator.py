from dotenv import load_dotenv
import pyperclip
import os
import subprocess
from openai import OpenAI


# Cargar las variables de entorno desde el archivo .env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_git_diff():
    """Obtiene los cambios en git diff --staged, excluyendo package-lock.json."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--staged', '--', '.',
                ':(exclude)package-lock.json'],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener los diffs: {e}")
        return ""


def generate_commit_message(diff, api_key):
    """Genera un mensaje de commit usando la API de OpenAI."""
    if not diff:
        return "No se encontraron cambios en los archivos."

    prompt = f"""Eres un asistente que genera mensajes de commit claros y concisos utilizando los estándares de GitHub.
No solo dices qué se hizo, sino que intentas identificar los cambios y los archivos afectados. El mensaje debe estar en inglés.

Genera un mensaje de commit para el siguiente diff:

{diff}
"""

    try:
        response = client.chat.completions.create(model="gpt-4o",
                                                  messages=[
                                                      {"role": "system", "content": prompt}],
                                                  max_tokens=10000)

        commit_message = response.choices[0].message.content.strip()
        return commit_message or "No se pudo generar un mensaje."
    except Exception as e:
        print(f"Error al generar el mensaje de commit: {e}")
        return "Error al generar el mensaje."


def make_git_commit(message):
    """Realiza el commit en Git."""
    try:
        subprocess.run(['git', 'commit', '-m', message], check=True)
        print("✅ Commit realizado con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al realizar el commit: {e}")


def main():
    # Cargar la API Key desde las variables de entorno
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No se encontró la API Key de OpenAI. Asegúrate de tenerla configurada en el archivo .env.")
        return

    diff = get_git_diff()
    if not diff:
        print("⚠️ No hay cambios para commitear.")
        return

    commit_message = generate_commit_message(diff, api_key)
    print(f"\n🔹 Mensaje generado: \"{commit_message}\"")

    # Copiar mensaje al portapapeles
    pyperclip.copy(commit_message)
    print("📋 Mensaje copiado al portapapeles.")

    # Confirmación antes del commit
    confirm = input("¿Deseas realizar el commit? (y/n): ").strip().lower()
    if confirm == "y":
        make_git_commit(commit_message)
    else:
        print("❌ Commit cancelado.")


if __name__ == "__main__":
    main()
