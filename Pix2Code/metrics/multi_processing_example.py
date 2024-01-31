import sys,os
sys.path.append("/nlp/scr/zyanzhe/Pix2Code")

from Pix2Code.metrics.visual_score import visual_eval_v3_multi
from multiprocessing import Pool
import contextlib, joblib
from joblib import Parallel, delayed
from tqdm import tqdm
import numpy as np

@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
    """Context manager to patch joblib to report into tqdm progress bar given as argument"""
    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()


def print_multi_score(multi_score):
    final_size_score, final_matched_text_score, final_position_score, final_text_color_score, final_clip_score = multi_score
    print()
    print("final_size_score", final_size_score)
    print("Matched Text Score", final_matched_text_score)
    print("Position Score", final_position_score)
    print("Text Color Score", final_text_color_score)
    print("CLIP Score", final_clip_score)
    print("--------------------------------\n")

debug = False

reference_dir = "../../testset_100"

test_dirs = {"finetune-cogagent-chat-01-28-23-02": "../../predictions_100/finetune-cogagent-chat-01-28-23-02",\
             "finetune-cogagent-chat-01-18-18-28": "../../predictions_100/finetune-cogagent-chat-01-18-18-28",\
             "finetuned_v0": "../../predictions_100/finetuned_v0"}

file_name_list = [item for item in os.listdir("../../predictions_100/finetune-cogagent-chat-01-28-23-02") if item.endswith(".html")]
# file_name_list = ["102.html"]
print(len(file_name_list))
print(file_name_list)

input_lists = []
for filename in file_name_list:
    print(filename)

    input_pred_list = [os.path.join(test_dirs[key], filename.replace(".html", ".png")) for key in test_dirs]
    original = os.path.join(reference_dir, filename.replace(".html", ".png"))

    input_list = [input_pred_list, original]
    input_lists.append(input_list)

with tqdm_joblib(tqdm(total=len(input_lists))) as progress_bar:
    return_score_lists = list(tqdm(Parallel(n_jobs=16)(delayed(visual_eval_v3_multi)(input_list, debug=debug) for input_list in input_lists), total=len(input_lists)))

res_dict = {}
for key in test_dirs:
    res_dict[key] = []

for i, filename in enumerate(file_name_list):
    print(filename)
    return_score_list = return_score_lists[i]
    idx = 0
    for key in test_dirs:
        matched, final_score, multi_score = return_score_list[idx]
        idx += 1
        current_score = [final_score] + [item for item in multi_score]
        res_dict[key].append(current_score)

for key in test_dirs:
    print(key)
    current_res = np.mean(np.array(res_dict[key]), axis=0)
    print(current_res)