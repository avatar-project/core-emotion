import pymorphy2


class Imperative():

    def __init__(self) -> None:
        self.morph = pymorphy2.MorphAnalyzer()

    def isPovel(self, sentence: str, excl: bool = False) -> bool:
        """
            На вход строка
            Если есть слово в повелительном наклонение, возвращает True
            При excl = True, вернет True, только если говорящие не включен в действие (иди, идите), при идем будет False
        """
        sentence = sentence.split()

        for word in sentence:
            if self.isWordPovel(word, excl):
                return True

        return False

    def isWordPovel(self, word: str, excl: bool = False) -> bool:
        """
            Если слово в повелительном наклонение, возвращает True
            При excl = True, вернет True, только если говорящие не включен в действие (иди, идите), при идем будет False
        """
        word_morph = self.morph.parse(word)
        for w_morph in word_morph:
            if w_morph.score >= 0.4:
                if 'impr' in w_morph.tag:
                    if excl:
                        if 'excl' in w_morph.tag:
                            return True
                        else:
                            continue

                    return True

                return False

        return False
