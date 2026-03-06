from sklearn import metrics
import pandas as pd

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
    element_order_to_validate = sorted(element_order)

    is_valid, message_validation= _validate_for_ari_clusterings(clustering_true, clustering_pred, element_order)
    if not is_valid:
        raise ValueError(message_validation)

    labels_true = clustering_to_labels(clustering_true, element_order)
    labels_pred = clustering_to_labels(clustering_pred, element_order)
    answer = metrics.adjusted_rand_score(labels_true= labels_true, labels_pred= labels_pred)
    return answer


def _validate_for_ari_clusterings(clustering_true, clustering_pred, element_order):
    answer= True, ''

    element_order_to_validate = sorted(element_order)

    #no element in element_order can be duplicated
    grouped_elements = (pd.DataFrame({'element': element_order_to_validate})
                        .groupby('element')
                        .agg(number=('element', 'count'))
                        .reset_index())
    clusters_with_multiple = len(grouped_elements[grouped_elements['number'] > 1])
    if clusters_with_multiple >0:
        duplicates = grouped_elements[grouped_elements['number'] > 1]['element'].tolist()
        answer = False, f'element_order cannot have repeated elements. Duplicates found: {duplicates}'

    all_elements_in_clustering_true = sorted([item for sublist in clustering_true for item in sublist])
    if element_order_to_validate != all_elements_in_clustering_true:
        answer = False, f'clustering_true and element_order must have the same items'

    return answer