# @author jasperan
'''
This script consumes an ORDS endpoint with requests, gets the JSON data, formats it, and prepares it for
insertion into the OpenSearch cluster.
'''

import requests
import yaml
from tinydb import TinyDB, Query
import paramiko
from base64 import decodebytes
import random

def generate_random_16_digit_number():
    return int(''.join([str(random.randint(0, 9)) for _ in range(16)]))


db = TinyDB('../data/laps_db.json')
records_table = db.table('redbull')

def read_ords_endpoint(auth_data: dict):


    ords_endpoint = auth_data['ords_endpoint']

    # Consume ORDS endpoint - protected into a YAML file for security purposes
    response = requests.get(ords_endpoint)
    data = response.json()['f1sim']
    try:
        assert type(data) == type(list())
    except AssertionError:
        print('[ORDS ERROR] Endpoint not returning properly formatted data')
    return data

# after this function completes, you will get C = A - B, where
# A = all records
# B = records already inserted in previous executions of the program
# so, you will only get C = a JSON file with NEW laps.

def create_opensearch_format(data: list):
    line_writer = list()
    i = 0

    for x in data:

        # check tinydb existence of this record. if not, add it to the db.
        result = check_tinydb(x['ID'], x['LAP_TIME_DSP'])
        if result == 1:
            # this means it's new data, so we insert it too to our OpenSearch cluster.
            line_writer.append({"index": {"_index": "redbull_ords", "_id": generate_random_16_digit_number()}})
            lap_str = "racer id: {ID}, racer name: {R_NAME}, track name: {TRACKNAME}, invalid lap: {INVALID_LAP}, total lap time: {LAP_TIME_DSP}, sector 1 time: {S1}, sector 2 time: {S2}, sector 3 time: {S3}, lap date: {LAP_DATE}".format(**x).replace("\"", "")
            new_obj = {"data": lap_str}
            line_writer.append(new_obj)
            print('[NEW LAP] {}/{}'.format(i, len(data)))

        else: 
            # don't do anything if this data was already present.
            print('[DUPLICATE LAP] {}/{}'.format(i, len(data)))
        i+= 1
    return line_writer

def check_tinydb(id: str, lap_time: str):
        lap_exists = records_table.search((Query().racer_id == id) & (Query().lap_time == lap_time))
        if not lap_exists:
            records_table.insert({'racer_id': id, 'lap_time': lap_time})
            return 1
        else: return 0

def output_opensearch_file(file_path: str, line_writer: list):
    num_errors = 0
    with open(file_path, 'w', encoding="utf-8") as output_file:
        for item in line_writer:
            try:
                write_str = str(item).replace("\'", "\"")
                output_file.write("{}\n".format(write_str))
            except UnicodeEncodeError as e:
                print('[ERR] {}: {}'.format(write_str, e))
                num_errors += 1

    print('[FINISHED] TOTAL ERRORS: {}'.format(num_errors))


def send_file(auth_data: dict, source: str, destination: str):
    scp_command = """scp -i {} {} {}@{}:{}""".format(
        auth_data['key_location'],
        source,
        auth_data['user'],
        auth_data['ip_address'],
        destination
    )
    print(scp_command)

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(auth_data['ip_address'], username=auth_data['user'], key_filename=auth_data['key_location'], password='')
    
    # send the file through SFTP
    ftp_client=ssh_client.open_sftp()
    ftp_client.put(source, destination)
    ftp_client.close()

    return ssh_client


def update_cluster(auth_data: dict, ssh_client: paramiko.SSHClient):
    # this points to the private IP address of the OS cluster (not the bastion's ip address)
    # as this command will be remotely executed within the bastion
    # /redbull/ is the name of the index
    command = """curl -H 'Content-Type: application/x-ndjson' -XPOST https://10.0.3.12:9200/redbull/_bulk?pretty --data-binary @/home/opc/ords/opensearch_redbull_data.json -u {}:{} --insecure""".format(
        auth_data['cluster_private_user'],
        auth_data['cluster_private_password']
    )
    
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(command)
    print(ssh_stdout.read().decode())
    print(ssh_stderr.read().decode())



def main():
    opensearch_file_location = '../data/opensearch_redbull_data.json'
    bastion_destination_path = '/home/opc/ords/opensearch_redbull_data.json'
    with open('../auth.yaml', 'r') as file:
        auth_data = yaml.safe_load(file)

    
    # 1. Read ORDS data
    data = read_ords_endpoint(auth_data)
    # 2. Process data and convert to OpenSearch JSON format
    new_opensearch_laps = create_opensearch_format(data)
    # 3. Create resulting opensearch.json file
    output_opensearch_file(opensearch_file_location, new_opensearch_laps)
    # 4. Send this file through SFTP to the bastion
    ssh_client = send_file(auth_data, opensearch_file_location, bastion_destination_path)
    # 5. Run OpenCluster PUT command
    update_cluster(auth_data, ssh_client)

if __name__ == '__main__':
    main()

