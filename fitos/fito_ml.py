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

    #no element in element_order can be duplicated
    grouped_elements = (pd.DataFrame({'element': element_order})
                        .groupby('element')
                        .agg(number=('element', 'count'))
                        .reset_index())
    clusters_with_multiple = len(grouped_elements[grouped_elements['number'] > 1])
    if clusters_with_multiple >0:
        duplicates = grouped_elements[grouped_elements['number'] > 1]['element'].tolist()
        raise ValueError(f'element_order cannot have repeated elements. Duplicates found: {duplicates}')

    #every element in clustering_true must be in element_order
    domain = {item: False for item in element_order}
    all_elements = [item for sublist in clustering_true for item in sublist]
    elements_not_in_domain = set([item for item in all_elements if item not in domain])
    if elements_not_in_domain:
        raise ValueError(f"Found elements not in domain: {elements_not_in_domain}")

    labels_true = clustering_to_labels(clustering_true, element_order)
    labels_pred = clustering_to_labels(clustering_pred, element_order)
    answer = metrics.adjusted_rand_score(labels_true= labels_true, labels_pred= labels_pred)
    return answer