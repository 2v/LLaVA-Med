import json
from data.benchmark_image_challenge.prompts import prompt_multimodal_fixed, prompt_image_only_fixed, \
    prompt_text_only_fixed


def modify_json_keys_image_challenge(file_path, output_file_path, prompt_type):
    with open(file_path, 'r') as file:
        data = json.load(file)

    modified_data = []
    for entry in data:
        new_entry = {}
        new_entry['id'] = entry['date']

        question = entry['question']
        options = list(map(lambda x: x['label'], entry['options']))

        if prompt_type == 'mm_fixed':
            formatted_question = prompt_multimodal_fixed.format(question=question, options=options)
            new_entry['image'] = entry['image_path'].split('\\')[1]
        elif prompt_type == 'image_only_fixed':
            formatted_question = prompt_image_only_fixed.format(options=options)
            new_entry['image'] = entry['image_path'].split('\\')[1]
        elif prompt_type == 'text_only_fixed':
            # we just don't add an image key for the model to not include this in context
            formatted_question = prompt_text_only_fixed.format(question=question, options=options)
        else:
            print('Please select one of: \'mm_fixed\', \'image_only_fixed\', or \'text_only_fixed\'')
            return

        new_entry['conversations'] = [
            {"from": "human", "value": formatted_question},
            {"from": "gpt", "value": str(entry['answer'])}
        ]

        modified_data.append(new_entry)

    # Write the modified data to a JSON lines file
    with open(output_file_path, 'w') as file:
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


