import argparse
import json
from collections import defaultdict
from pprint import pprint


class ChatEvaluation:
  # Calculate precision, recall, F1 overall and for each domain.

  @staticmethod
  def get_domain(x):
    for domain in ['chest_xray', 'mri', 'histology', 'gross', 'ct_scan']:
      in_domain = x['domain'][domain]
      if in_domain:
        return domain

  @staticmethod
  def get_avg(x):
    return sum([float(y) for y in x]) / len(x)

  @staticmethod
  def eval(samples):
    predictions = [
      (x['question_id'], x['type'], ChatEvaluation.get_domain(x), x['result'].split('\n')[0].split(' ')) for x in
      samples]
    score_type_dict = defaultdict(lambda: defaultdict(list))
    for q_id, q_type, domain, (a1_score, a2_score) in predictions:
      score_type_dict[q_type][1].append(a1_score)
      score_type_dict[q_type][2].append(a2_score)
      score_type_dict['all'][1].append(a1_score)
      score_type_dict['all'][2].append(a2_score)
      score_type_dict[domain][1].append(a1_score)
      score_type_dict[domain][2].append(a2_score)

    result = defaultdict(dict)

    for q_type, score_dict in score_type_dict.items():
      result[q_type]['gpt4_score'] = ChatEvaluation.get_avg(score_dict[1])
      result[q_type]['pred_score'] = ChatEvaluation.get_avg(score_dict[2])
      result[q_type]['pred_relative_score'] = ChatEvaluation.get_avg(
        [float(s2) / float(s1) for s1, s2 in zip(score_dict[1], score_dict[2])]) * 100
      result[q_type]['data_size'] = len(score_dict[1])
    # print results
    pprint(result)


def main(args):
  results = []
  with open(args.output_path) as f:
    for line in f:
      results.append(json.loads(line))

  # Perform Evaluation for all results
  ChatEvaluation().eval(results)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--question_input_path', type=str, default='data/eval/llava_med_eval_qa50_qa.jsonl')
  parser.add_argument('--output_path', type=str, default='data/eval/llava_med_eval_qa50_qa_ans.jsonl')
  args = parser.parse_args()
  main(args)
