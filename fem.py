import numpy
import numpy.linalg
import matplotlib.pyplot


def k(x):
    if x < 1:
        return 1
    else:
        return 2


def fem(u0, g1, n, f):
    h = 2.0 / n
    #górna przekątna
    d1 = lambda x: -1 / h + 1 / 2 * k(x)
    #główna przekątna
    d2 = 2 / h
    #dolna przekątna
    d3 = lambda x: -1 / h - 1 / 2 * k(x)
    # wstępnie uzupełniam macierz (jeszcze nic nie wiadomo o podziale - czy parzysty, nieparzysty)
    matrix_a = numpy.zeros((n, n))
    for i in range(n):
        matrix_a[i, i] = d2
        if (i > 0):
            matrix_a[i - 1][i] = d1(i * h)
            matrix_a[i][i - 1] = d3(i * h)
    matrix_a[n - 1][n - 1] = 1 / h + 1
    #dla parzystego n - otrzymujemy nieparzystą ilość punktów, więc jeden z nich znajdzie się na środku przedziału (czyli w 1)
    if n % 2 == 0:
        mid = int(n / 2) - 1
        matrix_a[mid][mid] = 2 / h - 1 / 2
    #dla nieparzystego podziału punkt 1 występuje pomiędzy punktami podziału, zatem uzupełniam odpowiednie miejsca
    else:
        left = int(n / 2) - 1
        right = left + 1
        matrix_a[left, left] = 2 / h - 1 / 8
        matrix_a[right, right] = 2 / h - 1 / 8
        matrix_a[right, left] = -1 / h - 7 / 8
        matrix_a[left, right] = -1 / h + 5 / 8

    # całkowanie metodą Simpsona:
    matrix_b = numpy.zeros((n, 1))
    #przesunięcie indeksów ze względu na to, że python indeksuje od 0, a w 0 jest warunek Dirichleta
    for i in range(1, n + 1):
        matrix_b[i - 1] = f(h * i) * 4 * h / 3

    # przesuniecie Dirichleta
    matrix_b[0] -= u0 * (-1/h -1/2)
    # warunek Neumanna
    matrix_b[n - 1] = (f(2) + 2 * f(2 - (h / 2))) * h / 6 + g1
    
    solution = numpy.linalg.solve(matrix_a, matrix_b)
    finalSolution = numpy.zeros((n + 1, 1))
    for i in range(n):
        finalSolution[i + 1] = solution[i]
    #uzupełnienie warunku Dirichleta w zerze
    finalSolution[0] = u0
    #rysowanie wykresu:
    points = numpy.linspace(0.0, 2.0, n + 1)
    matplotlib.pyplot.plot(points, finalSolution)
    matplotlib.pyplot.show()
