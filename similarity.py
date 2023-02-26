import spacy
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
from collections import defaultdict

# Load the spaCy English language model
nlp = English()

# Define a function to tokenize a string using spaCy
def tokenize(text):
    doc = nlp(text)
    return [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]

# Define a function to find similar items in a list of strings
def find_similar(text_list):
    # Create a defaultdict to store the groups
    groups = defaultdict(list)
    
    # Initialize a spaCy PhraseMatcher with a list of patterns
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp(text) for text in text_list]
    matcher.add("SIMILAR", None, *patterns)
    
    # Loop through the list of strings and find matches
    for i, text1 in enumerate(text_list):
        # Tokenize the current string
        tokens1 = tokenize(text1)
        
        # Find matches using the PhraseMatcher
        matches = matcher(nlp(text1))
        
        # Loop through the matches and group them together
        for match_id, start, end in matches:
            match_text = text_list[match_id]
            if match_text != text1:
                # Tokenize the matching string
                tokens2 = tokenize(match_text)
                
                # Calculate the similarity score between the two strings
                similarity = nlp(" ".join(tokens1)).similarity(nlp(" ".join(tokens2)))
                
                # Add the strings to the same group if they are similar enough
                if similarity > 0.5:
                    groups[i].append(match_id)
                    groups[match_id].append(i)
    
    # Convert the defaultdict to a list of sets
    return [set(group) for group in groups.values() if group]

# Test the function
text_list = ["The quick brown fox jumps over the lazy dog",
             "The brown fox jumps over the lazy dog",
             "The quick brown fox jumps over the lazy dog in the morning",
             "The slow brown dog jumps over the lazy fox",
             "The quick brown fox jumps over the lazy dog in the evening",
             "The quick brown fox jumped over the lazy dog"]
groups = find_similar(text_list)
for group in groups:
    print([text_list[i] for i in group])
