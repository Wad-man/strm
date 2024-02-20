import streamlit as st
import pandas as pd
import io
import openpyxl
from openpyxl.workbook import Workbook


#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context

st.title('Конвертация файла')
st.text('Загружаете файл, нажимаете конвертировать, затем скачиваете готовый файл.')


uploaded_file = st.file_uploader("Загрузка файла :thinking_face:", type=['csv'])
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name, "FileType":uploaded_file.type}
    st.subheader("Файл загружен :sunglasses:")
    result = st.button("Конвертировать")
    if result:
        # Чтение файла import.csv
        df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
        #df = df.iloc[1:]  # убрать первую строку

        # Формируем уникальные значения
        unique_keys = df[['date','company_name','query_group_name','source','device','region_name']].drop_duplicates().values.tolist()

        # Справочник значений
        grades = ["Свой сайт", "Позитивный", "Нейтральный", "Негативный", "Не релевантный", "Нет оценки"]

        # Формируем новый файл
        result_df = pd.DataFrame(columns=['date','company_name','query_group_name','source','device','region_name','grade_name','cnt','page_tone_export'])
        # Цикл для заполнения нового файла
        for key in unique_keys:
            for grade in grades:
                temp_df = pd.DataFrame([key + [grade, 0, 0]], columns=result_df.columns)
                result_df = pd.concat([result_df, temp_df])

        # Замена нулей на значения из исходного DataFrame
        updates = {}           
        for _, row in df.iterrows():
            key = row[['date','company_name','query_group_name','source','device','region_name','grade_name']].values.tolist()
            mask = result_df[['date','company_name','query_group_name','source','device','region_name','grade_name']].eq(key).all(1)

            result_df.loc[mask, 'cnt'] = row['cnt']
            result_df.loc[mask, 'page_tone_export'] = row['page_tone_export']

        result_df.to_csv('export.csv', sep=';', index=False, encoding='utf-8-sig')

        st.subheader("Файл готов :heart:")
        with open('export.csv', encoding='utf-8-sig') as file:
            # сохранить в CSV
            st.download_button(
                label="Скачать результат (CSV)",
                data=file,
                file_name='export.csv',
                mime='text/csv; charset=utf-8',
                type="secondary",
            )

            # сохранить в XLSX
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                result_df.to_excel(writer, sheet_name='PageTone', index=False)
                workbook = writer.book
                worksheet = workbook.active
                worksheet.title = 'PageTone'
                worksheet.column_dimensions['A'].width = 20
                worksheet.column_dimensions['B'].width = 20
                worksheet.column_dimensions['C'].width = 20
                worksheet.column_dimensions['D'].width = 20
                worksheet.column_dimensions['E'].width = 20
                worksheet.column_dimensions['F'].width = 20
                worksheet.column_dimensions['G'].width = 20
                worksheet.column_dimensions['H'].width = 20
                worksheet.column_dimensions['I'].width = 20
                
            st.download_button(
                label="Скачать результат (XLSX)",
                data=output.getvalue(),
                file_name='export.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                type="primary",
            )
