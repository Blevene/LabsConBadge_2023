'''
Once a "winner" combination has been selected
remove the corresponding objects from the arrays in this script
This script can then be used to select a card for seeding on a user's badge!
'''
import random

def select_item(items):
  # Select one item from the array
  item = random.choice(items)
  return item

victims = [
  { "type": "victim", "value": "ngo" },
  { "type": "victim", "value": "journo" },
  { "type": "victim", "value": "wallstreet" },
  { "type": "victim", "value": "government" }
]

malware = [
  { "type": "malware", "value": "plugx" },
  { "type": "malware", "value": "hyperscrape" },
  { "type": "malware", "value": "sofacy" },
  { "type": "malware", "value": "applejeus" }
]

actors = [
  { "type": "actor", "value": "china" },
  { "type": "actor", "value": "iran" },
  { "type": "actor", "value": "north korea" },
  { "type": "actor", "value": "russia" }
]

# Select one item from each array
selected_items = [
  select_item(victims),
  select_item(malware),
  select_item(actors)
]

# Randomly select one item from the selected items
random_item = random.choice(selected_items)

print(random_item)