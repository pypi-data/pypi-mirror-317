import adaletTextCleaner as clean


def test_convertTRChars():
    text = "İstanbul güzel bir şehir"
    expected = "Istanbul guzel bir sehir"
    print(clean.convertTRChars(text))
    assert clean.convertTRChars(text) == expected

def test_lowercase(): 
    text = "T.C. KÜÇÜK HARFLERE ÇEVİR"
    expected = "tc küçük harflere çevir"
    print(clean.lowercase(text))
    assert clean.lowercase(text) == expected

def test_removeCityDistrictNames():

    text = "İstanbul Kadıköy güzel bir yer"
    expected = "güzel bir yer"
    print(clean.removeCityDistrictNames(text))
    assert clean.removeCityDistrictNames(text) == expected

def test_removePunctuations():    

    text = "Merhaba, dünya! Nasıl?"
    expected = "Merhaba dünya Nasıl"
    print(clean.removePunctuations(text))
    assert clean.removePunctuations(text) == expected

def test_keepAlphaNumericCharacters():  
    text = "abc&%123 xyz"
    expected = "abc xyz"
    print(clean.keepAlphaNumericCharacters(text, False))
    print(clean.keepAlphaNumericCharacters(text, True))
    assert clean.keepAlphaNumericCharacters(text, removeNumbers=False) == "abc 123 xyz"
    assert clean.keepAlphaNumericCharacters(text, True) == expected

def test_removeSpecialCharacters():  
 
    text = "«test»—data”"
    expected = "test data"
    print(clean.removeSpecialCharacters(text))
    assert clean.removeSpecialCharacters(text) == expected

def test_removeStopwords():

    text = "Bu test   cümlesi ile deneme"
    expected = "test cümlesi deneme"
    print(clean.removeStopwords(text))
    assert clean.removeStopwords(text) == expected

def test_removeSingleCharacters():
    text = "a test cümlesi b c d"
    expected = "test cümlesi"
    print(clean.removeSingleCharacters(text))
    assert clean.removeSingleCharacters(text) == expected

def test_removeUnusedWords():

    text = "imzalıdır bu örnek bir metindir"
    expected = "bu örnek bir metindir"
    print(clean.removeUnusedWords(text))
    assert clean.removeUnusedWords(text) == expected

def test_removeCommonWords():

    text = "Bu Ticaret hukuk test"
    expected = "bu test"
    print(clean.removeCommonWords(text))
    assert clean.removeCommonWords(text) == expected

def test_removeConsecutiveConsonants():
    text = "bcdc kfg güzel"
    expected = "kfg güzel"
    print(clean.removeConsecutiveConsonants(text))
    assert clean.removeConsecutiveConsonants(text) == expected

def test_removeConsecutiveVowels():
    text = "aai aa güzel"
    expected = "aa güzel"
    print(clean.removeConsecutiveVowels(text))
    assert clean.removeConsecutiveVowels(text) == expected

def test_cleanSpaces():
    text = "  Bu  bir    test.  "
    expected = "Bu bir test."
    print(clean.cleanSpaces(text))
    assert clean.cleanSpaces(text) == expected

def test_replaceAbbreviations(): 

    text = "Av. Ahmet ve inş"
    expected = "avukat ahmet ve inşaat"
    print(clean.replaceAbbreviations(text))
    assert clean.replaceAbbreviations(text) == expected

def test_allowOnlySpecificCharacters():  
    
    text = "—abc@!10 x.yz"
    expected = "—abc 10 x.yz"
    expected2 = "abc 10 x.yz"    
    print(clean.allowOnlySpecificCharacters(text, False))
    print(clean.allowOnlySpecificCharacters(text, True))
    assert clean.allowOnlySpecificCharacters(text, removeSpecialChars=False) == expected
    assert clean.allowOnlySpecificCharacters(text, removeSpecialChars=True) == expected2

def test_text_normalizer():

    text = "T.C. Av. Mehmet Kadıköy'den10 İstanbul'a geçti."
    expected = "tc avukat mehmet den geçti"
    print(clean.text_normalizer(text))
    assert clean.text_normalizer(text) == expected

if __name__ == "__main__":

    test_convertTRChars()
    test_lowercase()
    test_removeCityDistrictNames()
    test_removePunctuations()
    test_keepAlphaNumericCharacters()
    test_removeSpecialCharacters()
    test_removeStopwords()
    test_removeSingleCharacters()
    test_removeUnusedWords()
    test_removeCommonWords()
    test_removeConsecutiveConsonants()
    test_removeConsecutiveVowels()
    test_cleanSpaces()
    test_replaceAbbreviations()
    test_allowOnlySpecificCharacters()
    test_text_normalizer()
