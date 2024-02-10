import csv
from pathlib import Path

with open('import.csv', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';') 
    imported_rows = list(reader)[1:] # без заголовка

unique_keys = set()

for row in imported_rows:
    key = tuple(row[:6])  
    unique_keys.add(key)
    
unique_keys = list(unique_keys)

grades = ["Свой сайт", "Позитивный", "Нейтральный", "Негативный", "Не релевантный", "Нет оценки"]

result_rows = []

for key in unique_keys:
    for grade in grades:
        result_rows.append(list(key) + [grade, 0, 0])

for row in imported_rows:
    key = tuple(row[:6])
    grade = row[6]  
    for result_row in result_rows:
        if key == tuple(result_row[:6]) and grade == result_row[6]:
            result_row[7] = row[7]
            result_row[8] = row[8]

headers = ["date","company_name","query_group_name","source","device","region_name","grade_name","cnt","page_tone_export"] 

with open(Path('export.csv'), 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, delimiter=';')   
    writer.writerow(headers)    
    writer.writerows(result_rows)   