import csv
from datetime import datetime

def process_shifts(path_to_csv):

    
    workerList = []
    costToHour = {}#dictionary of cost for each hour
    with open(path_to_csv) as file:
        reader = csv.reader(file)
        
        #csv.DictReader

        count = 0
        next(reader)

        for row in reader:
            break_notes = convert_breaktimes(row[0])
            workerList.append([break_notes[0], break_notes[1], datetime.strptime(row[3], '%H:%M'), datetime.strptime(row[1], '%H:%M'), float(row[2])])
            if count > 6:
                break

            count += 1;
    #for each time loop through each item getting the worker's salary
    for i in range(9,23):
        hourStart = datetime.strptime(str(i) + ":00", '%H:%M')
        hourEnd = datetime.strptime(str(i+1) + ":00", '%H:%M')
        count = 0.0
        for item in workerList:
            count = count + calculate_hour_employee(hourStart, hourEnd, item[0], item[1], item[2], item[3], item[4])
        costToHour[str(i) + ":00"] = count

    return costToHour


def convert_breaktimes(break_notes):
    break_times = []
    break_times = break_notes.split("-")
    start = format_time(break_times[0])
    end = format_time(break_times[1])
    break_dates = [datetime.strptime(start, '%H:%M'), datetime.strptime(end, '%H:%M')]
    return break_dates

def break_length(break_dates):
    dur = break_dates[1]-break_dates[0]
    hours = dur.seconds/3600.0
    return hours

def format_24hrs(time):
    result = int(time)
    if(result<8):
        result = result + 12
        if(result>23):
            result = result-24

    result = str(result)
    return result

def format_time(time):
    result = time 
    if("PM" in time):
        result = result.replace("PM", "")

    if(" " in time):
        result = result.replace(" ", "")

    if("." in time):
        halves = result.split(".")
        placeHolder = format_24hrs(halves[0])
        result = placeHolder + ":" + halves[1]
    if(":" not in result):
        result = format_24hrs(result)
        return result + ":00"
    return result

def calculate_hour_employee(hourStart, hourEnd, breakStart, breakEnd, shiftStart, shiftEnd, cost):
    if(hourStart<shiftStart and (hourEnd <shiftStart or hourEnd == shiftStart)):
        return 0

    if((hourStart>shiftEnd or hourStart == shiftEnd) and hourEnd> shiftEnd):
        return 0

    if((hourStart>breakStart or hourStart == breakStart) and (hourEnd<breakEnd or hourEnd == breakEnd)):
        return 0

    if((hourStart>breakStart or hourStart == breakStart) and hourStart<breakEnd and hourEnd > breakEnd):
        times = [breakEnd, hourEnd]
        return break_length(times) * cost

    if(hourStart<breakStart and (hourEnd<breakEnd or hourEnd==breakEnd) and hourEnd>breakStart):
        times = [hourStart, breakStart]
        return break_length(times) * cost

    return cost

def calculate_hour_cost(start, end, workerList):
    counter = 0.0
    for worker in workerList:
        cost = calculate_hour_employee(start, end, worker[0], worker[1], worker[2], worker[3], worker[4])
        counter = counter + cost 

    return counter


def process_sales(path_to_csv):
    salesList = []
    salesHourValue = {}
    with open(path_to_csv) as file:
        reader = csv.reader(file)
        count = 0
        next(reader)
        for row in reader:
            salesList.append([row[0], row[1]])


    for i in range(9,23):
        hour = str(i)
        hourSum = 0.0
        for row in salesList:
                time = row[1].split(":") #get time and split it at ":"
                if(hour == time[0]):
                    hourSum = hourSum + float(row[0])
        salesHourValue[str(i) + ":00"] = hourSum
        
            
    return salesHourValue

def compute_percentage(shifts, sales):
    percentages = {}
    salesHourValue = sales
    costToHour = shifts
    for i in range(9,23):
        hour = str(i) + ":00"
        if(float(salesHourValue[hour]) == 0.0):
            percent = float(salesHourValue[hour])-float(costToHour[hour]) 
        else:
            percent = float(costToHour[hour])/float(salesHourValue[hour])*100

        percentages[hour] = percent
    return percentages


def best_and_worst_hour(percentages):
    min = 0.0
    best = ""
    worst = ""
    for item in percentages:
        if(percentages[item]>=0.0):
            min = percentages[item]#set starting value to non negative number

    for item in percentages:
        if(percentages[item]<min and percentages[item] >= 0.0):
            min = percentages[item]
            best = item

    for item in percentages:
        if(percentages[item]<min):
            min = percentages[item]
            worst = item

    bestAndWorst = [best, worst]
    return bestAndWorst

def main(path_to_shifts, path_to_sales):
    """
    Do not touch this function, but you can look at it, to have an idea of
    how your data should interact with each other
    """
    shifts_processed = process_shifts(path_to_shifts)
    sales_processed = process_sales(path_to_sales)
    percentages = compute_percentage(shifts_processed, sales_processed)
    best_hour, worst_hour = best_and_worst_hour(percentages)
    print("best hour: " + best_hour)
    print("worst hour: " + worst_hour)
    return best_hour, worst_hour

if __name__ == '__main__':
    path_to_sales = "transactions.csv"
    path_to_shifts = "work_shifts.csv"
    best_hour, worst_hour = main(path_to_shifts, path_to_sales)


