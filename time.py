import timeit

#print(timeit.timeit("ip_calculate('ip_list.txt', 'ipv4')", setup='from CLIapp.run import ip_calculate', number=100000))

# 19.26107039101771
# 35.65866882100818 увеличение кол-ва входных данных в 2 раза
# 53.047058525000466 увеличение кол-ва входных данных в 3 раза
# 168.90080423498875 увеличение кол-ва входных данных в 10 раз

