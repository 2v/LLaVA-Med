import json
import os

question_file = "data/eval/llava_med_eval_qa50_qa.jsonl"

questions = [json.loads(q) for q in open(os.path.expanduser(question_file), "r")]
#questions = get_chunk(questions, args.num_chunks, args.chunk_idx)
# answers_file = os.path.expanduser(args.answers_file)
# os.makedirs(os.path.dirname(answers_file), exist_ok=True)
# ans_file = open(answers_file, "w")

print("here")


# for i, line in enumerate(tqdm(questions)):
#     idx = line["question_id"]
