start_lambda = 1.0
end_lambda = 3.60
lambda_delta = 0.05
requests = 200
thresholds = 10

l = start_lambda
total_time = 0.0

while True:
    total_time += requests * (1 / l)

    l = round(l + lambda_delta, 2)
    if l > end_lambda:
        break
total_time *= thresholds

print("===== Stimate run time =====")
print("> start_lambda %.2f" % start_lambda)
print("> end_lambda %.2f" % end_lambda)
print("> lambda_delta %.2f" % lambda_delta)
print("> requests %d" % requests)
print()

time = total_time
day = time // (24 * 3600)
time = time % (24 * 3600)
hour = time // 3600
time %= 3600
minutes = time // 60
time %= 60
seconds = time

print("Total apprx. time %.2fs = %dd%dh%dm%ds" % (total_time, day, hour, minutes, seconds))
