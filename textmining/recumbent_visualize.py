import pandas as pd
from math import log
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import networkx as nx
import scipy

def draw_wordcloud(vocabs,name):
  save_name = '{}.png'.format(name)
  fp='C:\Windows\Fonts\Calibri.ttf'
  target = (dict(vocabs) if type(vocabs) ==list else vocabs)
  wc = WordCloud(background_color='White', width=400,height=300,font_path=fp)
  cloud = wc.generate_from_frequencies(target)
  plt.figure(figsize=(12,9))
  plt.imshow(cloud)
  plt.axis('off')
  # plt.show()
  image = plt.savefig(save_name)
  return image


def draw_network(edges,G,limit,name):
  idx_limit = limit+1
  save_name ='{}.png'.format(name)
  # 상위 100개만
  for word1,word2, weight in edges[:idx_limit]:
    G.add_edge(word1,word2,weight = float(weight))
    # edge_set.add((word1,word2))

  position = nx.spring_layout(G,k=0.09,iterations=limit)
  plt.figure(figsize=(12,9))
  nx.draw_networkx_nodes(G,position,node_size=0)
  nx.draw_networkx_edges(G,position,edgelist=edge_list[:idx_limit],
              width=weight_list[:idx_limit],edge_color='lightgray')
  nx.draw_networkx_labels(G,position,font_size=15)
  plt.axis('off')
  # plt.show()
  image = plt.savefig(save_name)
  return image


df = pd.read_csv('recumbent_fin_327.csv',header=[0])
docs = df['abstract'].tolist()

#vectorizing
vect = CountVectorizer(stop_words="english")
docs_np = np.array(docs)
#target docs에 vect적용 
DTM = vect.fit_transform(docs_np)
DTM_array = DTM.toarray()
feature_names = vect.get_feature_names()
dtm_not_tword  = vect.vocabulary_
# vect -> dataframe 
DTM_df = pd.DataFrame(DTM_array,columns = feature_names)


# dtm_not_tword  = vect.vocabulary_
target_words=["calf","ankle","knee","thight","hip",...,"blood glucose"]
# target word 새로 만들기 
new_twords = []
# target word list 빈도수 check 
twords_count =[] 
for target in target_words:
  if target in dtm_not_tword :
    pair = (target,dtm_not_tword.get(target))
    twords_count.append(pair)
    new_twords.append(target)

# 새로운 타겟 키워드 DTM 
target_DTM_df = DTM_df[new_twords]

#######워드 클라우드 그리기########

# 키워드 기준 워드클라우드
wc_tword =draw_wordcloud(twords_count,"target_wordcloud")
# 전체문서 기준 워드클라우드
wc_all = draw_wordcloud(dtm_not_tword,"alldocs_wordcloud")


#######네트워크 그래프 그리기########

edges, edge_set, G = [], set(), nx.Graph()
target_DTM = scipy.sparse.csr_matrix(target_DTM_df.values)
word_corr = np.corrcoef(target_DTM.todense(),rowvar=0)

for i in range(len(new_twords)):
  for j in range(i+1,len(new_twords)):
   edges.append((new_twords[i],new_twords[j],word_corr[i,j]))
edges = sorted(edges,key=lambda x:x[2],reverse=True)

edge_list = [(word1,word2) for word1, word2, weight in edges]
weight_list = [weight for _,_, weight in edges]

network_tword = draw_network(edges,G,100,"target_networkx")

