import os
import re
import sys
import subprocess
from openai import OpenAI

def main(api_key, branch_name):
    if not api_key:
        print("Error: OpenAI API key is missing.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Read the new task description
    try:
        with open("tasks/new_task.md", "r") as file:
            task_description = file.read()
    except FileNotFoundError:
        print("Error: new_task.md file not found.")
        sys.exit(1)

    # Inspirational code snippet for the solution
    inspirational_code = """
        // Example of a simple class modeling arrays
        /**
        * Reference solutions for Task 5, Arrays
        * @author Linus Östlund
        * This would not have been possible without my computer, a M1 Macbook Air.
        */
        public class Arrays {

            /**
            * Count the average value of array with integers
            * @param array of integers
            * @return the average of element integer sum
            */
            public static int average(int[] array) {
                int sum = 0;
                for (int i = 0; i < array.length; i++) {
                    sum += array[i];
                }
                return sum / array.length;
            }

            /**
            * Count the average value of array with doubles
            * @param array of doubles
            * @return average of array elements
            */
            public static double average(double[] array) {
                double sum = 0;
                for (int i = 0; i < array.length; i++) {
                    sum += array[i];
                }
                return sum / array.length;
            }

            /**
            * Return the element closest to -inf in an array
            * @param array of integers
            * @return smallest element
            */
            public static int smallestElement(int[] array) {
                // we don't ask students to handle empty lists
                if (array.length == 0) {
                    throw new IllegalArgumentException("The list is empty!");
                }
                // find smallest element with a foreach loop
                int min = array[0];
                for (int i = 0; i < array.length; i++) {
                    if (array[i] < min) {
                        min = array[i];
                    }
                }
                return min;
            }

            /**
            * Return a copy of array with the elements reversed
            * @param array
            * @return reversed elements of @param
            */
            public static int[] reverse(int[] array){
                int[] reversed = new int[array.length];
                // Example using two loop variables, but one could also be declared outside the loop
                for (int i = array.length - 1, j = 0; i > 0 || j < array.length; i--, j++) {
                    reversed[j] = array[i];
                }
                return reversed;
            }

            /**
            * Return the even elements of an integer array
            * All numbers n where n % 2 == 0 is even, including 0 and negative numbers.
            * @param array
            * @return an array with the even numbers of @param
            */
            public static int[] evenNumbers(int[] array) {
                int evenNumbers = 0;
                // in order to allocate right size,
                // first count the number of even elements in the array
                for (int i = 0; i < array.length; i++) {
                    if (array[i] % 2 == 0){
                        evenNumbers++;
                    }
                }

                // then populate the new array
                int[] evenArray = new int[evenNumbers];
                for (int i = 0, j = 0; i < array.length; i++) {
                    if (array[i] % 2 == 0) {
                        evenArray[j] = array[i];
                        j++;
                    }
                }
                return evenArray;
            }
        }

        // Example of a simple class using array lists
        import java.util.ArrayList;

        public class SetTheory {

            // The maximum threshold
            private static final int MAX = 100;

            /**
            * Generate an ArrayList between min and max
            * @param min lower bound, inclusive
            * @param max upper bound, non-inclusive
            * @return an ArrayList with all integers in [min, max - 1]
            */
            public static ArrayList<Integer> generateSet(int min, int max) {
                ArrayList<Integer> set = new ArrayList<>();
                if (min >= max) {
                    // return empty list
                    return set;
                } else {
                    // Ternary operator to see if max > 100
                    for (int i = Math.max(min, 0); i < Math.min(max, MAX); i++) {
                        set.add(i);
                    }
                    return set;
                }
            }

            /**
            * Return an ArrayList with the unique elements of a and b combined
            * @param a ArrayList A
            * @param b ArrayList B
            * @return the union of A and B
            */
            public static ArrayList<Integer> union(ArrayList<Integer> a, ArrayList<Integer> b) {
                // make a copy of 'a' by feeding it into the ArrayList constructor
                ArrayList<Integer> union = new ArrayList<>(a);
                for (Integer i : b) {
                    if (!union.contains(i)) {
                        union.add(i);
                    }
                }
                return union;
            }

            /**
            * Return the intersection of two ArrayList
            * @param a ArrayList A
            * @param b ArrayList B
            * @return the intersection of A and B
            */
            public static ArrayList<Integer> intersection(ArrayList<Integer> a, ArrayList<Integer> b) {
                ArrayList<Integer> res = new ArrayList<>();
                for (Integer i : a) {
                    if (b.contains(i)) {
                        res.add(i);
                    }
                }
                return res;
            }

            /**
            * Return the complement of an ArrayList
            * @param a
            * @return the complement of set
            */
            public static ArrayList<Integer> complement(ArrayList<Integer> a) {
                ArrayList<Integer> res = new ArrayList<>();
                for (int i = 0; i < MAX; i++)
                    if (!a.contains(i))
                        res.add(i);
                return res;
            }

            /**
            * Return the cardinality of an ArrayList
            * @param a
            * @return set.size() :-)
            */
            public static int cardinality(ArrayList<Integer> a) {
                return a.size();
            }

            /**
            * Return the cardinality of the union of two sets
            * @param a
            * @param b
            * @return |A| + |B| - |A∩B|
            */
            public static int cardinalityOfUnion(ArrayList<Integer> a, ArrayList<Integer> b) {
                return cardinality(union(a, b));
            }
        }

    """

    # Combine task description and inspirational code into a single prompt for solution generation
    prompt = (
        f"Based on the following task description, generate a complete and functional Java solution that meets all the requirements. "
        f"The solution should be well-structured, use meaningful variable names, include necessary comments for clarity, "
        f"and be ready to pass a comprehensive set of unit tests.\n\n"
        f"### Task Description\n\n"
        f"{task_description}\n\n"
        f"### Inspirational Code Snippet\n\n"
        f"{inspirational_code}\n\n"
        "IMPORTANT: The response must be plain Java code with no markdown formatting or ```java blocks. "
        "Ensure that each class is entirely self-contained and is not left incomplete. "
        "No part of the next file should be left in the current file. "
        "Ensure that each class is saved in its own appropriately named file, and that there are no 'leftover' initializers or class definitions from subsequent files."
        "Ensure all imports, public classes, and everything related to the class is included in the appropriate file."
        "Write NO TEXT beyond the code itself, whatsoever. "
    )

    # Call OpenAI API to generate the solution code
    response_content = generate_with_retries(client, prompt, max_retries=3)
    if response_content is None:
        print("Error: Failed to generate solution code after multiple retries.")
        sys.exit(1)

    # Ensure the .hidden_tasks directory exists
    hidden_tasks_dir = os.path.join(".hidden_tasks")
    os.makedirs(hidden_tasks_dir, exist_ok=True)

    # Write the generated code to Java files
    write_generated_code_to_files(hidden_tasks_dir, response_content)

    # Commit and push changes
    commit_and_push_changes(branch_name, hidden_tasks_dir)

def write_generated_code_to_files(directory, code_content):
    """
    Write generated Java code to appropriate files in the specified directory.
    Handles cases where leftover comments or initializations are present.
    Also ensures that import statements and public class declarations are captured.
    """
    leftover_content = ""  # To capture leftover content before the first class
    current_imports = ""   # To capture and carry over import statements
    file_blocks = re.split(r'\b(class|public\s+class|abstract\s+class|final\s+class)\b', code_content)  # Split on different class declarations

    for i in range(1, len(file_blocks), 2):  # Iterate over every class block
        class_declaration = file_blocks[i] + file_blocks[i + 1]  # Reattach split 'class' or 'public class'
        block = leftover_content + class_declaration

        # Extract class name
        class_name_match = re.search(r'class\s+([A-Za-z_]\w*)\s*{', block)  # Match 'class ClassName {'
        if class_name_match:
            class_name = class_name_match.group(1)  # Extract the class name
        else:
            print(f"Skipping block due to missing class name in block: {block[:50]}")
            continue

        # Clean up the block, removing content after the last closing brace
        cleaned_block = clean_class_block(block)

        # Ensure the necessary imports are included
        cleaned_block = check_and_add_missing_imports(cleaned_block)

        # Prepend any import statements (gathered from previous blocks)
        cleaned_block = current_imports + cleaned_block

        # Clear leftover and import content for the next file
        leftover_content = ""
        current_imports = ""

        # Write cleaned code to a file
        file_name = f"{class_name}.java"
        file_path = os.path.join(directory, file_name)

        try:
            with open(file_path, "w") as java_file:
                java_file.write(cleaned_block)
            print(f"Successfully wrote {file_name}")
        except IOError as e:
            print(f"Error writing file {file_name}: {e}")

def clean_class_block(block):
    """Ensure the block only contains content until the last closing brace."""
    
    # Find the position of the last closing brace '}' in the block
    last_closing_brace = block.rfind("}")
    
    if last_closing_brace != -1:
        # Truncate the block at the last closing brace
        block = block[:last_closing_brace + 1]
    
    return block

def check_and_add_missing_imports(block):
    """
    Check the class block for missing imports and add necessary imports based on the content.
    """
    required_imports = {
        "List": "import java.util.List;",
        "ArrayList": "import java.util.ArrayList;",
        "Map": "import java.util.Map;",
        "HashMap": "import java.util.HashMap;",
        "Scanner": "import java.util.Scanner;",
        "Set": "import java.util.Set;",
        "HashSet": "import java.util.HashSet;",
        "Random": "import java.util.Random;"
    }

    # Extract existing imports from the block
    existing_imports = re.findall(r'^\s*import .*;', block, re.MULTILINE)

    # Add missing imports
    imports_to_add = []
    for class_name, import_statement in required_imports.items():
        if class_name in block and import_statement not in existing_imports:
            imports_to_add.append(import_statement)

    # Prepend missing imports at the start of the block
    if imports_to_add:
        block = "\n".join(imports_to_add) + "\n\n" + block

    return block

def generate_with_retries(client, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating solution code: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
    return None

def commit_and_push_changes(branch_name, directory_path):
    try:
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)

        subprocess.run(["git", "add", directory_path], check=True)
        subprocess.run(["git", "commit", "-m", "Add generated solution"], check=True)
        subprocess.run(
            ["git", "push", "--set-upstream", "origin", branch_name],
            check=True,
            env=dict(os.environ, GIT_ASKPASS='echo', GIT_USERNAME='x-access-token', GIT_PASSWORD=os.getenv('GITHUB_TOKEN'))
        )
    except subprocess.CalledProcessError as e:
        print(f"Error committing and pushing changes: {e}")
        sys.exit(1)

if len(sys.argv) != 3:
    print("Error: Missing required command line arguments 'api_key' and 'branch_name'")
    sys.exit(1)

api_key = sys.argv[1]
branch_name = sys.argv[2]

main(api_key, branch_name)
