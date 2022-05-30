import pymorphy2
import re
from app.libs.toxic.porter_stem import Porter


class SmallTalk():

    def __init__(self) -> None:
        self.morph = pymorphy2.MorphAnalyzer()
        self.stemmer = Porter()

        self.AFFECT = re.compile(
            u"(ик|ек|к|ец|иц|оск|ечк|оньк|еньк|ышк|инш|ушк|юшк)$")

    def isAffect(self, sentence: str) -> tuple:
        """
            Передается предложение и возвращается tuple(bool, list) есть ли уменьшительно-ласткательные слова и список таких слов
        """
        words = sentence.split()
        words_affect = []
        affect = False

        for word in words:
            if self.isNoun(word):
                word_stem = self.word_stemming(word)
                word_affect = re.search(self.AFFECT, word_stem)
                if word_affect:
                    words_affect.append(word)
                    affect = True

        return affect, list(set(words_affect))

    def isNoun(self, word) -> bool:
        words_form = self.morph.parse(word)
        for word_form in words_form:
            if word_form.score >= 0.4:
                if 'NOUN' in word_form.tag:
                    return True

        return False

    def list_stemming(self, word_list: list) -> list:
        stem_list = []

        for word in word_list:
            stem_list.append(self.word_stemming(word))

        return stem_list

    def word_stemming(self, word: str) -> str:
        return self.stemmer.stem(word)
