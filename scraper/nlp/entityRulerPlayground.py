import spacy
from spacy.tokens import Token
from scraper.nlp.patternsNLP import salaryPatterns, experiencePatterns

nlp = spacy.blank('en')
ruler = nlp.add_pipe('entity_ruler')
patterns = [*salaryPatterns, *experiencePatterns]
ruler.add_patterns(patterns)

text = 'The United States base range for this position is $164,448 - $234,926, plus equity. '
doc = nlp(text)
# $184,049–262,928 USD
# $203,410–290,586 USD
# $184,050- $262,928

def tokenPartOfPattern(token: Token):
    money = token.is_currency
    likeNum = token.like_num
    dash = token.text in ['—','–','-']
    return money or likeNum or dash

print(*[(t, tokenPartOfPattern(t)) for t in doc], sep='\n')
print(doc.ents)
for ent in doc.ents:
    print(ent.text, ent.label_)

