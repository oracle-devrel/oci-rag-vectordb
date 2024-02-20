import json
from faker import Faker
import random
fake = Faker()


'''
@author jasperan
This script will generate as many fake users as we want for our RAG healthcare dataset.
This is intended to generate some synthetic data that can be embedded into a vector
store and retrieved using OCI GenAI Agents Service.
'''

number_generations = input('Please, input how many patient records you want to generate:')
number_generations = int(number_generations)

if number_generations < 0:
    number_generations = input('Please, input a positive valid integer number:')


with open('../data/janedoe.json', 'r') as file:
    data = json.load(file)
    # Generate similar objects based on data
    all_data = list()
    for _ in range(number_generations):
        patient_gender = random.choice(["male", "female"])
        fake_data = {
            "patient":{
                "name":fake.name_male() if patient_gender == "male" else fake.name_female(),
                "age":random.randint(15, 55),
                "gender":patient_gender,
                "blood_type":random.choice(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']),
                "address":fake.address(),
                "phone":fake.msisdn(),
                "last_visit": "2023-05-12",
                "passport": fake.passport_number(),
                "appointments":[
                    {
                        "doctor":"Dr. John Smith",
                        "date":"2023-03-01",
                        "time":"14:00",
                        "reason":"Annual Checkup"
                    },
                    {
                        "doctor":"Dr. John Smith",
                        "date":"2023-05-12",
                        "time":"10:30",
                        "reason":"Follow-up for knee surgery"
                    }
                ],
                "medical_records":[
                    {
                        "date":"2022-12-15",
                        "doctor":"Dr. Jane Doe",
                        "diagnosis":"Common cold",
                        "prescription":"Rest, fluids, and over-the-counter medication"
                    },
                    {
                        "date":"2022-02-11",
                        "doctor":"Dr. John Smith",
                        "diagnosis":"Knee injury",
                        "prescription":"Physical therapy and pain medication"
                    }
                ]
            }
        }
        print('[NEW] {} | {} || {} | Phone Number: {}'.format(
            fake_data['patient']['name'],
            fake_data['patient']['gender'],
            fake_data['patient']['passport'],
            fake_data['patient']['phone']
        ))
        all_data.append(fake_data)

    with open('../data/generated_data.json', 'w') as file:
        json.dump(all_data, file, indent=4)
