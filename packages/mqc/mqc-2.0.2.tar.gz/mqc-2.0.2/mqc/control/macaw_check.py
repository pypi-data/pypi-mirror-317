import cobra
from macaw.main import run_all_tests

model = cobra.io.read_sbml_model('/home/dengxg/project/mqc/mqc/local_test_data/bigg_data/iML1515.xml')
(test_results, edge_list) = run_all_tests(model)