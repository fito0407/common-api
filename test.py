import fitos.fito_util as fu
import fitos.fito_ml as fm

#print(fu.get_now_utc())
#print(fu.get_now_utc_x_days_back(30))


#df_files= fu.get_dataframe_from_jsons('test_json')
#a=df_files

good_order = ['A', 'B', 'C', 'D', 'E', 'F']
short_element_order = ['A', 'B', 'C', 'D', 'E']
extended_element_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
duplicated_element_order = ['A', 'B', 'C', 'D', 'E', 'F', 'F']

clustering_true = [['B', 'A', 'C'], ['D'], ['E', 'F']]
duplicated_clustering_true = [['B', 'A', 'C'], ['D'], ['E', 'F', 'A']]

clustering_pred = [['A', 'B'], ['C', 'D'], ['E', 'F']]
duplicated_clustering_pred = [['A', 'B', 'F'], ['C', 'D'], ['E', 'F']]


ari= fm.ari_clusterings(clustering_true, clustering_pred, good_order)
print(f"Adjusted Rand Index (vs ground truth): {ari:.3f}")