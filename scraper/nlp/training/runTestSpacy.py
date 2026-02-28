from scraper.nlp.patternsNLP import patterns
import spacy
from spacy.tokens import DocBin
from spacy.training import Example

testDocBin = DocBin().from_disk("./scraper/nlp/training/test.spacy")
docs = list(testDocBin.get_docs(spacy.blank("en").vocab))


nlp = spacy.load("./scraper/nlp/training/output/model-best")
ruler = nlp.add_pipe("entity_ruler")
ruler.add_patterns(patterns)

docs = list(testDocBin.get_docs(nlp.vocab))

# Create Example objects for evaluation
examples = []
for gold_doc in docs:
    pred_doc = nlp(gold_doc.text)
    examples.append(Example(pred_doc, gold_doc))  # predicted + gold

# Evaluate
results = nlp.evaluate(examples)


print("Performance Metrics:")
print(f"NER Precision: {results['ents_p']:.2f}")
print(f"NER Recall:    {results['ents_r']:.2f}")
print(f"NER F-score:  {results['ents_f']:.2f}")
print("Per-entity stats:", results.get("ents_per_type", {}))