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
Your input text goes here. It can be a longer piece of text that you want to summarize into a shorter version.
Make sure to provide enough context for the summarization to be meaningful.
"""

# Summarize the text
summary = summarize_text(text)
print(summary)
