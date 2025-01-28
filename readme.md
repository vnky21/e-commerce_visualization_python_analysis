## **Cara Menjalankan Proyek**

### **1. Buat Virtual Environment**
1. Buka terminal atau command prompt.
2. Jalankan perintah berikut untuk membuat virtual environment:
   ```bash
   python -m venv env
   ```
3. Aktifkan virtual environment:
   - **Windows**:
     ```bash
     .\env\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source env/bin/activate
     ```

### **2. Instal Dependensi**
1. Pastikan virtual environment aktif.
2. Jalankan perintah berikut untuk menginstal semua dependensi:
   ```bash
   pip install -r requirements.txt
   ```

### **3. Jalankan Aplikasi Streamlit**
1. Navigasikan ke folder proyek yang berisi file `dashboard.py`.
2. Jalankan perintah berikut:
   ```bash
   streamlit run dashboard/dashboard.py
   ```
3. Aplikasi akan terbuka di browser Anda.