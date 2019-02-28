
f = open("in.txt", "r")
f_out = open("out.txt", "w")

for line in f:
    number = float(line.replace(",", "."))
    print(str(number/100).replace(".", ","), file=f_out)

f.close()
f_out.close()
