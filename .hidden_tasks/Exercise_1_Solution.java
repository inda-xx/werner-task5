```java
public class SentenceStructure {

    public static void main(String[] args) {
        String sentence = "The quick brown fox jumps over the lazy dog.";
        String updatedSentence = alterPunctuation(sentence);
        System.out.println(updatedSentence);
    }

    public static String alterPunctuation(String sentence) {
        if (sentence == null || sentence.trim().isEmpty()) {
            return sentence;
        }
        
        char lastChar = sentence.charAt(sentence.length() - 1);
        if (lastChar == '.') {
            return sentence.substring(0, sentence.length() - 1) + "!";
        } else if (lastChar == '!') {
            return sentence.substring(0, sentence.length() - 1) + ".";
        } else {
            return sentence;
        }
    }
}
```