import re
#import string
import json
import os
from adaletTextCleaner import utils


class Cleaner:

    def __init__(self):

        current_dir = os.path.dirname(__file__)  # Geçerli dosyanın bulunduğu dizin

        trChar_path = os.path.join(current_dir, "resources\\trCharToReplace.json")     
        punct_path = os.path.join(current_dir, "resources\\punctuations.txt") 
        params_path = os.path.join(current_dir, "resources\\cleaningParams.txt")    
        stops_path = os.path.join(current_dir, "resources\\stopwords.txt")    
        unused_path = os.path.join(current_dir, "resources\\adaletUnusedWords.txt")                    
        common_path = os.path.join(current_dir, "resources\\adaletCommonWords.txt")  
        abbr_path = os.path.join(current_dir, "resources\\abbreviations.json")      
        allowed_path = os.path.join(current_dir, "resources\\allowedChars.txt")     


        with open(trChar_path, "r", encoding="utf-8") as file:
            self.TRCHARTOREPLACE = json.load(file)

        _, _, self.cityDistrictNames = utils.getCityDistrictNames()  

        # string.punctuations characters are : !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        #PUNCTUATIONS = string.punctuation
        with open(punct_path, "r", encoding="utf-8") as file:
            self.PUNCTUATIONS = file.read()

        with open(params_path, "r", encoding="utf-8") as file:
            partOfFile = file.read()

            charactersToKeepStart = partOfFile.find("<CHARACTERS_TO_KEEP>") + len("<CHARACTERS_TO_KEEP>")
            charactersToKeepEnd = partOfFile.find("</CHARACTERS_TO_KEEP>")
            charactersAndNumbersToKeepStart = partOfFile.find("<CHARACTERSANDNUMBERS_TO_KEEP>") + len("<CHARACTERSANDNUMBERS_TO_KEEP>")
            charactersAndNumbersToKeepEnd = partOfFile.find("</CHARACTERSANDNUMBERS_TO_KEEP>")
            specialCharactersStart = partOfFile.find("<SPECIAL_CHARACTERS>") + len("<SPECIAL_CHARACTERS>")
            specialCharactersEnd = partOfFile.find("</SPECIAL_CHARACTERS>")            

            characterTokens = partOfFile[charactersToKeepStart:charactersToKeepEnd]
            self.CHARACTERSTOKEEP = re.compile(r'[{}]'.format(characterTokens))
            characterAndNumbersTokens = partOfFile[charactersAndNumbersToKeepStart:charactersAndNumbersToKeepEnd]
            self.CHARACTERSANDNUMBERSTOKEEP = re.compile(r'[{}]'.format(characterAndNumbersTokens))
            specialCharacters = partOfFile[specialCharactersStart:specialCharactersEnd]
            self.SPECIALCHARACTERS = re.compile(r'[{}]'.format(specialCharacters))          

        with open(stops_path, "r", encoding="utf-8") as file:
            self.STOPWORDS = file.read().split("\n")  

        with open(unused_path, "r", encoding="utf-8") as file:
            self.ADALETUNUSEDWORDS = file.read().split("\n")   

        with open(common_path, "r", encoding="utf-8") as file:
            self.ADALETCOMMONWORDS = file.read().split("\n")   

        with open(abbr_path, "r", encoding="utf-8") as file:
            self.ABBREVIATIONS = json.load(file)

        with open(allowed_path, "r") as file:
            self.ALLOWEDCHARS = file.read()          


                
    def convertTRChars(self, text):

        try:
            if isinstance(text, str):
        
                # Iterate over all key-value pairs in dictionary
                for key, value in self.TRCHARTOREPLACE.items():
                    # Replace key character with value character in string
                    text = text.replace(key, value)
        except Exception as e:
            print("Error: ", e)
        
        return text
    

    def lowercase(self, text):

        try:
            if isinstance(text, str):
                text = utils.turkish_lower(text)
            text = self.cleanSpaces(text)
            
        except Exception as e:
            print("Error: ", e)

        return text


    def removeCityDistrictNames(self, text):
           
        try:
            if isinstance(text, str):
                text = utils.turkish_lower(text)
                text = ' '.join(word for word in text.split() if word not in self.cityDistrictNames)
        except Exception as e:
            print("Error: ", e)

        return text


    def removePunctuations(self, text):

        try:
            if isinstance(text, str):
                text = text.translate(str.maketrans(self.PUNCTUATIONS, ' ' * len(self.PUNCTUATIONS)))

            text = self.cleanSpaces(text)            
        except Exception as e:
            print("Error: ", e)

        return text


    def keepAlphaNumericCharacters(self, text, removeNumbers):

        try:
            if isinstance(text, str):
                if not removeNumbers:
                    pattern = re.compile(self.CHARACTERSANDNUMBERSTOKEEP)
                else:
                    pattern = re.compile(self.CHARACTERSTOKEEP)
                text = re.sub(pattern, ' ', text)
                text = self.cleanSpaces(text)                
        except Exception as e:
            print("Error: ", e)

        return text


    def removeSpecialCharacters(self, text):

        try:
            if isinstance(text, str):
                pattern = re.compile(self.SPECIALCHARACTERS)
                text = re.sub(pattern, ' ', text)
                text = self.cleanSpaces(text)
        except Exception as e:
            print("Error: ", e)

        return text


    def removeStopwords(self, text):

        try:
            if isinstance(text, str):
                text = utils.turkish_lower(text)
                text = ' '.join(word for word in text.split() if word not in self.STOPWORDS)
        except Exception as e:
            print("Error: ", e)

        return text
            

    def removeSingleCharacters(self, text):

        try:
            if isinstance(text, str):
                text = ' '.join([w for w in text.split() if len(w) > 1])
        except Exception as e:
            print("Error: ", e)

        return text


    def removeUnusedWords(self, text):

        try:
            if isinstance(text, str):
                text = utils.turkish_lower(text)
                text = ' '.join(word for word in text.split() if word not in self.ADALETUNUSEDWORDS)
        except Exception as e:
            print("Error: ", e)

        return text


    def removeCommonWords(self, text):

        try:
            if isinstance(text, str):
                text = utils.turkish_lower(text)
                encodeText, indices = utils.encodeTextToArray(text, self.ADALETCOMMONWORDS, fullTextSearch=True)
                resolvedText = text.split(' ')
                if len(resolvedText):
                    resolvedText = utils.removeElements(resolvedText, indices)
                    text = ' '.join(resolvedText)
        except Exception as e:
            print("Error: ", e)

        return text


    def removeConsecutiveConsonants(self, text):

        try:
            if isinstance(text, str):
                result = []
                for word in text.strip().split(" "):
                    if isinstance(word, str):
                        # if there are more than 3 consecutive consonants for a text
                        if len(utils.consonantConsecutiveList(word, 3)) == 0:
                            result.append(word)
                if len(result) > 0:
                    text = ' '.join(result)
        except Exception as e:
            print("Error: ", e)

        return text


    def removeConsecutiveVowels(self, text):
        try:
            if isinstance(text, str):
                result = []
                for word in text.strip().split(" "):
                    if isinstance(word, str):
                        # if there are more than 2 consecutive vowels for a text
                        if len(utils.vowelConsecutiveList(word, 2)) == 0:
                            result.append(word)
                if len(result) > 0:
                    text = ' '.join(result)
        except Exception as e:
            print("Error: ", e)

        return text


    def cleanSpaces(self, text):

        try:
            # return str(rawText).replace("\'", "").replace('"', "").replace("\t", "").replace("\n", "")
            if isinstance(text, str):
                #text = re.sub(r'\s+', ' ', text).strip()
                text = re.sub(r'\s+', ' ', text).strip()
        except Exception as e:
            print("Error: ", e)

        return text


    def replaceAbbreviations(self, text):

        try:
            if isinstance(text, str): 
                text = utils.turkish_lower(text) 
                text = self.removePunctuations(text)
                for abbr, full_form in self.ABBREVIATIONS.items():
                    text = re.sub(r'\b{}\b'.format(re.escape(abbr)), full_form, text)
                text = self.cleanSpaces(text)
            
        except Exception as e:
            print("Error: ", e)

        return text


    #: if requested allowCharacters params, then merge all unwanted punctuations and finally remove allowedchars from them
    def allowOnlySpecificCharacters(self, text, removeSpecialChars):

        try:
            if isinstance(text, str):
                charactersForReplace = self.PUNCTUATIONS
                if removeSpecialChars==True:
                    charactersForReplace += self.SPECIALCHARACTERS.pattern
                if len(self.ALLOWEDCHARS.strip()) > 0:
                    uniqueCharacters = ''.join(set(charactersForReplace) - set(self.ALLOWEDCHARS))
                else:
                    uniqueCharacters = ''.join(set(charactersForReplace))
                
                text = text.translate(str.maketrans(uniqueCharacters, ' ' * len(uniqueCharacters)))
                text = self.cleanSpaces(text)
        except Exception as e:
            print("Error: ", e)

        return text



    def text_normalizer(self, 
                        text:str,
                        removeStopwords: bool = True,
                        isResolved: bool = False,
                        removeUnused: bool = False,
                        isConvertTRChars: bool = False,
                        removeSpecialChars: bool = False,
                        isLowerCase: bool = True,
                        keepAlphaNumChars: bool = True,
                        removeNumbers: bool = True,
                        removeConsecutiveConsonants: bool = False,
                        removeConsecutiveVowels: bool = False,
                        removePunctuations: bool = True,
                        removeCityDistrictNames: bool = True,
                        isAllowOnlySpecificChars: bool = False,
                        isReplaceAbbr: bool = True  ):
        try:
            text = self.cleanSpaces(text)

            if isLowerCase:
                text = self.lowercase(text)

            if isAllowOnlySpecificChars:
                text = self.allowOnlySpecificCharacters(text, removeSpecialChars)
            else:           
                if removePunctuations:
                    text = self.removePunctuations(text)
                if removeSpecialChars:
                    text = self.removeSpecialCharacters(text)

            if isResolved:
                text = self.removeCommonWords(text)

            if removeCityDistrictNames:
                text = self.removeCityDistrictNames(text)

            if removeStopwords:
                text = self.removeStopwords(text)

            if removeUnused:
                text = self.removeUnusedWords(text)

            if isReplaceAbbr:
                text = self.replaceAbbreviations(text)

            if isConvertTRChars:
                text = self.convertTRChars(text)

            if keepAlphaNumChars:
                if removeNumbers:
                    text = self.keepAlphaNumericCharacters(text,removeNumbers)
                else:
                    text = self.keepAlphaNumericCharacters(text, not removeNumbers)

            text = self.removeSingleCharacters(text)

            if removeConsecutiveConsonants:
                text = self.removeConsecutiveConsonants(text)

            if removeConsecutiveVowels:
                text = self.removeConsecutiveVowels(text)

        except Exception as e:
            print("Error: ", e)
        

        
        return text


