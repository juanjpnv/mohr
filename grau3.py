def segundo_grau(a, b, c):
    raiz_delta = (b**2 - 4*a*c)**.5
    x1 = (-b + raiz_delta)/(2*a)
    x2 = (-b - raiz_delta)/(2*a)

    return x1, x2


def terceiro_grau(a3, a2, a1, a0):
    """
    Retorna as raízes de uma função do tipo: a3*X^3 + a2*x^2 + a1*x + a0 = 0
    Limitações: a3 =! 0
    Utiliza-se o método de Cardano-Tartaglia: http://www.profcardy.com/cardicas/cardano.php
    """
    """Para o método de Tartaglia, a3 = 1. Então todos os termos da função são divididos por a3"""
    a2 = a2/a3
    a1 = a1/a3
    a0 = a0/a3

    """Aplicação do método de Tartaglia"""
    Q = (3*a1 - a2**2)/9
    R = (9*a1*a2 - 27*a0 - 2*a2**3)/54

    s0 = (Q**3 + R**2)
    s1 = abs(s0)**.5*(1j if s0 < 0 else 1)
    s = R + s1
    t = R - s1

    if (type(s) != complex) and (s < 0):
        S = (abs(s)) ** (1 / 3)*(-1)
    elif (type(s) != complex) and (s >= 0):
        S = (abs(s)) ** (1 / 3)
    else:
        S = s**(1 / 3)

    if (type(s) != complex) and (t < 0):
        T = (abs(t)) ** (1 / 3)*(-1)
    elif (type(s) != complex) and (t >= 0):
        T = (abs(t)) ** (1 / 3)
    else:
        T = t**(1 / 3)

    x1 = S + T - (1/3)*a2
    x2 = (-1/2)*(S+T) - (1/3)*a2 + (1/2)*(3**.5)*(S-T)*1j
    x3 = (-1/2)*(S+T) - (1/3)*a2 - (1/2)*(3**.5)*(S-T)*1j

    return x1, x2, x3


print(terceiro_grau(1, 4, 4, 1))
