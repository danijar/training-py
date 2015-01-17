def dial_pad_char(number, index):
  """Get letter from telephone dial pad. Each key has up to three letters on
  it. The specific letter of those can be specified by the index."""
  assert 0 <= number <= 9
  assert 0 <= index <= 2
  if number == 0:
    return 'O'
  elif number == 1:
    return 'I'
  # Zero and one have no character on them, the remaining have three each. This
  # gives us the character at the beginning of the right key. Then add the
  # index of the current key to get overall number of the character.
  alpahbeth_index = (number - 2) * 3 + index
  assert 0 <= alpahbeth_index <= 26
  character = chr(alpahbeth_index + ord('A'))
  return character

def number_words(number_array):
  """Get list of all possible letter representations for the telephone number
  given as integer array"""
  assert isinstance(number_array, list)
  words = []
  # Iterate over all valid index combinations
  index_array = [0] * len(number_array)
  while True:
    # Add current number
    word = ''
    for number, index in zip(number_array, index_array):
      word += dial_pad_char(number, index)
    words.append(word)
    # Increment for next solution and apply carryovers
    for i in reversed(range(len(index_array))):
      index_array[i] += 1
      # Zero and one don't have multiple options, other keys have three letter
      # to choose from. If there is no overflow anymore, break of of the loop.
      if index_array[i] > 2 or number_array[i] < 2:
        # Set rest index; carryover will be applied in next iteration. If we
        # reached the first digit and still have carryover, we exhausted the
        # solution space.
        if i > 0:
          index_array[i] = 0
        else:
          return words
      else:
        break

def amount_number_words(number_array):
  """Calculate how many different letter representations the telephone number
  has"""
  amount = 1
  for number in number_array:
    assert 0 <= number <= 9
    if number > 1:
      amount *= 3
  return amount

def assert_word(number_array, word):
  """Check whether the letter representation resolves to the telephone
  number"""
  assert len(number_array) == len(word)
  for i, (number, char) in enumerate(zip(number_array, word)):
    possible_chars = {dial_pad_char(number, index) for index in range(3)}
    assert char in possible_chars

def test():
  """Test function with a random seven digit telephone number"""
  # Generate random telephone number
  import random
  number_array = [None] * 7
  for i in range(len(number_array)):
    number_array[i] = random.randint(0, 9)
  # Calculate amount of solutions and print header
  amount = amount_number_words(number_array)
  print('There are', amount, 'representations for the telephone number:',
    ''.join(map(str, number_array)))
  # Find, validate and print all representations
  words = number_words(number_array)
  assert len(words) == amount
  for word in words:
    print(word, end=' ')
    assert_word(number_array, word)
  print('')

if __name__ == '__main__':
  test()
