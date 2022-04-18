from ast import Not
import re
from matplotlib.cbook import flatten

    
class EcsStemmer:
    def __init__(self):
        self.rootWords = open("SundaRootWordVer20220216.txt", encoding = 'utf-8').read()
  
    def isRootWord(self, word):
        if re.search(" "+ word +" ", self.rootWords): return 1
        else: return 0

    def stemm(self, words):
        result = []
        for word in words:
            if self.isRootWord(word): result.append(word)
            else: result.append(self.removingProcess(word))
        return result
    
    def stem_document(self, document):
        result = []
        for line in document.split('\n'):
            result.append(self.stem_sentence(line))
        return '\n'.join(filter(None, result))
  
    def stem_sentence(self, sentence):
        result = []
        for word in sentence.split():
            result.append(self.stemmWord(word))
        return ' '.join(filter(None, result))

    def stemmWord(self, word):
        return self.stemmingProcess(word)
       
    def writeLog(self, word, base, affix):
        with open('log/log.txt', 'a+') as f:        
            f.write('{} = {} {} '.format(word, base, affix))
            f.write('\n')
      
    def prefixRemoval(self, word):
        temp = []
        if word.startswith("nyang"): 
            temp.append(word[5:])
        if word.startswith(("pang","mang", "sang", "ting")): 
            temp.append(word[4:])
        if word.startswith(("per", "nga", "nge")): 
            temp.append(word[3:])
        if word.startswith(("mi","ma","ba","sa","si","di","ka","pa","pi","ti")): 
            temp.append(word[2:])
        return temp

    def suffixRemoval(self, word):
        temp = []
        if word.endswith(("keunana","eunana","anana")): 
            temp.append(word[:-3])
        if word.endswith(("keun","ning")): 
            temp.append(word[:-4])
        if word.endswith(("eun","ing")): 
            temp.append(word[:-3])
        if word.endswith(("na","an")): 
            temp.append(word[:-2])
        return temp
    
    def allomorphNormalize(self, word):        
        if word.startswith("ng"):
            str1 = word.replace("ng","k",1)
            str2 = word.replace("ng","",1)
            return [str1, str2]
        if word.startswith("ny"):
            str1 = word.replace("ny","c",1)
            str2 = word.replace("ny","s",1)
            return [str1, str2]
        if word.startswith("m"):
            str1 = word.replace("m","b",1)
            str2 = word.replace("m","p",1)
            return [str1, str2]
        if word.startswith("n"):
            str1 = word.replace("n","t",1)
            return [str1]
        return []
    
    def InfixRemoval(self, word):
        temp = []
        #temp.append(word)
        if word.startswith("ra"): 
            temp.append(word[2:])
        if re.search(r"^(ar)[aeéiou]\S{1,}", word): 
            temp.append(word[2:])     
        if word.find("ar") != -1 and word.find("ar") > 0 and word.find("ar") < 3:
            temp.append(word.replace("ar","",1))
        if word.find("al") != -1 and word.find("al") > 0 and word.find("al") < 3:
            temp.append(word.replace("al","",1))
        if re.search(r"^(al)[aeéiou]\S{1,}", word): 
            temp.append(word[2:])
        if word.find("in") != -1 and word.find("in") > 0 and word.find("in") < 3:
            temp.append(word.replace("in","",1))
        if word.find("um") != -1 and word.find("um") > 0 and word.find("um") < 3:
            temp.append(word.replace("um","",1))
        if re.search(r"^(um)[aeéiou]\S{1,}", word): 
            temp.append(word[2:])
        return temp
    
    def reduplicationNormalize(self, word):
        if (word[0:1] == word[1:2]): 
            return word[1:] #iimahan
        if (word[0:2] == word [2:4]): 
            return word[2:] #bébéja
        if (word[0:3] == word [3:6]): 
            return word[3:] #peupeureuman
        if (word.find("ng",1,(len(word) // 2)) != -1):
            pos = word.find(("ng"))
            if (word[:pos] == word[pos+2:pos+2+pos]):
                return word[pos+2:] #beungbeurat
        if (len(word) > 5) and (word[2:4] == word [4:6]): 
            return word [0:2] + word[4:] #kunanaon
        if (len(word) > 7) and (word[2:5] == word [5:8]): 
            return word [0:2] + word[5:] #
        return []

    def prefixProcess(self, list):
        resultList = []
        for x in range(len(list)):
            if list[x].startswith(("nyang","sang","pang","ting","mang","per","nga","nge","mi","ma","ba","sa","si","di","ka","pa","pi","ti")):
                resultList.append(self.prefixRemoval(list[x]))
        return resultList

    def suffixProcess(self, list):
        resultList = []
        for x in range(len(list)):
            if list[x].endswith(("na","an","keun","eun","ning","ing")):
                resultList.append(self.suffixRemoval(list[x]))
        return resultList

    def stemmingProcess(self, word):
        if self.isRootWord(word):
            self.writeLog(word, word, "rootWord")
            return word
        else:            
            stemList = []
            stemListTemp = []
            #step 1
            if word.count('-') < 1: 
                stemWord = word                    
            else:
                if word.count('-') == 1:    
                    stemWord = word[word.find('-')+1:]                
                    if stemWord.startswith(("mu")): #asal-muasal
                        pos = word.find('-')
                        if (word[:pos] == word[pos+3:]):
                            stemWord = word[pos+3:]
                else:                        
                    if word.count('-') == 2: 
                        tempWord = word[word.find('-')+1:]
                        stemWord = tempWord[tempWord.find('-')+1:]
                    else: stemWord = word  
                
            stemListTemp.append(stemWord)
            stemList.append(stemWord)
            #step 2 suffix
            count = 1 
            while count < 4:
                stem = self.suffixProcess(stemListTemp)
                if not stem:
                    count = 10
                else:
                    stemListTemp = []
                    stemListTemp.append(stem)
                    stemListTemp = list(flatten(stemListTemp))
                    stemList.append(stemListTemp)
                    count +=1                             
            #step 3 prefix
            count = 1 
            stemListTemp = list(flatten(stemList))
            stemListTemp = list(dict.fromkeys(stemListTemp))            
            while count < 5:
                stem = self.prefixProcess(stemListTemp)
                if not stem:
                    count = 10
                else:
                    stemListTemp = []
                    stemListTemp.append(stem)
                    stemListTemp = list(flatten(stemListTemp))
                    stemList.append(stemListTemp)
                    count +=1
            #step 4 reduplication
            stemListTemp = list(flatten(stemList))
            stemListTemp = list(dict.fromkeys(stemListTemp))            
            for x in range(len(stemListTemp)):
                stem = self.reduplicationNormalize(stemListTemp[x])
                if not stem:
                    continue
                else: stemList.append(stem)            
            stemListTemp = list(flatten(stemList))
            stemListTemp = list(dict.fromkeys(stemListTemp))
            #step 5 infix
            for x in range(len(stemListTemp)):
                stem = self.InfixRemoval(stemListTemp[x])
                if not stem:
                    continue
                else: stemList.append(stem)            
            stemListTemp = list(flatten(stemList))
            stemListTemp = list(dict.fromkeys(stemListTemp))
            #step 6 allomorph
            for x in range(len(stemListTemp)):
                stem = self.allomorphNormalize(stemListTemp[x])
                if not stem:
                    continue
                else: stemList.append(stem)
            stemListTemp = list(flatten(stemList))
            stemListTemp = list(dict.fromkeys(stemListTemp))
            #step 7
            for stem in (stemListTemp):
                if self.isRootWord(stem):
                    self.writeLog(word, stem, "stemmed")
                    return stem
                    
            self.writeLog(word, word, "UNK")
            return word
                            
            
    
    
    
    

    