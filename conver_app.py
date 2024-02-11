import streamlit as st
import pandas as pd

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
            st.download_button(
                label="Скачать результат",
                data=file,
                file_name='export.csv',
                mime='text/csv; charset=utf-8',
                type="primary",
            )