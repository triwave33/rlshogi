import numpy as np

A = np.arange(9*9).reshape((9,9))

test_suite =[
    (2,2, 6,2),
    (6,3, 1,3),
    (5,2, 5,7),
    (4,7, 4,2),
    (2,4, 5,7),
    (3,5, 1,3),
    (8,4, 5,7),
    (2,6, 5,3),
    (2,6, 2,7), # 1 hop
    (4,7, 4,6), # 1hop
    (8,3, 7,3), # 1hop
    (4,6, 5,6), # 1hop
    (3,5, 4,6), # 1hop
    (8,3, 7,2), # 1hop
    (4,6, 5,5), # 1hop
    (7,3, 6,4), # 1hop
    (2,4, 4,5), ### error case
    (2,4, 9,5), ### error case
    ]

def check_obstacle(arr, rs, cs, re, ce):
    rmin = min(rs, re)
    rmax = max(rs, re)
    cmin = min(cs, ce)
    cmax = max(cs, ce)

    if rs == re:
        tmp = arr[rs, (cmin+1):cmax]
    elif cs == ce:
        tmp = arr[(rmin+1):rmax, cs]
    elif abs(ce - cs) == abs(re - rs):
        if (ce -cs) * (re - rs) > 0:
            tmp = np.diag(arr[(rmin+1):rmax, (cmin+1):cmax])
        else:
            tmp = np.diag(np.flipud(arr[(rmin+1):rmax, (cmin+1):cmax]))
    else:
        raise ValueError("Invalid move")
    return tmp

for i, (rs, cs, re, ce) in enumerate(test_suite):
    print()
    print(i)
    print(A)
    print("start")
    print(A[rs, cs])
    print("end")
    print(A[re, ce])
    print("extracted array")
    print(check_obstacle(A, rs, cs, re, ce))
