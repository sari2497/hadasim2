#התוכנית קוראת את קובץ הlog בקטעים של 1000 שורות כל אחד
# ועבור כל אחד מהם סופרת שכיחות של כל אחד מקודי השגיאה שמופיע בקובץ.
# לאחר מכן התוצאות מחושבות יחד ומודפסים N קודי השגיאה השכיחים ביותר.
#יעילות זמן הריצה: O(n) כאשר n הוא מספר השורות בקובץ + O(klogm) כאשר K הוא מספר קודי השגיאה השונים בקובץ וM הוא מספר הקודים המבוקשים.
#הסבר: בתחילה יש מעבר לינארי על הקובץ וקריאת כל השורות שלו לאחר מכן הפונקציה most_common(N) פועלת ע"י בנית ערימת מקסימום בגודל N והכנסה ומיון האיברים עד לקבלתערימת מקסימום בגודל N המבוקש.
# סיבוכיות המקום היא O(K) כי בtotal_counter יש רשימה בגודל K קודי השגיאה שבקובץ.


from collections import Counter

#הגדרת הפונקציה
def sum_of_errors_in_file(N , filename = "logs.txt" ):
    chunk_size = 1000
    total_counter = Counter() #הגדרת מונה סופי מסוג COUNTER שיכיל בתוכו את סך המונים המצטברים בכל קריאה של קטע

#פתיחה וקריאת הקובץ בחלוקה למקטעים של 1000 שורות
    with open(filename , "r" , encoding= "utf-8") as file:
        while True:
            lines = [file.readline().strip()for _ in range (chunk_size) ]

            if not lines or all(line == "" for line in lines):
                break
        #עדכון המונה
            chunk_counter = Counter(line.split()[-1] for line in lines if line)
            total_counter.update(chunk_counter)

        #מציאת N קודי השגיאה השכיחים ביותר
    most_common_errors = total_counter.most_common(N)
    print(f"\n The {N} most common errors in the file '{filename}':\n")
    for code, count in most_common_errors:
        print(f"error code {code}: appeared {count} times")



sum_of_errors_in_file( 5,"logs.txt")
