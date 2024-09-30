import os
import sys
import subprocess  # Ensure subprocess is imported
import re
from openai import OpenAI

def main(api_key, branch_name):
    if not api_key:
        print("Error: OpenAI API key is missing.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Read the task description
    task_file_path = os.path.join("tasks", "new_task.md")
    try:
        with open(task_file_path, "r") as file:
            task_description = file.read()
    except FileNotFoundError:
        print("Error: new_task.md file not found.")
        sys.exit(1)

    # Extract exercises
    exercises = extract_exercises(task_description)

    # Generate solutions for each exercise
    for exercise in exercises:
        solution = generate_solution_for_exercise(client, exercise)
        write_solution_to_file(exercise['number'], solution)

    # Commit and push changes
    commit_and_push_changes(branch_name)

def extract_exercises(task_description):
    # Use regex to find exercise sections
    pattern = r'### Exercise (\d+)\n\n(.*?)\n(?=###|$)'
    matches = re.findall(pattern, task_description, re.DOTALL)
    exercises = []
    for match in matches:
        exercise = {
            'number': match[0],
            'content': match[1]
        }
        exercises.append(exercise)
    return exercises

def generate_solution_for_exercise(client, exercise):
    prompt = (
        f"Based on the following exercise, provide a complete and correct Java solution. "
        f"Ensure the solution meets all requirements and is well-documented.\n\n"
        f"### Exercise {exercise['number']}\n"
        f"{exercise['content']}\n\n"
        "Provide only the code without explanations or comments."
    )
    return generate_with_retries(client, prompt)

def write_solution_to_file(exercise_number, solution_content):
    # Ensure the .hidden_tasks directory exists
    hidden_tasks_dir = os.path.join(".hidden_tasks")
    os.makedirs(hidden_tasks_dir, exist_ok=True)

    # Write the solution to a file
    file_name = f"Exercise_{exercise_number}_Solution.java"
    file_path = os.path.join(hidden_tasks_dir, file_name)

    with open(file_path, "w") as file:
        file.write(solution_content)

def generate_with_retries(client, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specialized in generating Java code."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating solution: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
    print("Failed to generate solution after multiple retries.")
    sys.exit(1)

def commit_and_push_changes(branch_name):
    try:
        # Configure Git locally
        subprocess.run(["git", "config", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "config", "user.name", "GitHub Actions"], check=True)

        subprocess.run(["git", "add", ".hidden_tasks"], check=True)
        subprocess.run(["git", "commit", "-m", "Add generated solutions"], check=True)
        subprocess.run(
            ["git", "push", "--set-upstream", "origin", branch_name],
            check=True,
            env=dict(os.environ, GIT_ASKPASS='echo', GIT_USERNAME='x-access-token', GIT_PASSWORD=os.getenv('GITHUB_TOKEN'))
        )
    except subprocess.CalledProcessError as e:
        print(f"Error committing and pushing changes: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error: Missing required command line arguments 'api_key' and 'branch_name'")
        sys.exit(1)

    api_key = sys.argv[1]
    branch_name = sys.argv[2]

    main(api_key, branch_name)
