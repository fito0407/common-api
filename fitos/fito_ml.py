from sklearn import metrics
import pandas as pd
from collections import Counter

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