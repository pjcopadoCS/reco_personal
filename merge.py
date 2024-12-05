import pandas as pd


def merge_price():
    df1 = pd.read_excel('clean_dataset.xlsx')
    df2 = pd.read_excel('Products_Stock.xlsx')

    df2 = df2.drop_duplicates(subset='code')

    df_merged = pd.merge(df1, df2[['code', 'Selling_price']], left_on='code', right_on='code', how='left')

    df_result = df_merged[['code', 'title', 'Selling_price']]

    df_result.to_excel('products_merged.xlsx', index=False)


def merge_range():
    df1 = pd.read_excel('clean_dataset.xlsx', sheet_name='Hoja2')
    df2 = pd.read_excel('range3.xlsx')
    df3 = pd.read_excel('range4.xlsx')

    df2 = df2.drop_duplicates(subset='code')
    df3 = df3.drop_duplicates(subset='code')
 
    newdf = df1.merge(df2, on='code', how='left')

    newdf = newdf[['code', 'title', 'afrutado_especiado', 'joven_crianza', 'ligero_corpulento']]
    
    df3 = df3[['code', 'afrutado_especiado', 'joven_crianza', 'ligero_corpulento']]
    newdf = newdf.merge(df3, on='code', how='left')

    newdf.to_excel('productos_merged_range2.xlsx', index=False)


if __name__ == "__main__":
    merge_price()
    merge_range()
