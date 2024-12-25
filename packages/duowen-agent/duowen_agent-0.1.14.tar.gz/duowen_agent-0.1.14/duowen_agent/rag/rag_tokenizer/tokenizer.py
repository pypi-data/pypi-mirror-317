import re
import threading
from typing import Optional, List, Dict

import nltk
from hanziconv import HanziConv
from jieba import Tokenizer
from jieba.analyse import TFIDF, TextRank
from jieba.posseg import POSTokenizer
from nltk import word_tokenize
from nltk.data import find
from nltk.stem import PorterStemmer, WordNetLemmatizer
from rake_nltk import Rake

from .stopwords import STOPWORDS


def ensure_nltk_resource(resource_name):
    try:
        # 检查资源是否存在
        find(resource_name)
    except LookupError:
        # 如果资源不存在，则下载
        print(f"Resource '{resource_name}' not found. Downloading...")
        nltk.download(resource_name.split("/")[-1])


# Punkt 分词器	tokenizers/punkt
# 停用词库	corpora/stopwords
# WordNet 词库	corpora/wordnet
# POS 标注器	taggers/averaged_perceptron_tagger

ensure_nltk_resource("tokenizers/punkt")
ensure_nltk_resource("tokenizers/punkt_tab")
ensure_nltk_resource("corpora/stopwords")
ensure_nltk_resource("corpora/wordnet")
ensure_nltk_resource("taggers/averaged_perceptron_tagger")


def is_chinese(s) -> bool:
    if "\u4e00" <= s <= "\u9fa5":
        return True
    else:
        return False


def is_number(s) -> bool:
    if "\u0030" <= s <= "\u0039":
        return True
    else:
        return False


def is_alphabet(s) -> bool:
    if ("\u0041" <= s <= "\u005a") or ("\u0061" <= s <= "\u007a"):
        return True
    else:
        return False


def full_to_half_width(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xFEE0
        if (
            inside_code < 0x0020 or inside_code > 0x7E
        ):  # 转完之后不是半角字符返回原来的字符
            rstring += uchar
        else:
            rstring += chr(inside_code)
    return rstring


def traditional_to_simplified(line):
    """繁体转简体"""
    return HanziConv.toSimplified(line)


class RagTokenizer:
    def __init__(
        self,
        min_keywords_upper_limit: int = 10,
        max_keywords_upper_limit: int = None,
        ratio: float = 0.02,
        pos_filt: List[str] = None,
    ):
        """
        :param ratio: Ratio for topK estimation based on text length.
        :param min_keywords_upper_limit: Maximum limit for topK.

        """

        self.stopwords = STOPWORDS.copy()

        self.tokenizer = Tokenizer()

        self.pos_tokenizer = POSTokenizer(self.tokenizer)

        self.tfidf = TFIDF()
        self.tfidf.stop_words = self.stopwords

        self.textrank = TextRank()
        self.textrank.tokenizer = self.pos_tokenizer
        self.textrank.stop_words = self.stopwords
        if pos_filt:
            self.textrank.pos_filt = frozenset(pos_filt)
        else:
            self.textrank.pos_filt = frozenset(
                ("n", "nz", "nr", "nrt", "ns", "nt", "v", "vn", "j", "t", "i", "l")
            )
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

        self.min_keywords_upper_limit = min_keywords_upper_limit
        self.max_keywords_upper_limit = (
            max_keywords_upper_limit if max_keywords_upper_limit else 999999999
        )
        self.ratio = ratio
        self.load_dict_status = False

    def is_load_dict_status(self):
        return self.load_dict_status

    def add_stopword(self, word: str):
        """添加停词"""
        self.stopwords.add(word)

    def add_word(self, word, frequency: int = None, pos: str = None):
        """添加词性标注"""
        self.tokenizer.add_word(word, frequency, pos)

    def del_word(self, word):
        """添加词性标注"""
        self.tokenizer.del_word(word)

    def update_word(self, word, frequency: int = None, pos: str = None):
        self.del_word(word)
        self.add_word(word, frequency, pos)

    def extract_keywords_tfidf(
        self, text: str, max_keywords_per_chunk: Optional[int] = 10, search_cut=True
    ) -> List[str]:
        keywords = self.tfidf.extract_tags(text, max_keywords_per_chunk)
        if search_cut:
            data = []
            for i in keywords:
                data.extend(self.tokenizer.lcut_for_search(i))
            return data
        else:
            return keywords

    def extract_keywords_textrank(
        self, text: str, max_keywords_per_chunk: Optional[int] = 10, search_cut=True
    ) -> List[str]:
        keywords = self.textrank.textrank(sentence=text, topK=max_keywords_per_chunk)
        if search_cut:
            data = []
            for i in keywords:
                data.extend(
                    [i for i in self.tokenizer.lcut_for_search(i) if len(i) > 1]
                )
            return data
        else:
            return keywords

    @staticmethod
    def preprocess_text(text: str) -> str:
        line = full_to_half_width(text).lower()
        line = traditional_to_simplified(line)
        return line

    def _estimate_topk_cn(self, text: str) -> int:
        effective_length = len(re.findall(r"[\u4e00-\u9fa5]", text))
        estimated_topk = int(effective_length * self.ratio)

        return max(
            self.min_keywords_upper_limit,
            min(estimated_topk, self.max_keywords_upper_limit),
        )

    def _estimate_topk_en(self, text: str) -> int:
        effective_length = len(re.findall(r"[a-zA-Z0-9]+", text))
        estimated_topk = int(effective_length * self.ratio)
        return max(
            self.min_keywords_upper_limit,
            min(estimated_topk, self.max_keywords_upper_limit),
        )

    @staticmethod
    def extract_eng(text: str) -> str:
        # 保留字母、空格、常见的标点符号（如 ' - . , ? !）
        cleaned_text = re.sub(r"[^a-zA-Z\s'\-.,?!]", " ", text)
        # 去除多余的空格
        return re.sub(r"\s+", " ", cleaned_text).strip()

    def extract_eng_keywords(self, text: str) -> List[str]:
        _r = Rake(max_length=self._estimate_topk_en(text))
        _r.extract_keywords_from_text(text)
        data = []
        for line in _r.get_ranked_phrases():
            data.append(
                "_".join(
                    [
                        self.stemmer.stem(self.lemmatizer.lemmatize(t))  # 词形转换
                        for t in word_tokenize(line)
                    ]
                )
            )
        return data

    def extract_keywords(self, text, mode="textrank", search_cut=False) -> set[str]:

        _text = self.preprocess_text(text)
        zh_num = len([1 for c in _text if is_chinese(c)])
        if zh_num == 0:
            return set(self.extract_eng_keywords(_text))

        if mode == "tfidf":
            _data = self.extract_keywords_tfidf(
                _text, self._estimate_topk_cn(_text), search_cut
            )

        elif mode == "textrank":
            _data = self.extract_keywords_textrank(
                _text, self._estimate_topk_cn(_text), search_cut
            )
        else:
            raise ValueError(f"RagTokenizer.extract_keywords Unsupported mode: {mode}")

        _en_data = self.extract_eng(_text)

        if _en_data:
            return set(_data + self.extract_eng_keywords(_en_data))
        else:
            return set(_data)

    def question_extract_keywords(self, text, search_cut=False):
        """由于用户问题可能较短 导致textrank算法无法提取关键词，采用双算法兼容模式"""
        _text = self.preprocess_text(text)
        zh_num = len([1 for c in _text if is_chinese(c)])
        if zh_num == 0:
            return set(self.extract_eng_keywords(_text))

        _tfidf_data = self.extract_keywords_tfidf(
            _text, self._estimate_topk_cn(_text), search_cut
        )

        _textrank_data = self.extract_keywords_textrank(
            _text, self._estimate_topk_cn(_text), search_cut
        )

        _en_data = self.extract_eng(_text)

        if _en_data:
            return set(
                _tfidf_data + _textrank_data + self.extract_eng_keywords(_en_data)
            )
        else:
            return set(_tfidf_data + _textrank_data)


class RagTokenizerWrapper:
    """
    建议集成流程为

    from duowen_agent.rag.rag_tokenizer import rag_tokenizers,RagTokenizer
    import threading

    app_name = 'xxx'

    lock. = threading.Lock()

    def get_tokenizer_instance(app_name):
        with lock:
            if app_name in rag_tokenizers:
                return rag_tokenizers[app_name]

            else:
                _tokenizer = RagTokenizer()

                # 完成个性化加载
                _tokenizer.add_word()

                rag_tokenizers[app_name] = _tokenizer

                return rag_tokenizers[app_name]
    """

    def __init__(self):
        self.rag_tokenizer_instance: Dict[str, RagTokenizer] = {}
        self.lock = threading.Lock()

    def __contains__(self, item: str) -> bool:
        return item in self.rag_tokenizer_instance

    def __getitem__(self, item: str):
        if item in self.rag_tokenizer_instance:
            return self.rag_tokenizer_instance[item]
        else:
            raise KeyError(f"RagTokenizerWrapper not found instance {item}")

    def __setitem__(self, key: str, value: RagTokenizer):
        if key in self.rag_tokenizer_instance:
            del self.rag_tokenizer_instance[key]
        self.rag_tokenizer_instance[key] = RagTokenizer()

    def __delitem__(self, key: str):
        if key in self.rag_tokenizer_instance:
            del self.rag_tokenizer_instance[key]


rag_tokenizers = RagTokenizerWrapper()
