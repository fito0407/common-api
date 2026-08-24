import fitos.fito_util as fu
import fitos.fito_ml as fm

#print(fu.get_now_utc())
#print(fu.get_now_utc_x_days_back(30))


#df_files= fu.get_dataframe_from_jsons('test_json')
#a=df_files

#good_order = ['A', 'B', 'C', 'D', 'E', 'F']
#short_element_order = ['A', 'B', 'C', 'D', 'E']
#extended_element_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
#duplicated_element_order = ['A', 'B', 'C', 'D', 'E', 'F', 'F']

#clustering_true = [['B', 'A', 'C'], ['D'], ['E', 'F']]
#duplicated_clustering_true = [['B', 'A', 'C'], ['D'], ['E', 'F', 'A']]

#clustering_pred = [['A', 'B'], ['C', 'D'], ['E', 'F']]
#short_clustering_pred = [['A', 'B'], ['C', 'D'], ['E']]
#duplicated_clustering_pred = [['A', 'B', 'F'], ['C', 'D'], ['E', 'F']]


#ari= fm.ari_clusterings(clustering_true, clustering_pred, good_order)
#print(f"01. Adjusted Rand Index (vs ground truth): {ari:.3f}")

#ari= fm.ari_clusterings_replenish_pred(clustering_true, clustering_pred, good_order)
#print(f"02. Adjusted Rand Index (vs ground truth): {ari:.3f}")

#ari= fm.ari_clusterings_replenish_pred(clustering_true, short_clustering_pred, good_order)
#print(f"03. Adjusted Rand Index (vs ground truth): {ari:.3f}")

#text= "<div><p>on a mission to help businesses provide perfect customer experiences.</p>"
#cleaned_text= fu.clean_html(text)


query_embedder = fm.Query_embedder()
response_text= query_embedder.embed_text("bla")
response_query= query_embedder.embed_query("bla")

a=1