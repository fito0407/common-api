from sklearn import metrics
import pandas as pd
from collections import Counter
import threading
from fastembed import TextEmbedding
import numpy as np

def clustering_to_labels(clustering, element_order):
    element_to_cluster = {}
    for cluster_id, cluster in enumerate(clustering):
        for element in cluster:
            element_to_cluster[element] = cluster_id
    answer = []
    for element in element_order:
        answer.append(element_to_cluster[element])

    return answer

def ari_clusterings(clustering_true, clustering_pred, element_order):
    is_valid, message_validation= _validate_for_ari_clusterings(clustering_true, clustering_pred, element_order)
    if not is_valid:
        raise ValueError(message_validation)
    answer = _ari_clusterings(clustering_true, clustering_pred, element_order)
    return answer

def ari_clusterings_replenish_pred(clustering_true, clustering_pred, element_order):
    is_valid, message_validation= _validate_for_ari_clusterings(clustering_true, clustering_pred, element_order)
    if not is_valid:
        raise ValueError(message_validation)

    transformed_clustering_pred = []
    domain = {item: False for item in element_order}

    for cluster in clustering_pred:
        new_cluster = []
        for entity in cluster:
            if entity in domain:
                domain[entity]= True
                new_cluster.append(entity)
        transformed_clustering_pred.append(new_cluster)

    for key in domain:
        if not domain[key]:
            transformed_clustering_pred.append([key])

    answer = _ari_clusterings(clustering_true, transformed_clustering_pred, element_order)
    return answer

def _ari_clusterings(clustering_true, clustering_pred, element_order):
    labels_true = clustering_to_labels(clustering_true, element_order)
    labels_pred = clustering_to_labels(clustering_pred, element_order)
    answer = metrics.adjusted_rand_score(labels_true= labels_true, labels_pred= labels_pred)
    return answer

def _validate_for_ari_clusterings(clustering_true, clustering_pred, element_order):

    all_elements_in_clustering_true = sorted([item for sublist in clustering_true for item in sublist])
    all_elements_in_clustering_pred = sorted([item for sublist in clustering_pred for item in sublist])
    domain = sorted(element_order)

    is_valid, message_validation = _validate_duplicates(all_elements_in_clustering_true)
    if not is_valid:
        return is_valid, message_validation

    is_valid, message_validation = _validate_duplicates(all_elements_in_clustering_pred)
    if not is_valid:
        return is_valid, message_validation

    is_valid, message_validation= _validate_duplicates(domain)
    if not is_valid:
        return is_valid, message_validation

    if domain != all_elements_in_clustering_true:
        return False, f'clustering_true and element_order must have the same items'

    return True, ''

def _validate_duplicates(list_elements):
    counts = Counter(list_elements)
    duplicates = [item for item, count in counts.items() if count > 1]
    if duplicates:
        return False, f'Cannot have repeated elements. Duplicates found: {duplicates}'

    return True, ''

class Query_embedder():
    def __init__(self,model_name = "BAAI/bge-small-en-v1.5", dim = 384, query_instruction = "Represent this sentence for searching relevant passages: ") :
        self.model_name= model_name
        self.dim= dim
        self.query_instruction= query_instruction

        self.model = None
        self.model_lock = threading.Lock()

    def _get_model(self):
        if self.model is None:
            with self.model_lock:
                if self.model is None:
                    _model = TextEmbedding(model_name= self.model_name)
        return _model

    def _normalise(self, vec):
        # Unit-length vectors for cosine similarity (vector_cosine_ops / <=>).
        v = np.asarray(vec, dtype=np.float32)
        norm = np.linalg.norm(v)
        return v / norm if norm > 0 else v

    def embed_text(self,texts):
        # For stored documents (titles, bodies). Long bodies are truncated to the
        # model's max length by fastembed — a known v1 limitation, documented.
        model = self._get_model()
        return [self._normalise(v) for v in model.embed(list(texts))]

    def embed_query(self,text):
        # For a search query: prepend the bge query instruction, return one vector.
        model = self._get_model()
        vec = next(iter(model.embed([self.query_instruction + text])))
        return self._normalise(vec)