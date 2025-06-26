
import pandas as pd
# تحليل بيانات دعم العملاء
# تحميل البيانات
def load_data():
    df = pd.read_csv("data/Customer_support_data.csv")
    # التأكد من وجود الأعمدة المطلوبة
    return df

# تنظيف البيانات
def clean_data(df):
    # حذف الأعمدة غير المهمة إن وجدت (مثلاً ID)


    
    if 'Unique id' in df.columns:
        df = df.drop(columns=['Unique id'])
    
    # تحويل التواريخ لو موجودة (مثلاً وقت الطلب أو الرد)
    if 'Ticket created date' in df.columns:
        df['Ticket created date'] = pd.to_datetime(df['Ticket created date'])

    # حذف الفراغات في أسماء الأعمدة
    df.columns = df.columns.str.strip()

    return df

# تحليل أساسي
def basic_info(df):
    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "nulls": df.isnull().sum(),
        "dtypes": df.dtypes,
        "unique_values": df.nunique(),
        "describe": df.describe(include='all')
    }

# تحليل حسب القناة
def channel_analysis(df):
    return df['channel_name'].value_counts()

# تحليل حسب تقييم العملاء
def csat_analysis(df):
    return df['CSAT Score'].value_counts().sort_index()

# متوسط وقت الحل حسب النوع
def avg_resolution_by_category(df):
    if 'Resolution time (in hours)' in df.columns:
        return df.groupby('category')['Resolution time (in hours)'].mean().sort_values(ascending=False)
    else:
        return "No 'Resolution time (in hours)' column found."

# تحليل حسب الوردية
def shift_analysis(df):
    return df['Agent Shift'].value_counts()

# تحليل حسب مستوى الخبرة
def tenure_analysis(df):
    return df['Tenure Bucket'].value_counts()

# لو عايز تجرب مباشرة
if __name__ == "__main__":
    df = load_data()
    df = clean_data(df)

    print("✅ Basic Info")
    info = basic_info(df)
    for k, v in info.items():
        print(f"\n🔹 {k}:\n{v}")

    print("\n✅ Channel Analysis")
    print(channel_analysis(df))

    print("\n✅ CSAT Score Analysis")
    print(csat_analysis(df))

    print("\n✅ Avg Resolution Time by Category")
    print(avg_resolution_by_category(df))

    print("\n✅ Agent Shift Distribution")
    print(shift_analysis(df))

    print("\n✅ Tenure Bucket Distribution")
    print(tenure_analysis(df))

    print(df.dtypes)
    print(df.nunique())





