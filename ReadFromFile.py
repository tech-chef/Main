# importing csv module
import csv

def compare_file():
    print("Enter the index of the location where you'd like to send the person:")
    # csv file name
    filename = "location.csv"
    rows = []

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        count_row = 0
        for row in csvreader:
            if count_row == 0
                header = row
                count_row = count_row + 1
                continue
            if count_row == 1:
                count_row += 1
                continue
            rows.append(row)
        while True:
            for row in rows:
                print( str(count_row - 1) + ". " + row[0] )
                count_row += 1
            print( str(count_row - 1) + ". " + "Do not allow" )
            inp = input().trim()
            try:
                inp = int(inp)
            except:
                print("Wrong input. Try again")
                continue
            if inp == len(rows):
                print("Not allowing the person. Thank you.")
                return [0,0]
            else:
            return [rows[inp-1][1] , rows[inp-1][2]]
