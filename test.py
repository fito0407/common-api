import fitos.fito_util as fu
import fitos.fito_ml as fm

#print(fu.get_now_utc())
#print(fu.get_now_utc_x_days_back(30))


#df_files= fu.get_dataframe_from_jsons('test_json')
#a=df_files

short_element_order = ['A', 'B', 'C', 'D', 'E']
extended_element_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
element_order = ['A', 'B', 'C', 'D', 'E', 'F']
duplicated_element_order = ['A', 'B', 'C', 'D', 'E', 'F', 'F']

clustering_true = [['B', 'A', 'C'], ['D'], ['E', 'F']]
clustering_pred = [['A', 'B'], ['C', 'D'], ['E', 'F']]

ari= fm.ari_clusterings(clustering_true, clustering_pred, element_order)
print(f"Adjusted Rand Index (vs ground truth): {ari:.3f}")