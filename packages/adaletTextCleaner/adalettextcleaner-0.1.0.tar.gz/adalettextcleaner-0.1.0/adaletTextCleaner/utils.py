import re
from itertools import chain
import xml.etree.ElementTree as elemTree
import os

def encodeTextToArray(text, commonwords, fullTextSearch=False):

    encodeText = []
    indexArr = []
    if commonwords is not None:
        # encodeText = [1 if word in commonwords else 0 for word in text.split(' ')]
        for idx, word in enumerate(text.split(' ')):
            isExists = 0
            if word in commonwords:       
                isExists = 1
            else:
                for commonword in commonwords:   
                    # if commonword in word
                    if fullTextSearch:
                        if commonword in word:
                            isExists = 1
                            break
                    else:
                        # if word starting with commonword
                        pattern = f"^{commonword}"
                        if re.match(pattern, word):
                            isExists = 1
                            break
            encodeText.append(isExists)

        # assign initial values of -1
        startIdx = -1
        endIdx = -1
        # condition that array has reached at last, if exists then continue to append
        encodeText.append(-1)
        for idx, code in enumerate(encodeText):
            if code > 0:
                if startIdx == -1:
                    startIdx = idx
                endIdx = idx
            else:
                if endIdx > startIdx:
                    indexArr.append([startIdx,endIdx])
                startIdx = -1
                endIdx = -1

    return encodeText, indexArr


def removeElements(text, indices):
    # merge arrays in a list which contains only removable elements
    totalIdx = [list(range(arr[0], arr[1]+1)) for arr in indices]
    totalIdx = list(chain.from_iterable(totalIdx))
    # Reversing Indices List
    indicesList = sorted(totalIdx, reverse=True)
    # Traversing in the indices list
    for indx in indicesList:
        # checking whether the corresponding iterator index is less than the list length
        if indx < len(text):
            # removing element by index
            text.pop(indx)
    return text


def consonantConsecutiveList(word, count):
    consonant_list = re.split(r"[aeıiou]+", word, flags=re.I)
    return [y for y in consonant_list if len(y) > count]


def vowelConsecutiveList(word, count):
    consonant_list = re.split(r"[bcdfghjklmnprstvyz]+", word, flags=re.I)
    return [y for y in consonant_list if len(y) > count]


def turkish_lower(text):
    text = text.replace("T.C.", " tc ")
    text = re.sub(r'İ', 'i', text)
    text = re.sub(r'I', 'ı', text)
    text = text.lower()
    return text


def turkish_upper(text):
    text = re.sub(r'i', 'İ', text)
    text = text.upper()
    return text



#: read a xml file and parse its roots
def getCityDistrictNames():
    current_dir = os.path.dirname(__file__)  # Geçerli dosyanın bulunduğu dizin

    il_ilceler_path = os.path.join(current_dir, "resources\\il_ilceler.xml")       

    tree = elemTree.parse(il_ilceler_path)
    root = tree.getroot()

    cityNames = []
    districtNames = []
    cityDistrictNames = []

    try:
        for city in root.findall('CITY'):
            cityName = turkish_lower(str(city.attrib['cityname']))
            cityNames.append(cityName)
            for district in city.findall('DISTRICT'):
                districtName = turkish_lower(district.find('DISTNAME').text)
                if len(districtName.split('/')) > 1:
                    districtName = districtName.split('/')[0].strip()
                if len(districtName.split(' ')) > 1:
                    districtName = districtName.split(' ')[1].strip()
                districtNames.append(districtName)

                cityDistrictNames.append(cityName)
                cityDistrictNames.append(districtName)

    except Exception as e:
        print(e)

    return list(set(cityNames)), list(set(districtNames)), list(set(cityDistrictNames))

