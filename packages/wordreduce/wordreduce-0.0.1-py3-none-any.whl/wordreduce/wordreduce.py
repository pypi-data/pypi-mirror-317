from collections import Counter
from dataclasses import dataclass
from functools import wraps
import pandas as pd

import numpy as np
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.tree import DecisionTreeClassifier
from typing import Any, Iterable, List, Set


from .natural_text_tokenizer import tokenize
from .util import LOGGER



class TransformerNotFittedYetError(RuntimeError):
    pass


class WordReduce:
    
    def __init__(
        self,
        max_df: int | float = 0.1,
        min_df: int | float = 3,
        vocab_size: int = 15000,
        schema_size: int = 50,
        n_components: int = 50,
        random_state=0
    ) -> None:
        self.max_df = max_df
        self.min_df = min_df
        self.vocab_size = vocab_size
        self.schema_size = schema_size
        self.random_state = random_state
        self.n_components = n_components
        self._selected_features_mask = None
        self.fitted = False

        self.vectorizer = TfidfVectorizer(
            max_df=self.max_df,
            min_df=self.min_df,
            max_features=self.vocab_size
        )
        self.reducer = NMF(
            n_components=self.n_components,
            random_state=self.random_state
        )
        self.discretizer = KBinsDiscretizer(
            n_bins=2,
            strategy="kmeans",
            encode="onehot",
            random_state=self.random_state
        )


    def transform(self, documents: Iterable[str]) -> Any:
        if not self.fitted:
            raise TransformerNotFittedYetError()
        LOGGER.info("WordReduceLabeler: transforming with WordReduce...")
        vectorized = self.vectorizer.transform(documents)
        vectorized_sel = vectorized[:, self._selected_features_mask]
        return vectorized_sel.todense()


    def fit_transform(
        self, documents: Iterable[str]
    ) -> Iterable[Iterable[str]]:
        self.fit(documents)
        return self.transform(documents)


    def fit(self, documents: Iterable[str]) -> None:
        LOGGER.info("WordReduceLabeler: fitting WordReduce...")
        self.vectorized = self.vectorizer.fit_transform(documents)
        vectorized_red = self.reducer.fit_transform(self.vectorized)
        vectorized_red_dis = self.discretizer.fit_transform(vectorized_red)

        self.vectorized_red_dis_dense = [
            tuple(vec) for vec in vectorized_red_dis.todense().tolist()
        ]
        vectorized_red_dis_dense_freq = Counter(self.vectorized_red_dis_dense)
        
        clid_by_vec = {
            _y: idx for idx, (_y, _) in 
            enumerate(vectorized_red_dis_dense_freq.most_common())
        }

        self.y = [
            clid_by_vec[vec]
            if vectorized_red_dis_dense_freq[vec] > 1
            else 0
            for vec in self.vectorized_red_dis_dense
        ]
        
        self.tree_clf = DecisionTreeClassifier(random_state=self.random_state)
        self.tree_clf.fit(self.vectorized, self.y)

        self.selector = SelectFromModel(
            self.tree_clf,
            prefit=True,
            max_features=self.schema_size
        )
        self._selected_features_mask = np.array(self.selector.get_support())
        self.fitted = True




class WordReduceLabeler(WordReduce):

    def __init__(self, *args, **kwargs):
        """
        WordReduce.fit
          WordReduce.transform
            WordReduce/WordReduceLabeler.fit        # fit labels
            WordReduce/WordReduceLabeler.transform  # transform labels
            WordReduce/WordReduceLabeler.fit_clusterize
            WordReduce/WordReduceLabeler.clusterize
        """
        super().__init__(*args, **kwargs)
        LOGGER.info("WordReduceLabeler: running `__init__` with the "
                    "following parameters: "
                    " {}".format(str(self.__dict__)))
        self.is_refitted = False
        self.selected_X = None
        
    def fit(self, documents: Iterable[str]) -> None:
        LOGGER.info("WordReduceLabeler: fitting WordReduce Labeler...")
        super().fit(documents)
        y = super().transform(documents)
        self.selected_X = (
            self.vectorized
            .todense()[:, self._selected_features_mask]
        )
        LOGGER.info("WordReduceLabeler: computed feature selection.")
        self.is_refitted = True
    
    def __get_selected_feature_names(self) -> List[str]:
        return [
            f for f, e in zip(
                self.vectorizer.get_feature_names_out(),
                self._selected_features_mask
            ) if e
        ]

    def fit_transform(
        self, documents: Iterable[str]
    ) -> Iterable[Iterable[str]]:
        self.fit(documents)
        LOGGER.info("WordReduceLabeler: transforming with "
                    "WordReduce Labeler...")
        return self.transform(documents)
    
    def transform(
        self, documents: Iterable[Iterable[str]]
    ) -> Iterable[Iterable[str]]:
        if not self.is_refitted:
            raise TransformerNotFittedYetError()
        schema = self.__get_selected_feature_names()
        transformed = []
        for x in self.selected_X.tolist():
            features = [w for w, a in zip(schema, x) if a]
            transformed.append(features)
        return transformed

    def fit_clusterize(
        self, documents: Iterable[str]
    ) -> Iterable[int]:
        transformed = self.fit_transform(documents)
        return self.clusterize(transformed)

    def clusterize(
        self, transformed: Iterable[Iterable[str]]
    ) -> Iterable[int]:
        LOGGER.info("WordReduceLabeler: clustering with "
                    "fitted WordRduce Labeler...")
        if not self.is_refitted:
            raise TransformerNotFittedYetError()
        schema = self.__get_selected_feature_names()
        return self.y.copy()

        
