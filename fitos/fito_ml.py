from sklearn import metrics

def clustering_to_labels(clustering, element_order):
    element_to_cluster = {}
    for cluster_id, cluster in enumerate(clustering):
        for element in cluster:
            element_to_cluster[element] = cluster_id
    answer = []
    for element in element_order:
        answer.append(element_to_cluster[element])

    return answer

def ari_clusterings(clustering1, clustering2, element_order):
    labels1 = clustering_to_labels(clustering1, element_order)
    labels2 = clustering_to_labels(clustering2, element_order)
    answer = metrics.adjusted_rand_score(labels1, labels2)
    return answer