import json
import re
from datetime import datetime as dt
docLocations = ['anserini/collections/msmarco-passage/collection_jsonl/docs00.json','anserini/collections/msmarco-passage/collection_jsonl/docs01.json','anserini/collections/msmarco-passage/collection_jsonl/docs02.json','anserini/collections/msmarco-passage/collection_jsonl/docs03.json','anserini/collections/msmarco-passage/collection_jsonl/docs04.json','anserini/collections/msmarco-passage/collection_jsonl/docs05.json','anserini/collections/msmarco-passage/collection_jsonl/docs06.json','anserini/collections/msmarco-passage/collection_jsonl/docs07.json' ,'anserini/collections/msmarco-passage/collection_jsonl/docs08.json']
saveLocation = ['anserini/collections/msmarco-passage/collection_jsonlCLEANED/docs00.json','anserini/collections/msmarco-passage/collection_jsonlCLEANED/docs01.json','anserini/collections/msmarco-passage/collection_jsonlCLEANED/docs02.json','anserini/collections/msmarco-passage/collection_jsonlCLEANED/docs03.json','anserini/collections/msmarco-passage/collection_jsonlCLEANED/docs04.json','anserini/collections/msmarco-passage/collection_jsonlCLEANED/docs05.json','anserini/collections/msmarco-passage/collection_jsonlCLEANED/docs06.json','anserini/collections/msmarco-passage/collection_jsonlCLEANED/docs07.json' ,'anserini/collections/msmarco-passage/collection_jsonlCLEANED/docs08.json']


def main() :
    start = dt.now()
    for x in range(len(docLocations)) :
        removeSymbols(x)
        end = dt.now()
        elapsed=end-start
        print("Finished Doc0"+str(x)+"\tElapsed: %02d:%02d:%02d:%02d" % (elapsed.days, elapsed.seconds // 3600, elapsed.seconds // 60 % 60, elapsed.seconds % 60))



def removeSymbols(ID) :
    print(docLocations[ID])
    docJSON = open(docLocations[ID], 'r')
    storeJSON = open(saveLocation[ID], 'w')
    # c=0
    for line in enumerate(docJSON):
        # print(line[1])
        temp = json.loads(line[1])
        text = re.sub(r'[^\w]', ' ', temp["contents"])
        # print(temp["id"]," : " ,text)
        newLine = '{\"id\":\t'+str(temp["id"]) + ' , \"contents\": \"'+str(text)+'\"}\n'
        # newLineJson = json.loads(newLine)
        storeJSON.write(newLine)
        # c+=1
        # if c>10:
        #     break
    docJSON.close()
    storeJSON.close()


























if __name__ == "__main__":
    main()



