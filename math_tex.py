def signed(number):
    if number >=0:
        return '+' + str(number)
    if number < 0:
        return '-' + str(abs(number))