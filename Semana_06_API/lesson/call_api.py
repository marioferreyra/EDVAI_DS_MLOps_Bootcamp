import requests

search_api_url = 'http://127.0.0.1:8000/prediccion'

# CASO 1
data = {
    'Age': 34,
    'EmploymentType': 1,
    'GraduateOrNot': 1,
    'AnnualIncome': 500000,
    'FamilyMembers': 4,
    'ChronicDiseases': 1,
    'FrequentFlyer': 0,
    'EverTravelledAbroad': 0,
}

"""
# CASO 2
data = {
    'Age': 31,
    'EmploymentType': 0,
    'GraduateOrNot': 1,
    'AnnualIncome': 400000,
    'FamilyMembers': 6,
    'ChronicDiseases': 1,
    'FrequentFlyer': 0,
    'EverTravelledAbroad': 0,
}
"""

# response = requests.post(search_api_url, json=data)
# print(response.json())

response = requests.get('http://127.0.0.1:8000/edvai')
print(response.json())

# response = await requests.get('http://127.0.0.1:8000/edvai')
# print(response.json())
