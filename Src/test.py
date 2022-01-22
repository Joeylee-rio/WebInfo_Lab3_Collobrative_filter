id = [1,2,3]
sim = [1.85,2.33,4.6,7.8]

def func(x):
    return x-1
a = sum(sim[func(idx)] for idx in id)
print(a)

line = '10611	[10611, 17580, 9761, 105, 2390, 12425, 14366, 13746, 11739, 5035]'
line = line.strip().split('\t')
key = int(line[0])
res = []
value = line[1].strip('[')
value = value.strip(']')
value = value.strip().split(',')
for id in value:
    res.append(int(id))

