###############################
# Jan Feb Mar Apr May Jun #####
# Jul Aug Sep Oct Nov Dec #####
#   1   2   3   4   5   6   7 #
#   8   9  10  11  12  13  14 #
#  15  16  17  18  19  20  21 #
#  22  23  24  25  26  27  28 #
#  29  30  31 Sun Mon Tue Wed #
################# Thu Fri Sat #
###############################

def get_date_holes(current_date):
    month = current_date.month
    month_coordinate = (month - 1)%6 + (month > 5)*1j

    day = current_date.day
    day_coordinate = (day - 1) % 7 + ((day - 1) // 7)*1j + 2j

    weekday = current_date.weekday()
    weekday_coordinate = [4, 5, 6, 4+1j, 5+1j, 6+1j, 3][weekday] + 6j

    return {month_coordinate, day_coordinate, weekday_coordinate}
