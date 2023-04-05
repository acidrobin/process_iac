import os
import os.path as op

from arglu.file_type_utils import read_textgraph
from arglu.graph_processing import make_graph_from_arg_dicts, get_perspectives_dict
from arglu.plot_argument_graphs import show_graph



def main():
    all_files = [f for f in os.listdir("iac_data/textgraphs") if f.endswith(".txtgraph")]

    for f in all_files:
        nodes, relations = read_textgraph(op.join("iac_data/textgraphs", f))
        # for rel in relations:
        #     for srel in rel:
        #         if type(srel) != str:
        #             print(type(srel))
        #             import pdb; pdb.set_trace()


        print(nodes)
        print(relations)

        G = make_graph_from_arg_dicts(nodes, relations)
        show_graph(G, show_perspectives=True)




if __name__ == "__main__":

    main()