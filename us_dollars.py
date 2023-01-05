from money.money import Money
#dollars in latex format
def dollars(number):
    M = Money(str(number), currency = 'USD')
    M = '\\'+ M.format('en_US')
    return M


