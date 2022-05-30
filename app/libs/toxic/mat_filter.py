# coding=utf-8
import re


def count_mat_detect(text: str, mat_dict_path: str = "app/models/mats.txt"):
    """Модуль подсчёта матерных слов

    :param text: Текст который нужно проанализировать задаётся как str. Может быть любой длины
    :type text: str
    :return: Возвращает кортеж. В первой ячейке которого содержится количество матерных слов, во второй - процент матерных слов в текста и в третьей - множество матерных слов.
    :rtype: tuple
    """

    with open(mat_dict_path, "r", encoding="utf-8") as inp:
        mats = set(map(lambda x: x[:-1], inp.readlines()))

    words = re.sub("[\W_0-9]", " ", text.lower()).split()
    words_ammount = len(words)
    count_duck = 0
    matwords = []
    for word in words:
        if word in mats:
            count_duck += 1
            matwords.append(word)

    return (count_duck, int(count_duck / words_ammount * 100), list(set(matwords)))
