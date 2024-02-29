import ujson as json

with open('../data/generated_data.json', 'r') as file:
    data = json.load(file)
    all_data = list()

    i = 0
    line_writer = list()
    for item in data:
        line_writer.append({"index": {"_index": "11", "_id": i}})
        extended_item = dict()
        
        
        #extended_item['url'] = ''
        #extended_item['title'] = ''
        # we build our formatted string
        patient_str = '''name: {name}, age: {age}, gender: {gender}, blood_type: {blood_type}, address: 
        {address}, phone: {phone}, last_visit: {last_visit}, passport: {passport}'''.format(**item).replace("\"", "")

        extended_item['data'] = ', '.join("{!s}={!r}".format(key,val) for (key,val) in item.items())
        #"yesterday:{yesterday}, today:{today}, tomorrow:{tomorrow}".format(**mydict)

        #str_data = '''{"data": {}}'''.format(extended_item['data'])
        print(patient_str)
        line_writer.append({"data": "{})".format(patient_str).replace("\n", " ")})
        i += 1
    

#{"title": "", "body": "Oracle...", "url": "https://docs.oracle.com/en-us/iaas/Content/Compute/known-issues.htm"}

with open('../data/opensearch_data.json', 'w') as output_file:
    for item in line_writer:
        write_str = str(item).replace("\'", "\"")
        output_file.write("{}\n".format(write_str))
