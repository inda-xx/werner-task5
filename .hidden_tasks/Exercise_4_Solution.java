```java
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TextAnalyzer {

    public enum SentenceType {
        DECLARATIVE, INTERROGATIVE, EXCLAMATORY, IMPERATIVE, UNKNOWN
    }

    public static class Sentence {
        private String text;
        private SentenceType type;

        public Sentence(String text, SentenceType type) {
            this.text = text;
            this.type = type;
        }

        public String getText() {
            return text;
        }

        public SentenceType getType() {
            return type;
        }
    }

    public static List<Sentence> analyzeSentences(String text) {
        List<Sentence> sentences = new ArrayList<>();
        String[] splitSentences = text.split("(?<=[.?!])\\s+");
        for (String sentenceText : splitSentences) {
            SentenceType type = determineSentenceType(sentenceText);
            sentences.add(new Sentence(sentenceText.trim(), type));
        }
        return sentences;
    }

    private static SentenceType determineSentenceType(String text) {
        if (text.endsWith("?")) {
            return SentenceType.INTERROGATIVE;
        } else if (text.endsWith("!")) {
            return SentenceType.EXCLAMATORY;
        } else if (text.matches("^\\s*[A-Z].*")) {
            return SentenceType.DECLARATIVE;
        } else {
            return SentenceType.IMPERATIVE;
        }
    }

    public static List<String> findLiteraryDevices(String text) {
        List<String> devicesFound = new ArrayList<>();
        if (text.matches(".*\\b(simile|as.*as\\b|like\\b).*")) {
            devicesFound.add("Simile");
        }
        if (text.matches(".*\\b(metaphor\\b).*")) {
            devicesFound.add("Metaphor");
        }
        if (text.matches(".*\\b(alliteration\\b|\\b[\\w]+\\b\\s+\\1\\b).*")) {
            devicesFound.add("Alliteration");
        }
        return devicesFound;
    }

    public static List<List<String>> analyzeText(String text) {
        List<Sentence> sentences = analyzeSentences(text);
        List<List<String>> result = new ArrayList<>();
        for (Sentence sentence : sentences) {
            List<String> analysis = new ArrayList<>();
            analysis.add("Sentence: " + sentence.getText());
            analysis.add("Type: " + sentence.getType().name());
            List<String> devices = findLiteraryDevices(sentence.getText());
            if (devices.isEmpty()) {
                analysis.add("Literary Devices: None");
            } else {
                analysis.add("Literary Devices: " + String.join(", ", devices));
            }
            result.add(analysis);
        }
        return result;
    }

    public static void main(String[] args) {
        String text = "The sun was as bright as a diamond! Is this a question? Yes, it is. Come here.";
        List<List<String>> analysis = analyzeText(text);
        for (List<String> sentenceAnalysis : analysis) {
            for (String entry : sentenceAnalysis) {
                System.out.println(entry);
            }
            System.out.println();
        }
    }
}
```