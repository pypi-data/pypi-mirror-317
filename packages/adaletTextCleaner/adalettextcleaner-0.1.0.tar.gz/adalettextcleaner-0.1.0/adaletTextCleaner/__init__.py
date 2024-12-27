from .myfunctions import Cleaner, utils


cleaning_instance = Cleaner()

cleanSpaces = cleaning_instance.cleanSpaces
lowercase = cleaning_instance.lowercase
removePunctuations = cleaning_instance.removePunctuations
removeSpecialCharacters = cleaning_instance.removeSpecialCharacters
removeCommonWords = cleaning_instance.removeCommonWords
removeCityDistrictNames = cleaning_instance.removeCityDistrictNames
removeStopwords = cleaning_instance.removeStopwords
removeUnusedWords = cleaning_instance.removeUnusedWords
convertTRChars = cleaning_instance.convertTRChars
keepAlphaNumericCharacters = cleaning_instance.keepAlphaNumericCharacters
replaceAbbreviations = cleaning_instance.replaceAbbreviations
removeSingleCharacters = cleaning_instance.removeSingleCharacters
removeConsecutiveConsonants = cleaning_instance.removeConsecutiveConsonants
removeConsecutiveVowels = cleaning_instance.removeConsecutiveVowels
allowOnlySpecificCharacters = cleaning_instance.allowOnlySpecificCharacters
text_normalizer = cleaning_instance.text_normalizer

