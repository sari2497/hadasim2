#התוכנית פועלת ע"י שתי פונקציות:
# 1 check_and_divide- מבצעת בדיקות תקינות הקלט ומחלקת את הנתונים לקבצים קטנים יותר בחלוקה לפי שעות היממה סה"כ 24 קבצים
# 2 out_avg_file- csv פונקציה שמחשבת את הממוצע עבור כל שעה בכל תאריך וכותבת את התוצאה לקובץ פלט מסוג



import csv
from datetime import datetime
from collections import defaultdict



def check_and_divide(filename = "time_series.csv"):
    #הגדרת מבני נתונים כמו מילון וטבלת גיבוב
    rows_per_hour = defaultdict(list)
    double = set()
    #קריאת הקובץ
    with open("time_series.csv" , newline= '' , encoding= "utf-8" )as csvfile:
        reader = csv.reader(csvfile)

        #בדיקות תקינות פורמט התאריכים והערכים המספריים
        for row in reader:

            try:
                date_str = row[0]
                date_obj = datetime.strptime(date_str.strip(), "%d/%m/%Y %H:%M:%S")

            except ValueError:
                try:
                    date_obj = datetime.strptime(date_str.strip(), "%d/%m/%Y %H:%M")
                except ValueError:
                    print(f"Invalid date format or invalid timestamp: {row[0]}")
                    continue

            try:
                is_num = float(row[1])
                if is_num != is_num:
                    print(f"value is not a number {row[1]}")
                    continue
            except ValueError:
                print(f"value is not a number {row[1]}")
                continue
            #בדיקת כפילויות
            if date_obj in double:
                print(f"this date already exist {date_obj}")
                continue
            #אם התאריך לא נמצא עדיין - הכנסתו לטבלה
            double.add(date_obj)

            #כל תאריך שנמצא תקין נכנס למילון כאשר המפתח הוא השעה שלו
            rows_per_hour[date_obj.hour].append(row)

    #מעבר על המילון וכתיבת הנתונים לקבצים לפי שעות
    for hour , rows in rows_per_hour.items():
        with open(f"hour_{hour}.csv", "w", newline='' , encoding="utf-8") as per_hour_file:
            writer = csv.writer(per_hour_file)
            writer.writerows(rows)





def out_avg_file():

    #הגדרת מבני נתונים נצרכים וקובץ פלט
        out_file = "avg.csv"
        value_per_date = defaultdict(list)
        names_of_files = [f"hour_{hour}.csv" for hour in range(24)]
#מעבר כל אחד מהקבצים , חישוב הממוצע עבור כל תאריך בנפרד וכתיבת התוצאה לקובץ הפלט
        for name_of_file in names_of_files:
            hour = int(name_of_file.split('_')[1].split('.')[0])
            try:
                with open(name_of_file , newline='') as hour_file:
                    read_from_file = csv.reader(hour_file)
                    #הגדרת מילון ע"פ תאריך
                    for row in read_from_file:
                        date = row[0].split()[0]
                        value_per_date[date].extend(float(val) for val in row[1:])
                    for date , val in value_per_date.items():
                        avg = sum(val) / len(val)
                        if len(val) > 0:
                            with open(out_file, 'a', newline="", encoding="utf-8") as output:
                                writer = csv.writer(output)
                                writer.writerow([avg , f"{date} {hour}:00"])
                        else:
                            print(f"Warning: No values found for date {date}")

                    #ריקון המילון מערכים של שעה קודמת על מנת שלא יכנסו ערכים של שעות שונות עבור אותם תאריכים
                    value_per_date.clear()



            except FileNotFoundError:
                print(f"File {name_of_file}  isn't found")
                continue





check_and_divide("time_series.csv")
out_avg_file()

#------------------------------------------------שאלה 3----------------------------------------------
#אם הנתונים מגיעים בזרימה בזמן אמת אני אקלוט אותם אל תוך מילון מורחב שהמפתחות שלו הם התאריך והשעה הפותחת.
# כלומר כל נתון שמגיע ממוין למקום המתאים לו וחישוב הממוצע מתבצע מחדש עבור האינדקסים במילון שהתווספו להם ערכים.