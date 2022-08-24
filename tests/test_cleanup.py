import json
from assessment.run import clean

def test_no_leading_and_trailing_spaces():
    with open('./data/people.json', 'r') as f:
        data = json.load(f)

        clean(data)

        boring_found = False
        for person in data:
            if len(person["Interest1"].strip()) != len(person["Interest1"]) or \
                len(person["Interest2"].strip()) != len(person["Interest2"]) or \
                len(person["Interest3"].strip()) != len(person["Interest3"]) or \
                len(person["Interest4"].strip()) != len(person["Interest4"]):
                
                boring_found = True
                break

        assert not boring_found


def test_no_uppercase():
    with open('./data/people.json', 'r') as f:
        data = json.load(f)

        clean(data)

        upper_found = False
        for i in range(1,5):
            interest_str = "Interest" + str(i)
            for person in data:
                for c in person[interest_str]:
                    if c.isupper():
                        upper_found = True
                        break

        assert not upper_found        
    