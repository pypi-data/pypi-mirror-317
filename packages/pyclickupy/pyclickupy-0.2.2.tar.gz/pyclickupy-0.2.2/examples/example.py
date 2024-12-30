# import pyclickupy
# print(pyclickupy.hello())

import requests
from pyclickupy import ClickUpClient

print('executing')
API_KEY = ""
client = ClickUpClient(API_KEY)

workspaces = client.get_teams()
print('Workspaces:')
print(workspaces)

# Direct API request for goals
headers = {
    'Authorization': API_KEY,
    'Content-Type': 'application/json'
}

# Make direct GET request to ClickUp API
response = requests.get(
    f'https://api.clickup.com/api/v2/team/9011342609/goal',
    headers=headers
)

# Print raw JSON response
print('\nRaw Goals JSON:')
print(response.json())

"""
Test:
- get currennt goals
- then get assigned target and list
- then get tasks from list
- then add tasks to list
"""

# # Compare with client method result
# goals = client.get_goals('9011342609')
# print('\nClient Goals Result:')
# print(goals)

# goal = client.get_goal('55fb2be8-01dc-411d-871d-fa545e32839a')
# print('\nGoal:')
# print(goal)

# all_folders = client.get_folders('90111360926')
# print('All folders:')
# print(all_folders)


one_list = client.get_list('901108060324')
print(one_list)
