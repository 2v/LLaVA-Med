import json

from data.benchmark_image_challenge.prompts import prompt_multimodal_fixed_min, prompt_text_only_fixed_min, \
  prompt_image_only_fixed_min
from sklearn.model_selection import train_test_split


def modify_json_keys_image_challenge(file_path, output_file_path_train, prompt_type, train_test=False,
                                     output_file_path_test=None):
  prompt_mm = prompt_multimodal_fixed_min
  prompt_text_only = prompt_text_only_fixed_min
  prompt_image_only = prompt_image_only_fixed_min

  with open(file_path, 'r') as file:
    data = json.load(file)

  modified_data = []
  for entry in data:
    new_entry = {'id': entry['date']}

    question = entry['question']
    options = list(map(lambda x: x['label'], entry['options']))

    if prompt_type == 'mm_fixed':
      formatted_question = prompt_mm.format(question=question, options=options)
      new_entry['image'] = entry['image_path'].split('\\')[1]
    elif prompt_type == 'image_only_fixed':
      formatted_question = prompt_image_only.format(options=options)
      new_entry['image'] = entry['image_path'].split('\\')[1]
    elif prompt_type == 'text_only_fixed':
      # we just don't add an image key for the model to not include this in context
      formatted_question = prompt_text_only.format(question=question, options=options)
    else:
      print('\'prompt_type\' must be one of: \'mm_fixed\', \'image_only_fixed\', or \'text_only_fixed\'.')
      return

    new_entry['conversatons'] = [
      {"from": "human", "value": formatted_question},
      {"from": "gpt", "value": str(entry['answer'])}
    ]

    modified_data.append(new_entry)

  if train_test:
    train_data, test_data = train_test_split(modified_data, test_size=0.3, random_state=42)

    with open(output_file_path_train, 'w') as file:
      json.dump(train_data, file)
      file.write('\n')

    with open(output_file_path_test, 'w') as file:
      json.dump(test_data, file)
      file.write('\n')
  else:
    with open(output_file_path_train, 'w') as file:
      json.dump(modified_data, file)
      file.write('\n')


# generate the image challenge benchmark
modify_json_keys_image_challenge('../benchmark_image_challenge/benchmark_high_res.json',
                                 '../benchmark_image_challenge/benchmark_high_res_multimodal.json',
                                 'mm_fixed')

modify_json_keys_image_challenge('../benchmark_image_challenge/benchmark_high_res.json',
                                 '../benchmark_image_challenge/benchmark_high_res_image_only.json',
                                 'image_only_fixed')

modify_json_keys_image_challenge('../benchmark_image_challenge/benchmark_high_res.json',
                                 '../benchmark_image_challenge/benchmark_high_res_text_only.json',
                                 'text_only_fixed')

modify_json_keys_image_challenge(file_path='../benchmark_image_challenge/benchmark_high_res.json',
                                 output_file_path_train='../benchmark_image_challenge/benchmark_high_res_multimodal_train.json',
                                 output_file_path_test='../benchmark_image_challenge/benchmark_high_res_multimodal_test.json',
                                 prompt_type='text_only_fixed',
                                 train_test=True)
