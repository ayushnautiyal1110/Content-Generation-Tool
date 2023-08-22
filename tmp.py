# import speech_recognition as sr

# recognizer = sr.Recognizer()

# with sr.Microphone() as source:
#     print("Say something:")
#     audio_data = recognizer.listen(source,timeout=60)

# try:
#     text = recognizer.recognize_google(audio_data)
#     print("You said: " + text)
# except sr.UnknownValueError:
#     print("Speech Recognition could not understand audio")
# except sr.RequestError as e:
#     print(f"Could not request results from Google Speech Recognition service; {e}")
import re
from collections import Counter

def preprocess_text(text):
    # Convert text to lowercase and remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    return text

def summarize_text(text, num_sentences=3):
    # Preprocess the text
    preprocessed_text = preprocess_text(text)

    # Split the text into words
    words = preprocessed_text.split()

    # Calculate word frequency
    word_freq = Counter(words)

    # Calculate sentence scores based on word frequency
    sentence_scores = {}
    sentences = text.split('.')
    for i, sentence in enumerate(sentences):
        for word in sentence.split():
            if word in word_freq:
                if i in sentence_scores:
                    sentence_scores[i] += word_freq[word]
                else:
                    sentence_scores[i] = word_freq[word]

    # Select top sentences for summary
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    selected_sentences = sorted_sentences[:num_sentences]

    # Sort selected sentences based on original order
    selected_sentences.sort()

    # Generate the summary
    summary = ' '.join([sentences[idx] for idx, _ in selected_sentences])

    return summary

# Example text
text = """
motivation, forces acting either on or within a person to initiate behaviour. The word is derived from the Latin term motivus (“a moving cause”), which suggests the activating properties of the processes involved in psychological motivation.
Psychologists study motivational forces to help explain observed changes in behaviour that occur in an individual. Thus, for example, the observation that a person is increasingly likely to open the refrigerator door to look for food as the number of hours since the last meal increases can be understood by invoking the concept of motivation. As the above example suggests, motivation is not typically measured directly but rather inferred as the result of behavioral changes in reaction to internal or external stimuli. It is also important to understand that motivation is primarily a performance variable. That is, the effects of changes in motivation are often temporary. An individual, highly motivated to perform a particular task because of a motivational change, may later show little interest for that task as a result of further change in motivation.Motives are often categorized into primary, or basic, motives, which are unlearned and common to both animals and humans; and secondary, or learned, motives, which can differ from animal to animal and person to person. Primary motives are thought to include hunger, thirst, sex, avoidance of pain, and perhaps aggression and fear. Secondary motives typically studied in humans include achievement, power motivation, and numerous other specialized motives.Motives have also sometimes been classified into “pushes” and “pulls.” Push motives concern internal changes that have the effect of triggering specific motive states. Pull motives represent external goals that influence one’s behaviour toward them. Most motivational situations are in reality a combination of push and pull conditions. For example, hunger, in part, may be signaled by internal changes in blood glucose or fat stores, but motivation to eat is also heavily influenced by what foods are available. Some foods are more desirable than others and exert an influence on our behaviour toward them. Behaviour is, thus, often a complex blend of internal pushes and external pulls.
"""

# Summarize the text
summary = summarize_text(text)
print(summary)
