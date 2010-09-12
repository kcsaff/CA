
bit_count = [0]
while (len(bit_count) < 512):
    bit_count += [x + 1 for x in bit_count]
