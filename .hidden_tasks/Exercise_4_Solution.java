```java
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class LiteraryAnalysis {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("Exercise 4: Comparative Literary Analysis");
        System.out.println("Choose a major theme and perform the following tasks.");
        performVocabularyTask(scanner);
        constructArgument(scanner);

        scanner.close();
    }

    private static void performVocabularyTask(Scanner scanner) {
        List<String> vocabulary = new ArrayList<>();
        
        System.out.println("Enter 5 vocabulary words and their meanings:");
        for (int i = 0; i < 5; i++) {
            System.out.print("Word " + (i + 1) + ": ");
            String word = scanner.nextLine();

            System.out.print("Meaning: ");
            String meaning = scanner.nextLine();

            System.out.println("Sentence using " + word + ": ");
            String sentence = scanner.nextLine();
            
            vocabulary.add(String.format("%s: %s\nSentence: %s", word, meaning, sentence));
        }

        System.out.println("\nVocabulary Overview:");
        vocabulary.forEach(System.out::println);
    }

    private static void constructArgument(Scanner scanner) {
        System.out.println("\nConstruct an Argument");
        System.out.println("Which author presents a more compelling depiction of societal influences on personal identity, and why?");
        
        System.out.print("Thesis Statement: ");
        String thesis = scanner.nextLine();

        List<String> supportingEvidence = new ArrayList<>();
        System.out.println("\nEnter supporting evidence from each text:");
        for (int i = 0; i < 3; i++) {
            System.out.print("Evidence " + (i + 1) + ": ");
            supportingEvidence.add(scanner.nextLine());
        }
        
        System.out.print("\nConclusion: ");
        String conclusion = scanner.nextLine();

        System.out.println("\nYour Argument:");
        System.out.println("Thesis: " + thesis);
        supportingEvidence.forEach(e -> System.out.println("Evidence: " + e));
        System.out.println("Conclusion: " + conclusion);
    }
}
```