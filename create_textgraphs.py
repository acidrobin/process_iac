import pandas as pd
import os
import os.path as op

from arglu.file_type_utils import write_textgraph


def get_comment_dict(df):
    parent_ids = list(df["parent_id"])
    title = list(df["title"])[0]
    # topic_id = [id for id in parent_ids if str(id).startswith("t")][0]


    comment_dict = dict(df[["comment_id", "comment"]].values)

    comment_dict[0] = title
    return comment_dict 



def df_to_links(df, comment_dict):
    link_codes = df[["comment_id","stance","parent_id"]].values
    main_links = [[comment_dict[x[0]], x[1] + "s", comment_dict[x[2]]] for x in link_codes]
    return main_links



def main():
    all_files = [f for f in os.listdir("iac_data/comment_threads") if f.endswith(".csv")]

    for file_name in all_files:
        
        df = pd.read_csv(op.join("iac_data/comment_threads", file_name),
                dtype = {"title":str,"topic":str,"stance":str,"comment":str,"parent_id":int,"comment_id":int,"viewpoint":str} )

        df = df.fillna("")

        out_name = file_name[:-4] + ".txtgraph"

        comment_dict = get_comment_dict(df)
        links = df_to_links(df, comment_dict)
        for rel in links:
            for srel in rel:
                if type(srel) != str:
                    print(type(srel))
                    nan_keys = [k for k,v in comment_dict.items() if type(v) != str]
                    comment_dict_vals = [v for v in comment_dict.values()]

                    import pdb; pdb.set_trace()

        
        write_textgraph(op.join("iac_data/textgraphs", out_name), links)



if __name__ == "__main__":
    main()