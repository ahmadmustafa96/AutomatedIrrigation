import sqlite3
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report



def ml_pipeline(db_path):
    time.sleep(15)
    while True:
        try:
            conn = sqlite3.connect(db_path, timeout=15)

            conn.execute('PRAGMA journal_mode = WAL')
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM readings")
            allstuff = cursor.fetchone()

            if allstuff:
                df = pd.read_sql('SELECT timestamp, crop, temperature, moisture, irrigation FROM readings ORDER BY id DESC LIMIT -1 OFFSET 10', con=conn)
                X = df[['crop', 'temperature', 'moisture']]
                Y = df['irrigation']

                preprocessor = ColumnTransformer(
                    transformers=[('num', StandardScaler(), ['temperature','moisture']),
                    ('cat', OneHotEncoder(), ['crop'])
                ])

                X_processed = preprocessor.fit_transform(X)
                X_train, X_test, Y_train, Y_test = train_test_split(X_processed, Y, test_size=0.2, random_state=42)

                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X_train, Y_train)

                predictions = model.predict(X_test)
                print(classification_report(Y_test, predictions))

                casee = pd.read_sql('SELECT timestamp, crop, temperature, moisture, irrigation FROM readings ORDER BY id DESC LIMIT 1', con=conn)
                processed_case = preprocessor.transform(casee)

                prediction = model.predict(processed_case)

                cursor.execute('UPDATE ml SET irrigation_que = ? WHERE id = 1', (int(prediction[0]),))
                print(f"SEEEEEEE: {(int(prediction[0]),)}")
                conn.commit()
                conn.close()
        except Exception as e:
            print(f"ML Error {e}")

        time.sleep(10)

if __name__ == '__main__':
    db_path = input("Enter database path: ")
    ml_pipeline(db_path)

        

