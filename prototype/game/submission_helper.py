'''
This function takes the three distinct JSON objects (our cards)
concats them into a single array, and then sorts them by the value of "type"
this ensure that it should always be in order of actor, malware, victim
'''
def concatenate_arrays(array1, array2, array3):
  # Concatenate the three arrays
  combined_array = [array1, array2, array3]

  # Sort the combined array by the value of the "type" field
  sorted_array = sorted(combined_array, key=lambda x: x['type'])

  return sorted_array

# Example usage
a = {'type': 'actor', 'value': 'russia'}
b = {'type': 'victim', 'value': 'government'}
c = {'type': 'malware', 'value': 'hyperscrape'}

combined_array = concatenate_arrays(a, b, c)
print(combined_array)