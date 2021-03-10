from os import sep
import re
import json
import pandas as pd
import math
import nltk
import operator
from datetime import datetime as dt
from nltk.corpus import stopwords 
nltk.download('stopwords')

eval_file = open('anserini/Eval_FourThousand.txt', 'r');
docLocations = ['anserini/collections/msmarco-passage/collection_jsonl/docs00.json','anserini/collections/msmarco-passage/collection_jsonl/docs01.json','anserini/collections/msmarco-passage/collection_jsonl/docs02.json','anserini/collections/msmarco-passage/collection_jsonl/docs03.json','anserini/collections/msmarco-passage/collection_jsonl/docs04.json','anserini/collections/msmarco-passage/collection_jsonl/docs05.json','anserini/collections/msmarco-passage/collection_jsonl/docs06.json','anserini/collections/msmarco-passage/collection_jsonl/docs07.json' ,'anserini/collections/msmarco-passage/collection_jsonl/docs08.json']
queries = 'anserini/collections/msmarco-passage/trainQueries_small_first_fourthousand.tsv'
# queries_new = open('anserini/collections/msmarco-passage/NEW_trainQueries_fourthousand_small', 'w')
resultrunLocation = 'anserini/runs/run.trainQueries_small_first_fourthousand.trec'
topDoc = 3

def main():
    print("Improving the probabilitic baseline implementation Using Blind feedback a.k.a. pseudo random feedback!")
    print(" For ease of use the location of the files and filenames are hardcoded! If there is need for change please don't forget to rename them")
    #Goal is to do Query expansion based on top document retrieved
    PsudoRelevanceFeedback()

def PsudoRelevanceFeedback() :
    c = 0
    # print("Length of array doclocations : ", len(docLocations))
    newQueriesDoc = open("QE_fourthousandQueries-New", 'w')
    start = dt.now()
    epoch = 20048/8;
    print("Starting...")
    for l in eval_file:
        if c%8==0 :
            print(c/8 +1," / ", epoch , "\t", (((c/8)+1)/epoch) *100 ,"%" )
            # print(l)
            # Now get the second item in the line -> QID
            qid = l.split(sep='\t')[1]
            # print("QID : ", qid)
            ## Get the actual query from the queries file
            queryString = getQuery(qid)
            # print(queryString)
            ## QID and Query are found, now get the top three 
            topDocs = getTopTenDocsID(qid)

            ## Now get the actual passages from of the topDocs
            topPassages = getDocs(topDocs)

            ### Query Expansion 
            # calculate tf-idf for passages
            result  = calculateTfIdf(topPassages)
            # for x in enumerate(result)
            Querynew = queryString.rstrip()
            termsToUse = 2
            if len(result)> 20:
                termsToUse = 20
            else :
                termsToUse = len(result)

            for q in range(termsToUse) : 
                Querynew += " " + str(result[q][0])

            # print(queryString)
            # print(Querynew)
            finalQuery = str(qid) + "\t"+Querynew+"\n"
            newQueriesDoc.write(finalQuery)
            end = dt.now()
            elapsed=end-start
            print("Elapsed: %02d:%02d:%02d:%02d" % (elapsed.days, elapsed.seconds // 3600, elapsed.seconds // 60 % 60, elapsed.seconds % 60))
        
        
        c +=1
        if c > 20055 : # Hard Coded ending according to Eval_file Remove later on!
            break

    newQueriesDoc.close()    
    eval_file.close()    
    print("Done!")    


def getDocs(DocsID) :
    # print(len(DocsID))
    topPassage = []
    for x in enumerate(DocsID) :
        if len(str(x[1])) < 7:
            topPassage.append(findDoc(0, x[1]))
        else :
            topPassage.append(findDoc(int(str(x[1])[0]), x[1]))
    
    return topPassage

def findDoc(index, docID) :
    # print("Doc0" + str(index)+ " for docID: ", docID)
    document = open(docLocations[index], 'r')
    text = " Some text"
    counter = 0
    for line in document :
        temp = json.loads(line)
        # counter +=1
        if int(temp["id"]) == docID:
            # print(int(temp["id"]), "\ttekst : ", temp["contents"])
            text = temp["contents"]
    document.close()
    return text

# Use qid to search in run result to find the top ten documents id
def getTopTenDocsID(qid) :
    topID = [0]*topDoc;
    counter=0
    resultrun = open(resultrunLocation, 'r')

    for line in resultrun :
        l = line.split(sep=' ');
        if int(l[0])==int(qid):
            # print(line, " -- " ,l[4])
            if int(l[3]) <= int(topDoc) :
                topID[int(l[3])-1] = int(l[2])
                # print("Found : ", line)
        # counter+=1
        # if counter>4 :
            # break
    # print("",qid, " and top docs : ", topID)
    resultrun.close()
    return topID


def getQuery(qid) :
    queryString=""
    # count =0
    queriesFile = open(queries, 'r')
    for line in queriesFile:
        # print(line)
        if line.split(sep='\t')[0] == qid:
            queryString = line.split(sep='\t')[1]
            # print("FOUND : ", queryString)
            break
        # count +=1
    queriesFile.close()
    return queryString



####################################################
############# Query Expansion ######################
####################################################

# Step 1 calculate tf-id of top doc term
# Add top 5 terms to query
# Save query to a new file (keep pid same, eventhough the query has been changed)

def calculateTfIdf(passages) :
    tokenset = []
    splitToken =[['']]*len(passages)
    ## Get rid of stopwords!
    stopWords = set(stopwords.words('english'))
    for x in range(len(passages)):
        for w in re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+",str.lower(passages[x])) :
            if w not in stopWords :
                tokenset.append(w)
                splitToken[x].append(w)
    
    tfIdf = {}
    for word in tokenset:
        wordtf = tokenset.count(word) / len(tokenset)
        wordidf = math.log(topDoc, 1+wordInDoc(splitToken, word))
        tfIdf[word] = wordtf*wordidf
    
    # print(tfIdf)
    return sorted(tfIdf.items(), key=operator.itemgetter(1) ,reverse=True)

def wordInDoc(splittokens, word) :
    count=0;
    for x in range(len(splittokens)) :
        if word in splittokens[x] :
            count+=1

    return count

if __name__ == "__main__":
    main()


