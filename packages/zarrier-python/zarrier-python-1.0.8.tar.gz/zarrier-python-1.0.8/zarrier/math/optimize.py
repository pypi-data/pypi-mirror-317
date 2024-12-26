from typing import List

def stupid_minimal(func, init_params:List, steps, *args, n=2, **kws):

    best_params = init_params.copy()
    for epoch in range(n):
        for index in range(len(init_params)):
            now_result = func(best_params)
            while True:
                now_params_1 = best_params.copy()
                now_params_2 = best_params.copy()
                now_params_1[index] += steps[index]
                now_params_2[index] -= steps[index]

                res1 = func(now_params_1)
                res2 = func(now_params_2)

                if res1 < now_result:
                    best_params = now_params_1
                    now_result = res1
                    continue

                if res2 < now_result:
                    now_result = res2
                    best_params = now_params_2
                    continue

                break
            
        print(f"epoch: {epoch}")


