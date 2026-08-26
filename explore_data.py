import pandas as pd

# 查看内审计划表
print("=" * 60)
print("=== 内审计划表 ===")
print("=" * 60)
xl1 = pd.ExcelFile(r'C:\Users\zu-5\OneDrive - Mettler Toledo LLC\05 QMS Projects\20 QM AI Assistant Agency\Internal audit dashboard\2026 Audit Planning_V1_20260821.xlsx')
print('Sheet names:', xl1.sheet_names)
for s in xl1.sheet_names:
    df = pd.read_excel(xl1, sheet_name=s, nrows=5)
    print(f'\n--- Sheet: {s} ---')
    print('Columns:', df.columns.tolist())
    print(df.to_string())

print("\n" + "=" * 60)
print("=== 内审发现项跟进表 ===")
print("=" * 60)
xl2 = pd.ExcelFile(r'C:\Users\zu-5\OneDrive - Mettler Toledo LLC\05 QMS Projects\20 QM AI Assistant Agency\Internal audit dashboard\2026内审发现项跟进表.xlsx')
print('Sheet names:', xl2.sheet_names)
for s in xl2.sheet_names:
    df = pd.read_excel(xl2, sheet_name=s, nrows=5)
    print(f'\n--- Sheet: {s} ---')
    print('Columns:', df.columns.tolist())
    print(df.to_string())
