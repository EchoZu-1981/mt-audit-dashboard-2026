import pandas as pd

# 查看 Planning sheet 完整数据
print("=" * 80)
print("=== Planning Sheet 完整数据 ===")
print("=" * 80)
xl1 = pd.ExcelFile(r'C:\Users\zu-5\OneDrive - Mettler Toledo LLC\05 QMS Projects\20 QM AI Assistant Agency\Internal audit dashboard\2026 Audit Planning_V1_20260821.xlsx')
df_planning = pd.read_excel(xl1, sheet_name='Planning', header=1)
print("Columns:", df_planning.columns.tolist())
print("\nShape:", df_planning.shape)
print("\nData preview:")
print(df_planning[['Audit No.', 'Processes/Area', 'J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', 'Plan created', 'Report communicated']].to_string())

# 查看发现项跟进表完整数据
print("\n" + "=" * 80)
print("=== 内审发现项跟进表 完整数据 ===")
print("=" * 80)
xl2 = pd.ExcelFile(r'C:\Users\zu-5\OneDrive - Mettler Toledo LLC\05 QMS Projects\20 QM AI Assistant Agency\Internal audit dashboard\2026内审发现项跟进表.xlsx')
df_findings = pd.read_excel(xl2, sheet_name='query')
print("Columns:", df_findings.columns.tolist())
print("\nShape:", df_findings.shape)
print("\n问题类别分布:")
print(df_findings['问题类别'].value_counts())
print("\nStatus分布:")
print(df_findings['Status'].value_counts())
print("\n审核场次分布:")
print(df_findings['审核场次'].value_counts())
print("\nData preview:")
print(df_findings[['审核场次', '审核日期', '问题类别', 'DueDate', 'Status']].to_string())
