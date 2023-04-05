from iacorpus import load_dataset
import numpy as np
import os.path as op
import pandas as pd


def get_discussions_with_stance():

    out_list = []

    dataset = load_dataset("fourforums")
    for discussion in dataset:

        idx = discussion.discussion_id
        posts = [post for post in discussion]
        id_stance_vec = [True if idx in [m.discussion_id for m in p.author.mturk_author_stances] else False for p in posts]
        has_all_stances = True if len(id_stance_vec) == sum(id_stance_vec) else False
        if has_all_stances:
            out_list.append(discussion)

    return out_list


def get_author_stance(post, discussion_id):
    all_stances = post.author.mturk_author_stances
    try:
        stance = [s for s in all_stances if s.discussion_id == discussion_id][0]
    except:
        import pdb; pdb.set_trace()
    options = ["topic_stance_votes_1", "topic_stance_votes_2"]
    most_voted_stance = max(options, key=lambda x: getattr(stance, x))
    return most_voted_stance


def convert_discussion_to_pandas(discussion):
    try:
        topic = discussion.topics[0].topic
    except:
        topic = "unknown"
    title = discussion.title
    posts = [post for post in discussion]
    discussion_id = discussion.discussion_id

    out_comments = {}

    for post in posts:
        post_viewpoint = get_author_stance(post, discussion_id)
        if not post.parent_post_id:
            stance = "support"
            parent_id = 0
        else:
            parent_id = post.parent_post_id
            try:
                parent_viewpoint = out_comments[parent_id]["viewpoint"]
            except:
                return "fail"
            if post_viewpoint != parent_viewpoint:
                stance = "attack"
            else:
                stance = "support"

        comment_dict = {"title": title,
            "topic": topic,
            "stance": stance,
            "comment": post.text,
            "parent_id": parent_id,
            "comment_id": post.post_id,
            "viewpoint": post_viewpoint            
            }

        out_comments[post.post_id] = comment_dict

    comments_list = [out_comments[k] for k in list(sorted(out_comments.keys()))]
    comments_df = pd.DataFrame(comments_list)
    return comments_df





def main():
    discussions = get_discussions_with_stance() #Only a small number of discussions have the users' stances labelled. We get those ones.

    print(len(discussions))

    fail_count = 0

    for d in discussions:
        if d.topics:
            title = d.topics[0].topic + "_" + d.title
        else:
            title = d.title
        title = title.replace("/","_")

        discussion_df = convert_discussion_to_pandas(d)
        if type(discussion_df) != str:
            discussion_df.to_csv(op.join("iac_data/comment_threads", title + ".csv"))
        else:
            fail_count += 1

    print(f"fail count: {fail_count}")
    
if __name__ == "__main__":
    main()




