#התוכנית פועלת ע"י שתי פונקציות:
# 1 check_and_divide- מבצעת בדיקות תקינות הקלט ומחלקת את הנתונים לקבצים קטנים יותר בחלוקה לפי שעות היממה סה"כ 24 קבצים
# 2 out_avg_file- csv פונקציה שמחשבת את הממוצע עבור כל שעה בכל תאריך וכותבת את התוצאה לקובץ פלט מסוג
#בשונה משאלה 2 כאן סוג הקובץ הוא שונה ולכן בוצעו התאמות בקוד כמו קריאת הקובץ עם ספריה שונה
# והבנה איך מתנהגת למשל קריאת הקובץ , בדיקת הפורמט ומעבר על השורות בקובץ
#היתרונות בקובץ parquet הם הפורמט הדחוס שלו שחוסך במקום , קריאה רציפה של הנתונים ןזיהוי שלהם ע"פ שם העמודה. בשונה מקובץ CSV הנתונים הנקראים ממנו נשמרים לפי סוגם והוא מתאים מאוד לעיבוד מקבילי

import pandas as pd
import csv
from datetime import datetime
from collections import defaultdict



def check_and_divide(filename = "time_series.parquet"):
    # הגדרת מבני נתונים - מילון וטבלת גיבוב
    rows_per_hour = defaultdict(list)
    double = set()

    # קריאת הקובץ
    try:
        df = pd.read_parquet("time_series.parquet")

    except Exception as e:
        print(f"Error reading the parquet file: {e}")
        return

    # בדיקות תקינות פורמט התאריכים והערכים המספריים
    for _, row in df.iterrows():

        date_str = str(row['timestamp']).strip()

        try:
            date_obj = datetime.strptime(date_str.strip(), "%d/%m/%Y %H:%M:%S")

        except ValueError:
            print(f"Invalid date format or invalid timestamp: {row['timestamp']}")
            continue

        try:
            value = row['value']
            is_num = float(value)
            if is_num != is_num:
                print(f"value is not a number {row['value']}")
                continue
        except (ValueError, TypeError):
            print(f"value is not a number {row['value']}")
            continue
        # בדיקת כפילויות
        if date_obj in double:
            print(f"this date already exist {date_obj}")
            continue
        #אם התאריך לא נמצא עדיין - הכנסתו לטבלה
        double.add(date_obj)

        #כל תאריך שנמצא תקין נכנס למילון כאשר המפתח הוא השעה שלו
        rows_per_hour[date_obj.hour].append(row.tolist())

    # מעבר על המילון וכתיבת הנתונים לקבצים לפי שעות
    for hour , rows in rows_per_hour.items():
        with open(f"hour_{hour}.csv", "w", newline='' , encoding="utf-8") as per_hour_file:
            writer = csv.writer(per_hour_file)
            writer.writerows(rows)
    print(len(double))




def out_avg_file():
        out_file = "avg.csv"
        value_per_date = defaultdict(list)
        names_of_files = [f"hour_{hour}.csv" for hour in range(24)]

#מעבר כל אחד מהקבצים , חישוב הממוצע עבור כל תאריך בנפרד וכתיבת התוצאה לקובץ הפלט
        for name_of_file in names_of_files:
            hour = int(name_of_file.split('_')[1].split('.')[0])
            try:
                with open(name_of_file , newline='') as hour_file:
                    read_from_file = csv.reader(hour_file)
                    for row in read_from_file:
                        #הכנסה למילון ע"פ תאריך
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





check_and_divide("time_series.parquet")
out_avg_file()

