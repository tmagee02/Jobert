import spacy
from scraper.nlp.patternsNLP import patterns

def handleNLP(jobUrl, jobDesc, offices, remote):
    nlp = spacy.load("./scraper/nlp/training/output/model-best")
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)
    text = f'{offices} ::: {remote}  <><><><>  {jobDesc}'
    doc = nlp(text)

    labelLists = {
        'SALARY' : [],
        'EXPERIENCE' : [],
        'LOCATION' : []
    }

    print('\n', jobUrl)
    sentences = text.split("\n\n")
    for sent in sentences:
        doc = nlp(sent)
        for ent in doc.ents:
            if ent.label_ in labelLists:
                print(ent.text, ent.label_)
                labelLists[ent.label_].append(ent.text)
            else:
                print(f'possible issue: {ent.text} -> {ent.label_}')

