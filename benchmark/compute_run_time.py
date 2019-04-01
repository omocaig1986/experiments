start_lambda = 0.1
end_lambda = 3.80
lambda_delta = 0.05
requests = 200

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
print("Total apprx. time %.2fs = %.2fhrs" % (total_time, total_time/3600))
