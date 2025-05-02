import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, ConfusionMatrixDisplay
from imblearn.over_sampling import SMOTE
import joblib

# Memuat dataset
df = pd.read_csv('dataset_skripsi.csv')
# Melihat 5 baris pertama
df.head()
# Mengganti nilai 0 dengan NaN
df.replace(0, np.nan, inplace=True)
# Informasi dataset
print("\nInformasi Dataset:")
df.info()
# Statistik deskriptif
print("\nStatistik Deskriptif:")
df.describe()
# Memeriksa jumlah nilai yang hilang dan duplikat
print("\nNilai yang hilang per kolom:")
print(df.isnull().sum())
print(f"\nJumlah data duplikat: {df.duplicated().sum()}")
# Menghapus baris dengan nilai NaN
df.dropna(inplace=True)
# Memeriksa jumlah nilai yang hilang
print("\nNilai yang hilang per kolom:")
print(df.isnull().sum())
# Reset index setelah menghapus
df.reset_index(drop=True, inplace=True)
df["CATATAN"] = df["CATATAN"].replace({"layak": "Layak","Tidak layak" : "Tidak Layak"})
df.CATATAN.value_counts()

# Visualisasi distribusi kelas target
plt.figure(figsize=(8, 6))
sns.countplot(x='CATATAN', data=df)
plt.title('Distribusi Kelas Target')
plt.show()
# Transformasi kolom CATATAN (Label encoding)
df['CATATAN'] = df['CATATAN'].map({'Layak': 1, 'Tidak layak': 0, 'Tidak Layak': 0})
# Melihat korelasi antar fitur
plt.figure(figsize=(9, 7))
correlation_matrix = df.select_dtypes(include=['float64', 'int64']).corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Korelasi antar Fitur')
plt.tight_layout()
plt.show()

# Menyimpan pemetaan label untuk referensi nanti
label_mapping = {1: 'Layak', 0: 'Tidak Layak'}
joblib.dump(label_mapping, 'label_mapping.pkl')

# Menyiapkan data
data = df.drop(columns=['PRODI','Nama','Fasahah','Tajwid','shalat','Total','Makhraj'])

# Menyimpan nama kolom untuk digunakan pada saat prediksi
feature_columns = data.drop(columns=['CATATAN']).columns.tolist()
joblib.dump(feature_columns, 'feature_columns.pkl')

X = data.drop(columns=['CATATAN'])
y = data['CATATAN']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Menggunakan SMOTE untuk menyeimbangkan kelas
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print("Distribusi kelas sebelum SMOTE:")
print(y_train.value_counts())
print("\nDistribusi kelas setelah SMOTE:")
print(y_train_smote.value_counts())
# Visualisasi distribusi kelas sebelum dan setelah SMOTE dengan label
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.countplot(x=y_train)
plt.title('Distribusi Kelas Sebelum SMOTE')
plt.xlabel('Kelas')
plt.ylabel('Jumlah')
plt.xticks(ticks=[0, 1], labels=['Tidak Layak', 'Layak'])

plt.subplot(1, 2, 2)
sns.countplot(x=y_train_smote)
plt.title('Distribusi Kelas Setelah SMOTE')
plt.xlabel('Kelas')
plt.ylabel('Jumlah')
plt.xticks(ticks=[0, 1], labels=['Tidak Layak', 'Layak'])

plt.tight_layout()
plt.show()
# Membuat dan melatih model KNN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_smote, y_train_smote)

# Evaluasi model
y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("\nLaporan Klasifikasi:")
print(classification_report(y_test, y_pred))
print('Akurasi Model KNN: {:.2f}%'.format(accuracy*100))

# Visualisasi confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Prediksi')
plt.ylabel('Aktual')
plt.savefig('static/confusion_matrix.png')
plt.close()

# Simpan model ke file
joblib.dump(knn, 'knn_model.pkl')
print("Model berhasil disimpan sebagai 'knn_model.pkl'")