'''
Generate a "winner" combination
This is the solution to the puzzle.
'''
import random

victims = [  { "type": "victim", "value": "ngo" },  { "type": "victim", "value": "journo" },  { "type": "victim", "value": "wallstreet" },  { "type": "victim", "value": "government" }]

malware = [  { "type": "malware", "value": "plugx" },  { "type": "malware", "value": "hyperscrape" },  { "type": "malware", "value": "sofacy" },  { "type": "malware", "value": "applejeus" }]

actors = [  { "type": "actor", "value": "china" },  { "type": "actor", "value": "iran" },  { "type": "actor", "value": "north korea" },  { "type": "actor", "value": "russia" }]

# Generate a combination of one item from each array
combination = (
  random.choice(victims),
  random.choice(malware),
  random.choice(actors)
)

print(combination)

