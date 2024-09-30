import os
import sys
import subprocess  # Ensure subprocess is imported
from openai import OpenAI

def main(api_key):
    if not api_key:
        print("Error: OpenAI API key is missing.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Read the existing task introduction
    task_file_path = os.path.join("tasks", "new_task.md")
    try:
        with open(task_file_path, "r") as file:
            task_description = file.read()
    except FileNotFoundError:
        print("Error: new_task.md file not found.")
        sys.exit(1)

    language = os.getenv("TASK_LANGUAGE", "English")
    learning_goals = os.getenv("LEARNING_GOALS", "")

    # Generate each module sequentially
    preparation = generate_preparation(client, language)
    learning_goals_section = generate_learning_goals(client, learning_goals, language)
    assignment = generate_assignment(client, language)
    exercises = generate_exercises(client, language)

    # Append modules to the task description
    with open(task_file_path, "a") as file:
        file.write("\n\n## Preparation\n\n")
        file.write(preparation)
        file.write("\n\n## Learning Goals\n\n")
        file.write(learning_goals_section)
        file.write("\n\n## Assignment\n\n")
        file.write(assignment)
        for idx, exercise in enumerate(exercises):
            file.write(f"\n\n### Exercise {idx+1}\n\n")
            file.write(exercise)

    # Commit and push changes
    commit_and_push_changes(task_file_path)

def generate_preparation(client, language):
    prompt = (
        f"In {language}, list the preparation steps students should take before starting the task. "
        f"Include any necessary readings, resources, or prerequisites."
    )
    return generate_with_retries(client, prompt)

def generate_learning_goals(client, learning_goals, language):
    prompt = (
        f"In {language}, outline the learning goals for the task, focusing on:\n{learning_goals}. "
        f"Present them in a clear, bullet-point format."
    )
    return generate_with_retries(client, prompt)

def generate_assignment(client, language):
    prompt = (
        f"In {language}, provide a detailed assignment description. "
        f"Explain what students are expected to do, including any specific requirements or guidelines."
    )
    return generate_with_retries(client, prompt)

def generate_exercises(client, language):
    exercises = []
    difficulty_levels = ["easy", "medium", "hard", "harder", "hardest"]
    previous_content = ""
    for idx, difficulty in enumerate(difficulty_levels):
        prompt = (
            f"In {language}, create exercise {idx+1} with {difficulty} difficulty. "
            f"Each exercise should build upon the previous ones and align with the learning goals. "
            f"Ensure the exercise is challenging and well-suited for students to deepen their understanding."
        )
        exercise = generate_with_retries(client, prompt)
        exercises.append(exercise)
        previous_content += f"\n\n{exercise}"
    return exercises

def generate_with_retries(client, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specialized in generating educational content."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating content: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
    print("Failed to generate content after multiple retries.")
    sys.exit(1)

def commit_and_push_changes(task_file_path):
    try:
        # Configure Git locally
        subprocess.run(["git", "config", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "config", "user.name", "GitHub Actions"], check=True)

        subprocess.run(["git", "add", task_file_path], check=True)
        subprocess.run(["git", "commit", "-m", "Add task modules"], check=True)
        subprocess.run(["git", "push"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error committing and pushing changes: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Missing required command line argument 'api_key'")
        sys.exit(1)

    api_key = sys.argv[1]

    main(api_key)