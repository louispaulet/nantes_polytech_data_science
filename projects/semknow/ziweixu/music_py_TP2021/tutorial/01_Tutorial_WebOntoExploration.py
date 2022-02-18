#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 16:59:58 2020
    
PURPOSE
    # select 1000 files frorm music corpus
    # select NPs from docs
    # use those NPs for web ontologies *master DS TP*
    
    *** music corpus
    --- select the files for 1000 regarding to length
    
    *** NPs selection for relation discovery over web knowledge
    --- recognize NPs, count NPs, clean NPs
    --- find the existence of NPs in wikipedia and use the existent format for this word
    
    *** NPs relation discovery
    --- Nps as subject to discover its hypernym
    --- Nps as object to discover its hyponym
    --- Nps as object and subject to discover thier relations
    
    
    Different from <music_v2.py>
    *** capsule into functions
    *** NO section 5
    *** topN_NPs_per_clt(LABELS, W2V_NPS, W2V_NPS_CT, TOPN_NMB): provide the top N frequent words in each cluster

@author: e16c846t
"""



from collections import Counter
import numpy as np
import pandas as pd
import spacy 
from spacy.lang.en.stop_words import STOP_WORDS #| version>2.0
import requests
from gensim.models import Word2Vec
from sklearn import cluster

# pip install SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON


path_music_code = '/Users/zoe/Desktop/codes/music_py_TP/'


###!!!---------------1. Music corpus Load ----------------------------------!!!###
df_select_doc = pd.read_csv(path_music_code +'df_select_1000doc.csv')


###!!!------------------2. NPs Selection ----------------------------------!!!###

### 2.1 recognize those NPs with all infos
nps_doc = []
nlp = spacy.load('en_core_web_sm') 

for text in df_select_doc['text']:
    np_doc = []
    doc = nlp(text) 
    for chunk in doc.noun_chunks:
        np_doc.append((chunk.text, chunk.root.text, chunk.root.dep_))
    nps_doc.append(np_doc)    
np.save(path_music_code +'nps_doc', nps_doc)
nps_doc = np.load(path_music_code +'nps_doc.npy', allow_pickle=True)

### 2.2 acquire the original NPs
source_nps_doc = []

for np_doc in nps_doc: 
    tmp = []
    for np1, root, dep in np_doc:
        tmp.append(np1)
    source_nps_doc.append(tmp)
np.save(path_music_code +'source_nps_doc', source_nps_doc)
# source_nps_doc = np.load(path_music_code +'source_nps_doc.npy', allow_pickle=True)


# 2.3 clean out stopwrds (stopwords)
source_nps_doc_v2 = []
for file in source_nps_doc:
    file_temp = []
    for nps in file:
        if nps.lower() not in STOP_WORDS:
            file_temp.append(nps)
    source_nps_doc_v2.append(file_temp)
np.save(path_music_code +'source_nps_doc_v2', source_nps_doc_v2)


###!!!------------------3. ML: feature representation of NPs  ----------------------------------!!!###
w2v_model = Word2Vec(source_nps_doc_v2, min_count=5) # Ignores all words with total frequency lower than 5.

"""
print (w2v_model.wv.similarity('album', 'soundtrack'))
# 0.9907767
print (w2v_model.wv.similarity('album', 'table'))
# 0.92826265
print (w2v_model.wv.most_similar(positive=['album'], negative=[], topn=5))
#output: [('Hell', 0.9991359710693359), ('Something', 0.9991189241409302), ('the spring', 0.9989477396011353), ('a documentary', 0.9989287853240967), ('Tracks', 0.9988466501235962)]
print (w2v_model.wv.__getitem__('album'))
# len(w2v_model.wv.__getitem__('album'))  #100
"""

w2v_feature = w2v_model.wv.vectors  #(21729, 100)  . new after stopwords (21621, 100)

kmeans = cluster.KMeans(n_clusters=10)
kmeans.fit(w2v_feature)

labels = kmeans.labels_



# find the the top-10 frequent words in each cluster

w2v_NPs = np.array(list(w2v_model.wv.vocab.keys())) # NPs 
w2v_NPs_ct = np.array([j.count for i, j in w2v_model.wv.vocab.items()]) # NPs' word count

def topN_NPs_per_clt(LABELS, W2V_NPS, W2V_NPS_CT, TOPN_NMB):
    topN_NPs_km = []
    
    for k in range(10):
        inx = np.where(LABELS == k)[0]
        
        w2v_NPs_t =  W2V_NPS[inx]      
        w2v_NPs_ct_t = W2V_NPS_CT[inx] 
        w2v_NPs_ct_dict_t = dict(zip(w2v_NPs_t, w2v_NPs_ct_t))
        
        topN_NPs_km.append(Counter(w2v_NPs_ct_dict_t).most_common()[:TOPN_NMB])
    
    return topN_NPs_km


topN_NPs_km = topN_NPs_per_clt(labels, w2v_NPs, w2v_NPs_ct, 10)
np.save(path_music_code +'topN_NPs_km', topN_NPs_km)


###!!!------------------4. NPs existence on Wiki ----------------------------------!!!###
topN_NPs = [j[0] for i in topN_NPs_km for j in i]
topN_ct = [j[1] for i in topN_NPs_km for j in i]
topN_cl = [inx_i for inx_i, i in enumerate(topN_NPs_km) for j in i]

nps_exist_text_topN = []
nps_exist_link_topN = []


### use the *openSearch* API to get the existed names
### https://www.mediawiki.org/wiki/API:Opensearch
S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"
for nps in topN_NPs:
    print(nps)
    PARAMS = {
        "action": "opensearch",
        "namespace": "0",
        "search": nps ,
        "limit": "5",
        "profile" : "fuzzy",
        "format": "json"}
    
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()  
    
    if len(DATA[1]) == 0:
        nps_exist_text_topN.append([None])
        nps_exist_link_topN.append([None])
    else:
        nps_exist_text_topN.append(DATA[1])
        nps_exist_link_topN.append(DATA[3])

df_nps_exist = pd.DataFrame()

df_nps_exist['sourceNPs_counts'] = topN_ct
df_nps_exist['sourceNPs_cluster'] = topN_cl
df_nps_exist['sourceNPs'] = topN_NPs
df_nps_exist['WikiMatchedNPs'] = [i[0] for i in nps_exist_text_topN]  # extract the top one candidates
df_nps_exist['WikiMatchedLink'] = [i[0] for i in nps_exist_link_topN]   # extract the top one candidates
df_nps_exist.to_csv(path_music_code +'df_nps_exist.csv')


###!!!------------------4. NPs and relation discovery in DBpedia by SPARQL query ----------------------------------!!!###

### 4.1 all the recognized NPs and one hypernym relation
np_query_li = ['_'.join(str(nps).split()) for nps in df_nps_exist.WikiMatchedNPs]
rel_query_li = ['<http://purl.org/linguistics/gold/hypernym>']

sparql = SPARQLWrapper("http://dbpedia.org/sparql")


### 4.2 query the OBJECT with given subject
NPs_AsSub_O = [None] * len(np_query_li)

for inx_np_query, np_query in enumerate(np_query_li):
    subj_qr = np_query
    obj_qr = np_query
    rel_qr = rel_query_li[0]
    
    NPs_AsSub_O_t = []
    
    try:     
        # query the OBJECT with given subject
        sparql.setQuery("""
                PREFIX dbp: <http://dbpedia.org/resource/>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                SELECT distinct ?y ?string where {
                   dbp:"""+subj_qr+" "+rel_qr+"""  ?y .
                   OPTIONAL {?y rdfs:label ?string . FILTER (lang(?string) = 'en') }}
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            print('______')
            print(np_query)
            print(result["string"]["value"])
            NPs_AsSub_O_t.append(result["string"]["value"])
             
    except:
        # to exclude the bad formats errors
        print(' None exist')
    
    NPs_AsSub_O[inx_np_query] = NPs_AsSub_O_t
#np.save(path_music_code +'NPs_AsSub_O', NPs_AsSub_O)

  


### 4.3 query the SUBJECT with given object
NPs_AsObj_S = [None] * len(np_query_li)

for inx_np_query, np_query in enumerate(np_query_li):
    subj_qr = np_query
    obj_qr = np_query
    rel_qr = rel_query_li[0]

    NPs_AsObj_S_t = []
    
    
    try:     
        # query the SUBJECT with given object
        sparql.setQuery("""
                PREFIX dbp: <http://dbpedia.org/resource/>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                SELECT distinct ?y ?string  where {
                   ?y """+rel_qr+""" dbp:"""+obj_qr+""".
                   OPTIONAL {?y rdfs:label ?string . FILTER (lang(?string) = 'en') }}
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            print('______')
            print(np_query)
            print(result["string"]["value"])
            NPs_AsObj_S_t.append(result["string"]["value"])
             
    except:
        # to exclude the bad formats errors
        print(' None exist')
    
    NPs_AsObj_S[inx_np_query] = NPs_AsObj_S_t    
#np.save(path_music_code +'NPs_AsObj_S', NPs_AsObj_S)
 
       

### 4.4 query the RELATIONS with given subject and object
NPs_AsSubjObj_r = []
NPs_AsSubjObj = []

for inx_np_query_S, np_query_S in enumerate(np_query_li):
    for inx_np_query_O, np_query_O in enumerate(np_query_li):
        
        NPs_AsSubjObj_r_t = []
        subj_qr = np_query_S
        obj_qr = np_query_O

        try:
            
            ### single layer relations between them
            sparql.setQuery("""
                    PREFIX dbp: <http://dbpedia.org/resource/>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    SELECT ?r where {
                       dbp:"""+subj_qr+""" ?r dbp:"""+obj_qr+""" .}
            """)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()

            if results["results"]["bindings"] != []:
                 for result in results["results"]["bindings"]:
                    print('______')
                    print(np_query)
                    print(result["r"]["value"])
                    NPs_AsSubjObj_r_t.append(result["r"]["value"])
        except:
            print('QueryBadFormed')
        
        NPs_AsSubjObj_r.append(NPs_AsSubjObj_r_t) 
        NPs_AsSubjObj.append((np_query_S, np_query_O))
      
#np.save(path_music_code +'NPs_AsSubjObj_r', NPs_AsSubjObj_r)
#np.save(path_music_code +'NPs_AsSubjObj', NPs_AsSubjObj)        
    


