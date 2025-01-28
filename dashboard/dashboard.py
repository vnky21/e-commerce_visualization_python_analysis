import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(layout="wide")


def color_bar_chart(data):
    return ['#1984c5' if x == data.max() else '#a7d5ed' for x in data]

data_dir = "dashboard/data/"

orders = pd.read_csv(data_dir + 'orders_dataset.csv')
orders_payments = pd.read_csv(data_dir + 'order_payments_dataset.csv')
orders_items = pd.read_csv(data_dir + 'order_items_dataset.csv')
sellers = pd.read_csv(data_dir + 'sellers_dataset.csv')
customers = pd.read_csv(data_dir + 'customers_dataset.csv')

data = {'orders': orders,
        'order_payments': orders_payments,
        'order_items': orders_items,
        'sellers': sellers,
        'customers': customers}

order_and_customers = pd.merge(
    data['orders'],
    data['customers'],
    on='customer_id',
    how='inner'
)

order_and_payment_df = pd.merge(
    data['orders'],
    data['order_payments'],
    how='inner',
    on='order_id'
)

order_and_customers["year_order_approved"] = pd.to_datetime(order_and_customers["order_approved_at"]).dt.year
order_and_payment_df["year_order_approved"] = pd.to_datetime(order_and_payment_df["order_approved_at"]).dt.year

customer_city_df_2018 = order_and_customers[order_and_customers["year_order_approved"] == 2018]
customer_city_df_2018 = (
    customer_city_df_2018.groupby(by="customer_city")
    .agg(count=("customer_id", "nunique"))
    .sort_values(by="count", ascending=False)
    .reset_index()
)


st.title("Dashboard Penjualan 2018")
st.sidebar.header("Navigasi")
st.sidebar.image("img/logo.png")

option = st.sidebar.selectbox(
    'Pilih Grafik',
    ['Distribusi Pesanan 2018 berdasarkan Kota', 'Metode Pembayaran 2018', 'Tingkat Payment Value 2018', 'Jumlah Seller dan Pesanan Seller']
)

if option == 'Distribusi Pesanan 2018 berdasarkan Kota':
    st.subheader("Distribusi Pesanan di Tahun 2018 berdasarkan Kota")
    top_10 = customer_city_df_2018.head(10).iloc[::-1]
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_facecolor('white')
    ax.barh(
        y=top_10['customer_city'].str.title(),
        width=top_10['count'],
        color=color_bar_chart(top_10['count']),
        zorder=2
    )

    for i, v in enumerate(top_10['count']):
        ax.text(v + 100, i, str(v), ha='left', fontsize=8, zorder=3)

    ax.grid(axis='x', linestyle='--', linewidth=0.4, zorder=0)
    ax.set_xlabel('Jumlah Order')
    ax.set_ylabel('Nama Kota')
    ax.set_title('Jumlah Order Tahun 2018 Berdasarkan Kota Customer', fontsize=12)
    ax.set_xlim(0, 10000)
   
    st.pyplot(fig)
    
    st.markdown("""
    - Kota dengan jumlah pesanan terbanyak pada tahun 2018 berdasarkan kota pelanggan adalah kota **Sao Paulo** dengan **9129** order.
    - Kota **Rio De Janiero** dan **Bella Horizonte** menempati urutan kedua dan ketiga.
    - Sebaran data menunjukkan bahwa jumlah pesanan di **Sao Paulo** sangat jauh dibandingkan kota lainnya.
    - Total ada **3.726 Kota** yang tercatat memiliki pesanan pada tahun 2018 berdasarkan kota pelanggan.
    """)

elif option == 'Metode Pembayaran 2018':
    st.subheader("Metode Pembayaran yang Paling Sering Digunakan di Tahun 2018")

    order_and_payment_2018 = order_and_payment_df[order_and_payment_df['year_order_approved'] == 2018]
    order_and_payment_2018 = order_and_payment_2018.groupby(by=['month_order_approved', 'payment_type']).agg(
        count=('order_id', 'nunique')
    ).reset_index()
    
    credit_card = order_and_payment_2018[order_and_payment_2018['payment_type'] == 'credit_card']
    boleto = order_and_payment_2018[order_and_payment_2018['payment_type'] == 'boleto']
    other = order_and_payment_2018[order_and_payment_2018['payment_type'].isin(['voucher', 'debit_card'])]
    other = other[other['month_order_approved'] != '09']
    other = other.groupby('month_order_approved').agg(
        count=('count', 'sum')
    ).reset_index()
    
    order_and_payment_2018['month_order_approved'] = pd.to_numeric(order_and_payment_2018['month_order_approved'], errors='coerce')
    credit_card = credit_card.sort_values('month_order_approved')
    boleto = boleto.sort_values('month_order_approved')
    other = other.sort_values('month_order_approved')

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_facecolor('white')
    ax.plot(credit_card['month_order_approved'], credit_card['count'], marker='o', label='Credit Card')
    ax.plot(boleto['month_order_approved'], boleto['count'], marker='o', label='Boleto')
    ax.plot(other['month_order_approved'], other['count'], marker='o', label='Other \n(Voucher, Debit Card)')

    for i, v in enumerate(credit_card['count']):
        ax.text(i + 1, v + 170, str(v), ha='center',fontsize=7)
        
    for i, v in enumerate(boleto['count']):
        ax.text(i + 1, v + 170, str(v), ha='center',fontsize=7)
        
    for i, v in enumerate(other['count']):
        ax.text(i + 1, v + 170, str(v), ha='center',fontsize=7)
        
    ax.set_ylim(0, 10000)
    ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.4, color='lightgrey')
    ax.legend(title='Jenis Pembayaran')
    ax.set_title('Frekuensi Order Berdasarkan Jenis Pembayaran Tahun 2018', fontsize=15)
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Frekuensi')
    st.pyplot(fig)
    
    st.markdown("""
                - Metode pembayaran _Credit Card_ menjadi yang paling sering digunakan dalam transaksi pesanan 
                - Semua metode pembayaran menunjukan pola penggunaan yang cenderung serpua sepanjang tahun
                - Tidak ada peningkatan atau penurun yang signifikan dalam tren penggunaan metode pembayaran
                - Metode pembayaran _Credit Card_ dan _Boleto_  memiliki tren penggunan terbanyak yang sama, yaitu pada bulan _Maret_""")

elif option == 'Tingkat Payment Value 2018':
    st.subheader("Tingkat Payment Value per Bulan pada Tahun 2018")
    
    payment_value_2018 = order_and_payment_df[order_and_payment_df['year_order_approved'] == 2018]
    payment_value_2018["year_order_approved"] = pd.to_datetime(payment_value_2018["order_approved_at"]).dt.month
    filtered_data = payment_value_2018[payment_value_2018['month_order_approved'] != 9]
    filtered_data = filtered_data.groupby(by='month_order_approved').agg({'payment_value' : 'sum'}).reset_index()

    fig, ax = plt.subplots(figsize=(12,4))
    ax.set_facecolor('white')
    ax.plot(filtered_data['month_order_approved'], filtered_data['payment_value'], marker='o', color='dodgerblue')
    for i, v in enumerate(filtered_data['payment_value']):
        ax.text(i + 1, v + 50000, (f'{int(v):,}'.replace(',', '.')), ha='center', fontsize=7)

    ax.set_ylim(80000, 1500000)
    ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.4, color='lightgrey')
    ax.set_title('Payment Value Tahun 2018', fontsize=15)
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Payment Value (BRL)')
    st.pyplot(fig)
    
    st.markdown("""
                - Tidak ada peningkatan atau penurunan yang signifikan dalam tren tingkat pembayaran
                - Tren tingkat pembayaran tertinggi terjadi pada bulan _Mei_, dan cenderung stabil tertinggi pada bulan _Maret - Mei_
                - Tren tingkat pembayaran terendah terjadi pada bulan _Februari_""")

elif option == 'Jumlah Seller dan Pesanan Seller':
    st.subheader("Jumlah Seller dan Pesanan Seller Berdasarkan Kota")
    
    sellers_and_orders = pd.merge(data['order_items'], data['sellers'], on='seller_id', how='inner')
    sellers_and_orders_2018 = pd.merge(sellers_and_orders, data['orders'], on='order_id', how='inner')
    sellers_by_city = sellers_and_orders_2018.groupby('seller_city')['seller_id'].nunique().sort_values(ascending=False).reset_index()
    orders_by_seller_city = sellers_and_orders_2018.groupby('seller_city')['order_id'].nunique().sort_values(ascending=False).reset_index()

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(26,6))

    sns.barplot(
        data=sellers_by_city.head(10),
        x='seller_id',
        y='seller_city',
        ax=ax[0],
        palette=color_bar_chart(sellers_by_city['seller_id']),
        zorder=2
    )
    for i, v in enumerate(sellers_by_city['seller_id'].head(10)):
        ax[0].text(v + 6,i, str(v), ha='left', va='center')
    
    ax[0].grid(axis='x', linewidth=0.4, linestyle='--', zorder=0)
    ax[0].set_xlabel('Jumlah Seller')
    ax[0].set_ylabel('')
    ax[0].set_title('Jumlah Seller Berdasarkan Kota',fontsize=12)
    ax[0].set_xlim(0,1000)

    sns.barplot(
        data=orders_by_seller_city.head(10),
        x='order_id',
        y='seller_city',
        ax=ax[1],
        palette=color_bar_chart(orders_by_seller_city['order_id']),
        zorder=2
    )
    for i, v in enumerate(orders_by_seller_city['order_id'].head(10)):
        ax[1].text(v + 150,i, f'{int(v):,}'.replace(',','.'), ha='left', va='center')
    ax[1].grid(axis='x', linewidth=0.4, linestyle='--', zorder=0)
    ax[1].set_xlabel('Jumlah Orderan')
    ax[1].set_ylabel('')
    ax[1].set_title('Jumlah Orderan Berdasarkan Kota Reseller',fontsize=12)
    ax[1].set_xlim(0,27500)

    st.pyplot(fig)
    
    st.markdown("""
                - Kota _Sao Paulo_ menjadi kota dengan seller dan order dari eller terbanyak, dengan jumlah 694 seller dan Orderan seller sebanyak 13.869
                - Sebaran dana menunjukkan bahwa jumlah eller dan orderan seller di _Sao Paulo_ sangat jauh dibandingkan kota lainnya
                - Meskipun kota _Ibitinga_ hanya memiliki 49 seller dan berada diperingkat 7, akan tetapi memiliki orderan seller peringkat 2 terbanyak dengan jumlah 3.146 pesanan seller""")

st.caption('Copyright (C) Rivanky Valensius Bara 2025')