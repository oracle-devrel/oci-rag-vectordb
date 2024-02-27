import ujson as json

with open('../data/generated_data.json', 'r') as file:
    data = json.load(file)
    all_data = list()

    line_writer = list()
    for item in data:
        line_writer.append({"index": {}})
        extended_item = dict()
        extended_item['body'] = item
        extended_item['url'] = ''
        extended_item['title'] = ''
        line_writer.append(extended_item)
    

#{"title": "", "body": "Oracle...", "url": "https://docs.oracle.com/en-us/iaas/Content/Compute/known-issues.htm"}

with open('../data/opensearch_data.json', 'w') as output_file:
    for item in line_writer:
        write_str = str(item).replace("\'", "\"")
        output_file.write("{}\n".format(write_str))
