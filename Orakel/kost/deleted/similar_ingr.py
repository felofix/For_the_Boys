import nltk
from nltk.corpus import wordnet

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return set(synonyms)

def find_similar_ingredients(ingredient):
    similar_ingredients = []
    for syn in get_synonyms(ingredient):
        similar_ingredients.extend(get_synonyms(syn))
    return set(similar_ingredients)

recipe = ['ricotta']

for ingredient in recipe:
    similar_ingredients = list(find_similar_ingredients(ingredient.split()[-1]))
    print(similar_ingredients)
