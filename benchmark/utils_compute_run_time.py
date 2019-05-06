start_lambda = 3.50
end_lambda = 3.50
lambda_delta = 0.05
requests = 25000

l = start_lambda
total_time = 0.0

while True:
    total_time += requests * (1 / l)

    l = round(l + lambda_delta, 2)
    if l > end_lambda:
        break

print("===== Stimate run time =====")
print("> start_lambda %.2f" % start_lambda)
print("> end_lambda %.2f" % end_lambda)
print("> lambda_delta %.2f" % lambda_delta)
print("> requests %d" % requests)
print()

hrs = int(total_time / 3600)
mins = int((total_time - hrs * 3600) / 60)
secs = total_time - hrs*3600 - mins*60

print("Total apprx. time %.2fs = %dh%dm%ds" % (total_time, hrs, mins, secs))
