from translate import get_translation, translate_list
from get_tweets import get_full_tweets, separar_en_oraciones
import spacy
from spacy.matcher import Matcher
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Función para eliminar las entidades y relaciones que estén vacías para que no aparezcan nodos separador o relaciones apuntando a un nodo vacío
def delete_empty_entities_and_relation(list_entities, list_relation):
    num = len(list_entities)
    entities = []
    relation = []
    for pos in range(num):
        if(list_entities[pos][0] != '' and list_entities[pos][1] != '' and list_relation[pos] != ''):
            entities.append(list_entities[pos])
            relation.append(list_relation[pos])
    return entities, relation

def get_entities(sent):
  ## chunk 1
  ent1 = ""
  ent2 = ""

  prv_tok_dep = ""    # dependency tag of previous token in the sentence
  prv_tok_text = ""   # previous token in the sentence

  prefix = ""
  modifier = ""

  #############################################################
  
  for tok in nlp(sent):
    ## chunk 2
    # if token is a punctuation mark then move on to the next token
    if tok.dep_ != "punct":
      # check: token is a compound word or not
      if tok.dep_ == "compound":
        prefix = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          prefix = prv_tok_text + " "+ tok.text
      
      # check: token is a modifier or not
      if tok.dep_.endswith("mod") == True:
        modifier = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          modifier = prv_tok_text + " "+ tok.text
      
      ## chunk 3
      if tok.dep_.find("subj") == True:
        ent1 = modifier +" "+ prefix + " "+ tok.text
        prefix = ""
        modifier = ""
        prv_tok_dep = ""
        prv_tok_text = ""      

      ## chunk 4
      if tok.dep_.find("obj") == True:
        ent2 = modifier +" "+ prefix +" "+ tok.text
        
      ## chunk 5  
      # update variables
      prv_tok_dep = tok.dep_
      prv_tok_text = tok.text
  #############################################################

  return [ent1.strip(), ent2.strip()]


def get_relation(sent):

	doc = nlp(sent)

	matcher = Matcher(nlp.vocab)
  	
	relation=[]
	# define the pattern
	pattern = [{'DEP': 'ROOT'},
			   {'DEP': 'prep', 'OP': "?"},
			   {'DEP': 'agent', 'OP': "?"},
			   {'POS': 'ADJ', 'OP': "?"}]

	matcher.add("matching_1", [pattern], on_match=None)

	matches = matcher(doc)

	for mathc_id, start, end in matches:
		matched_span = doc[start: end]
		# print(matched_span.text)
		relation.append(matched_span.text)
	return relation

	

tweets = get_full_tweets('Rusia', 1000)
print(len(tweets))
translated_tweets = translate_list(tweets, 'en')

nlp = spacy.load('en_core_web_sm')

entity_pairs = []
relation_pairs = []
for i in translated_tweets:
	l = separar_en_oraciones(i)
	for txt in l:
		if txt != '':
			relation_pairs.append(get_relation(txt))
			entity_pairs.append(get_entities(txt))
			
entity_pairs,relation_pairs = delete_empty_entities_and_relation(entity_pairs,relation_pairs)
            
# print('#### RELACIONES')
# pos = 0
# for i in entity_pairs:
    # print(i, ' - ', relation_pairs[pos])
    # pos = pos + 1
	
#print(pd.Series(entity_pairs).value_counts()[:2])
#print(pd.Series(relation_pairs).value_counts()[:2])

	
# extract subject
source = [i[0] for i in entity_pairs]

# # extract object
target = [i[1] for i in entity_pairs]

kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relation_pairs})

G=nx.from_pandas_edgelist(kg_df, "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())
                          
plt.figure(figsize=(12,12))

pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
plt.show()
