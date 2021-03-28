from owlready2 import *

import re, string
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer



# Get Ontologie Travel
def get_onto():
    onto = get_ontology("https://protege.stanford.edu/ontologies/travel.owl")
    onto.load()
    return onto

onto=get_onto()


#stop_words = set(stopwords.words('english'))
def tokenise(requet):
    token = word_tokenize(requet)
    return token


# Remove_noise from roquet
def remove_noise(tweet_tokens):
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.capitalize())
    return cleaned_tokens



# Return the Extraction of roquet
def ExtractConcept(requet):
    requet_token = remove_noise(tokenise(requet))
    concept_requet=[]
    for token in requet_token:
        for cc in onto.search(iri ="*"+token+"*"):
            if str(str(cc).split('.')[1])==token:
                concept_requet.append(cc)

    return concept_requet


# Return two concepts in roquet
def deuxConcept(requet):
    fils=[]
    concepts=ExtractConcept(requet)
    # fils concepts[0]
    if concepts[0].is_a[0]==concepts[1]:
        fils=allfils(concepts[0])
    if concepts[1].is_a[0]==concepts[0]:
        fils=allfils(concepts[1])

    return fils


# Return one Fille of node
def fils(concept,filslist):
    if len(list(concept.subclasses()))!=0:
        for c in concept.subclasses():
            filslist.append(c)
            fils(c,filslist)
    else:
        filslist.append(concept)


# Return all Fille of node
def Allfils(concepts):
    filslist=[]
    if len(concepts)!=0:
        for con in concepts:
            if len(list(con.subclasses()))!=0:
                for c in con.subclasses():
                    filslist.append(c)
                    fils(c,filslist)

    return list(set(filslist))


 # Return concept as string
def clean_con(list_con):
    l=[]
    for con in list_con:
        l.append(str(con).split('.')[1])
    return l


# Return all class of ontologie
def All_class(): 

    classall=[]
    for classe in onto.classes():
        classall.append(classe)
    #return classall
    return clean_con(classall)


#============== All cases  ==============#
def All_cases(con1, con2):
       
    # Requête composé de deux concepts ascendants 
    if con1 == con2.is_a[0]:
        return [con2]
    if con2 == con1.is_a[0]:
        return [con1]
    
    # Requête basée sur deux concepts frères 
    dd =[] # ifo of concepte
    for d in con1.disjoints():
        for de in d.entities:
            dd.append(de) 
            
    if con2 in dd:
        dd.append(con1.is_a[0])
        return list(set(dd))
    
    # Requête basée sur deux concepts  parents non ascendants et non frères
    else:
        return [con1, con2]



# All coples of concepts
def All_cople_cencepts(con):
    m = [(x, y) for x in con for y in con if x != y]

    copl_con = []
    for copl in m:
        if (copl[1],copl[0]) not in copl_con:
            copl_con.append(copl)

    return copl_con


# Return All terms_concept of All concepts
def All_terms_concept(concepts):
    terms_concept_copl = []
    copls = All_cople_cencepts(concepts)
    
    for copl in copls:
        terms_concept_copl.extend(All_cases(copl[0],copl[1]))
        
    return list(set(terms_concept_copl))



#=========================== Main Function ===========================#



def main(requet):

    terms=[]

    #stop_words = set(stopwords.words('english'))
    concepts = ExtractConcept(requet)

    for conc in concepts:
        print("\t\t ==============================")
        print("\t\t| "+str(conc)+" len : "+str(len(concepts)))
        print("\t\t ==============================")

    if len(concepts) == 1:
        terms = Allfils(concepts)
    if len(concepts) > 1:
        terms = Allfils(All_terms_concept(concepts))

    return [clean_con(concepts),clean_con(terms)]
