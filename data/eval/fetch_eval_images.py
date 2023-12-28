import json


def get_formatted_url(path):
    parts = path.split('/')

    # Replace the last part (filename) with the .tar.gz extension added to the folder name
    parts[-2] += ".tar.gz"
    new_path = '/'.join(parts[:-1])

    return link_root + new_path


def get_image_path(path):
    parts = path.split('/')
    new_path = '/'.join(parts[2:])
    return new_path


def write_to_json_lines(objects, file_name):
    with open(file_name, 'w') as file:
        for obj in objects:
            json_line = json.dumps(obj)
            file.write(json_line + '\n')


link_root = "https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/"

with open("llava_med_eval_qa50_fig_captions.json") as f:
    entries = json.load(f)

entries_list = []
for key in entries:
    entries_list.extend(entries[key])

output = []
for entry in entries_list:
    line = {}
    line['pmc_tar_url'] = get_formatted_url(entry['graphic_ref'])
    line['image_file_path'] = get_image_path(entry['graphic_ref'])
    line['pair_id'] = entry['pair_id']

    output.append(line)

file_name = '../llava_med_image_urls_eval.jsonl'

write_to_json_lines(output, file_name)


# "cd/6e/PMC2988167/LI-27-196-g003.jpg",
# "https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/cd/6e/PMC2988167.tar.gz"



