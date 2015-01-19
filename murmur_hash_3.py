def iterbytes(source):
	return [source[i:i+1] for i in range(len(source))]

def chunks(source, size=4):
	chunk = bytearray(size)
	parts = 0
	for part in source:
		number = int.from_bytes(part, byteorder='big')
		assert 0 <= number <= 255
		chunk[-parts] = number
		if parts < 3:
			parts += 1
		else:
			parts = 0
			yield chunk
	# Padd remaining bytes with zeros
	for _ in range(size - parts):
		chunk[-parts] = 0
		parts += 1
	yield chunk

def round_shift_left(value, amount):
	return (value << amount) & (value >> (128 - amount))

def murmur_hash_3(binary, seed=0xe9d158e0800eefc3):

	def mix(value):
		value ^= value >> 33
		value *= 0xff51afd7ed558ccd
		value ^= value >> 33
		value *= 0xc4ceb9fe1a85ec53
		value ^= value >> 33
		return value

	c1 = 0xff51afd7ed558ccd
	c2 = 0xc4ceb9fe1a85ec53

	h1 = seed
	h2 = seed

	for chunk in chunks(iterbytes(binary), 16):
		k1 = int.from_bytes(chunk[:2], byteorder='big')
		k1 *= c1
		k1 = round_shift_left(k1, 31)
		k1 *= c2
		k1 &= 0xffffffffffffffff

		h1 ^= k1
		h1 = round_shift_left(h1, 27)
		h1 += h2
		h1 = h1 * 5 + 0x52dce729
		h1 &= 0xffffffffffffffff

		k2 = int.from_bytes(chunk[2:], byteorder='big')
		k2 *= c2
		k2 = round_shift_left(k2, 33)
		k2 *= c1
		k2 &= 0xffffffffffffffff

		h2 ^= k2
		h2 = round_shift_left(h2, 31)
		h2 += h1
		h2 = h2 * 5 + 0x38495ab5
		h2 &= 0xffffffffffffffff

	h1 ^= len(binary)
	h2 ^= len(binary)
	h1 += h2
	h2 += h1
	h1 = mix(h1)
	h2 = mix(h2)
	h1 += h2
	h2 += h1

	result = (h1 << 8) + h2
	result &= 0xffffffffffffffff
	return result

def interactive():
	while True:
		string = input('String: ')
		binary = bytes(string, encoding='utf-8')
		print(binary)
		hashed = murmur_hash_3(binary)
		print('Hash:', '{:#x}'.format(hashed))

if __name__ == '__main__':
	interactive()
