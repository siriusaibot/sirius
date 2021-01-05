from random import shuffle
from parsivar import Normalizer
from parsivar import SpellCheck
from parsivar import FindStems
from parsivar import Tokenizer
from hazm import Lemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

datelist = []
my_tokenizer = Tokenizer()
lemmatizer = Lemmatizer()
my_stemmer = FindStems()
myspell_checker = SpellCheck()
my_normalizer = Normalizer()
with open("stopwords1.txt", "r") as file:
    f = file.read()
StopWords = f.split("\n")
vectorizer = CountVectorizer()
def CleanText(InputText):
    WordsList = my_tokenizer.tokenize_words(my_normalizer.normalize(InputText))
    for i in range(len(WordsList)-1, -1, -1):
        if(WordsList[i] in StopWords):
            del WordsList[i]
            break

        WordsList[i] = lemmatizer.lemmatize(WordsList[i]).split("#")[-1]
    JoinedWords = " ".join(WordsList)
    SpellCheckedText = myspell_checker.spell_corrector(JoinedWords)
    return SpellCheckedText

sentences = []
labels = []
with open("1.txt", "r") as file:
    f = file.read()
    type1 = f.split("\n")
shuffle(type1)
for i in range(len(type1)-1, -1, -1):
    if(type1[i] == ''):
        del type1[i]
    else:
        labels.append(int(type1[i][0]))
        sentences.append(CleanText(type1[i][2:]))
sentences_train, sentences_test, y_train, y_test = train_test_split(
    sentences, labels, test_size=0.2, random_state=1000)
vectorizer.fit(sentences_train)
X_train = vectorizer.transform(sentences_train)
X_test = vectorizer.transform(sentences_test)

def LogisticClf(Input):
    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
#     print(score)
    Input = CleanText(Input)
    Input = vectorizer.transform([Input])
    return (classifier.predict(Input)[0])


def KnnClf(Input):
    from sklearn.neighbors import KNeighborsClassifier
    neigh = KNeighborsClassifier()
    neigh.fit(X_train, y_train)
    Input = CleanText(Input)
    Input = vectorizer.transform([Input])
    score = neigh.score(X_test, y_test)
#     print(score)
    return neigh.predict(Input)[0]

def RandForestClf(Input):
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(random_state=0)
    clf.fit(X_train, y_train)
    Input = CleanText(Input)
    Input = vectorizer.transform([Input])
    score = clf.score(X_test, y_test)
#     print(score)
    return clf.predict(Input)[0]


def Vote(UserInput):
    VoteList = []
    VoteList.append(LogisticClf(CleanText(UserInput)))
    VoteList.append(KnnClf(CleanText(UserInput)))
    VoteList.append(RandForestClf(CleanText(UserInput)))
    # print(VoteList)
    return max(set(VoteList), key=VoteList.count)
def Intent(UserInput):
    return Vote(CleanText(UserInput))
UserInput = str(input(": "))
Intent(UserInput)
