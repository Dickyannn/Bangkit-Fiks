import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca dataset
day_df = pd.read_csv("cleaned_day_df.csv")
hour_df = pd.read_csv("cleaned_hour_df.csv")

# Mengubah kolom dteday menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
hour_df['datetime'] = hour_df['dteday'] + pd.to_timedelta(hour_df['hr'], unit='h')

st.title("Analisis Pengaruh Suhu, Cuaca, dan Waktu terhadap Jumlah Penyewaan Sepeda")
st.header("Nama: Dicky Anugrah")
st.subheader("Email: m001b4ky1119@bangkit.academy")
st.text("ID Dicoding: m001b4ky1119")
st.write("""Visualisasi ini menyajikan hasil olahan data mengenai penyewaan sepeda yang dipengaruhi oleh suhu, kondisi cuaca, hari kerja, dan akhir pekan. Data yang digunakan diambil dari dataset `day.csv` dan `hour.csv`, yang berisi informasi tentang cuaca, tanggal, jumlah penyewa sepeda, dan berbagai informasi lainnya.""")

# 1. Rata-rata penyewaan sepeda per bulan 
st.subheader("Rata-rata Penyewaan Sepeda per Bulan")

# Menghitung rata-rata penyewaan per bulan berdasarkan kondisi cuaca
monthly_rentals = day_df.groupby('mnth')['cnt'].mean().reset_index()

# Membuat visualisasi tren penyewaan sepeda per bulan
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=monthly_rentals, x='mnth', y='cnt', marker='o', ax=ax1)
ax1.set_title('Tren Penyewaan Sepeda per Bulan')
ax1.set_xlabel('Bulan')
ax1.set_ylabel('Jumlah Penyewaan')
ax1.set_xticks(range(1, 13))
ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
st.pyplot(fig1)

# Insight
st.write("""
**Insight:** 
- Terdapat tren penyewaan sepeda yang bervariasi setiap bulannya, dengan beberapa bulan menunjukkan puncak yang signifikan, yaitu pada bulan Juni dan juga September.
""")

# 2. Bivariat Distribusi Suhu dan Penyewaan Sepeda
st.subheader("Distribusi Suhu dan Penyewaan Sepeda")

fig2, ax2 = plt.subplots(1, 2, figsize=(14, 6))

sns.histplot(day_df['temp'], bins=30, kde=True, ax=ax2[0])
ax2[0].set_title('Distribusi Suhu')
ax2[0].set_xlabel('Suhu (normalisasi antara 0 dan 1)')

sns.histplot(day_df['cnt'], bins=30, kde=True, ax=ax2[1])
ax2[1].set_title('Distribusi Penyewaan Sepeda')
ax2[1].set_xlabel('Jumlah Penyewaan Sepeda (cnt)')

st.pyplot(fig2)

# Insight
st.write("""
**Insight:** 
- Terlihat bahwa sebaran dari suhu pada data set ini tidak dapat terlihat jelas apakah sebarannya normal ataukah miring ke kiri atau kanan.
- Distribusi penyewaan sepeda memiliki pola dengan beberapa puncak, tapi masih terlihat bahwa sebarannya normal.
""")



# 3. Rata-rata penyewaan sepeda per bulan berdasarkan kondisi cuaca
st.subheader("Rata-rata Penyewaan Sepeda per Bulan berdasarkan Kondisi Cuaca")

# Menghitung rata-rata penyewaan per bulan berdasarkan kondisi cuaca
pivot_table_monthly = day_df.pivot_table(values='cnt', index='mnth', columns='weathersit', aggfunc='mean', observed=False)

# Membuat visualisasi
fig1, ax1 = plt.subplots(figsize=(12, 6))
pivot_table_monthly.plot(kind='bar', width=0.8, ax=ax1)
ax1.set_title('Rata-rata Penyewaan Sepeda per Bulan berdasarkan Kondisi Cuaca')
ax1.set_xlabel('Bulan')
ax1.set_ylabel('Rata-rata Jumlah Penyewaan Sepeda (cnt)')
ax1.set_xticks(range(12))
ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=0)
ax1.legend(title='Kondisi Cuaca', labels=['Cerah', 'Berawan', 'Hujan'])
ax1.grid()
st.pyplot(fig1)

# Insight
st.write("""
**Insight:** 
- Bulan Agustus memiliki akumulasi penyewaan sepeda tertinggi, tetapi jumlah penyewaan sepeda tertinggi jatuh pada bulan September dengan cuaca cerah, dan paling sedikit pada bulan Januari pada saat cuaca hujan.
- Cuaca yang buruk seperti hujan mengurangi jumlah penyewaan sepeda.
""")

# 4. Hubungan antara suhu dan jumlah penyewaan sepeda
st.subheader("Hubungan antara Suhu dan Jumlah Penyewaan Sepeda")

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=day_df, x='temp', y='cnt', hue='weathersit', ax=ax2)
ax2.set_title('Hubungan antara Suhu dan Jumlah Penyewaan Sepeda')
ax2.set_xlabel('Suhu (normalisasi antara 0 dan 1)')
ax2.set_ylabel('Jumlah Penyewaan Sepeda (cnt)')
ax2.legend(title='Kondisi Cuaca')
st.pyplot(fig2)

# Insight
st.write("""
**Insight:** 
- Terdapat hubungan positif antara suhu dan jumlah penyewaan sepeda.
- Penyewaan meningkat saat suhu lebih tinggi, terutama saat cuaca cerah.
""")

# 5. Rata-rata penyewaan sepeda berdasarkan kondisi cuaca dan hari (akhir pekan vs hari kerja)
st.subheader("Rata-rata Penyewaan Sepeda berdasarkan Kondisi Cuaca dan Hari")

day_df['is_weekend'] = day_df['weekday'].isin([5, 6]).astype(int)
pivot_table = day_df.pivot_table(values='cnt', index='weathersit', columns='is_weekend', aggfunc='mean', observed=False)

fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.barplot(data=pivot_table.reset_index().melt(id_vars='weathersit'), 
            x='weathersit', 
            y='value', 
            hue='is_weekend', 
            ax=ax3)
ax3.set_title('Rata-rata Penyewaan Sepeda berdasarkan Kondisi Cuaca dan Hari')
ax3.set_xlabel('Kondisi Cuaca')
ax3.set_ylabel('Rata-rata Jumlah Penyewaan Sepeda')
ax3.set_xticks([0, 1, 2])
ax3.set_xticklabels(['Cerah', 'Berawan', 'Hujan'], rotation=45)
ax3.legend(title='Hari', loc='upper right', labels=['Hari Kerja', 'Akhir Pekan'])
st.pyplot(fig3)

# Insight
st.write("""
**Insight:**
- Penyewaan sepeda lebih tinggi pada akhir pekan dibandingkan hari kerja.
- Kondisi cuaca buruk mempengaruhi penyewaan sepeda baik pada hari kerja maupun akhir pekan.
""")

# 6. Matriks Korelasi antara Variabel
st.subheader("Matriks Korelasi antara Variabel")

corr = day_df[['temp', 'cnt', 'weathersit', 'is_weekend']].corr()
fig4, ax4 = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8}, ax=ax4)
ax4.set_title('Matriks Korelasi antara Variabel')
st.pyplot(fig4)

# Insight
st.write("""
**Insight:** 
- Terdapat korelasi positif antara suhu dan jumlah penyewaan sepeda.
- Penyewaan lebih tinggi terjadi pada akhir pekan dibandingkan hari kerja.
""")



# Insight
st.write("""
**Conclution:**
- Conclution pertanyaan 1: Ada hubungan positif antara suhu dan jumlah penyewaan sepeda, di mana akhir pekan dengan cuaca baik menghasilkan penyewaan lebih tinggi dibandingkan hari kerja. Cuaca buruk jelas mengurangi jumlah penyewaan.
- Conclution pertanyaan 2: Bulan Agustus memiliki jumlah penyewaan tertinggi (351,194 penyewaan), terutama saat kondisi cuaca baik, yang berkontribusi terhadap tingginya angka penyewaan.
""")
