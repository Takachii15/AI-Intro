
# saya mengikuti logika bapak saay quiz 2 kemarin
# tetapi karena task ini membutuhkan jumlah literals yang genap
# maka saya mengasusmsikan logikanya dapat menggunakan kebalikan dari XOR
# yaitu IFF (if and only if) atau not XOR, itulah mengapa di returnnya saya
# menggunakan (~a v ~b) yang merupakan cnf dari ~(a ^ b)

from logic import conjoin, disjoin


def evenTrue(literals):
    s = literals[0]
    s2 = literals[0]
    for i in range(len(literals[1:])):
        s = disjoin(s, literals[i+1])
        s2 = disjoin(~s, ~literals[i+1])
    return disjoin(~s, ~s2)
