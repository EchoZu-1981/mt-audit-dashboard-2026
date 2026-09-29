"""
导出 2026 内审看板为独立 HTML 文件
生成包含所有图表和数据的静态 HTML，可直接分享给他人查看
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from data_loader import load_all_data_from_files, FINDING_TO_PLAN_MAP

# ==================== 加载数据 ====================
print("正在加载数据...")
base_dir = os.path.dirname(os.path.abspath(__file__))
# 优先从 data/ 目录读取
planning_file = os.path.join(base_dir, 'data', '2026 Audit Planning_V1_20260821.xlsx')
findings_file = os.path.join(base_dir, 'data', '2026年内审发现跟进表.xlsx')
# 如果 data/ 目录不存在，回退到根目录
if not os.path.exists(planning_file):
    planning_file = os.path.join(base_dir, '2026 Audit Planning_V1_20260821.xlsx')
if not os.path.exists(findings_file):
    findings_file = os.path.join(base_dir, '2026年内审发现跟进表.xlsx')

planning_df, finding_df, dept_stats = load_all_data_from_files(planning_file, findings_file)

update_time = datetime.now().strftime("%Y-%m-%d %H:%M")

# ==================== 计算 KPI ====================
total_audits = len(planning_df) if not planning_df.empty else 0
completed_audits = len(planning_df[planning_df['status'] == 'Completed']) if not planning_df.empty and 'status' in planning_df.columns else 0
completion_rate = (completed_audits / total_audits * 100) if total_audits > 0 else 0

total_findings = len(finding_df) if not finding_df.empty else 0
resolved_findings = len(finding_df[finding_df['Status'] == 'Closed']) if not finding_df.empty and 'Status' in finding_df.columns else 0
resolution_rate = (resolved_findings / total_findings * 100) if total_findings > 0 else 0

open_findings = len(finding_df[finding_df['Status'] == 'Open']) if not finding_df.empty and 'Status' in finding_df.columns else 0
in_progress_findings = len(finding_df[finding_df['Status'] == 'On-going']) if not finding_df.empty and 'Status' in finding_df.columns else 0

# ==================== 生成图表 HTML ====================

# 图1: 审核完成进度环形图
if total_audits > 0:
    fig1 = go.Figure(data=[go.Pie(
        labels=['已完成', '未完成'],
        values=[completed_audits, total_audits - completed_audits],
        hole=0.7,
        marker=dict(colors=['#4CAF50', '#E0E0E0']),
        textinfo='percent+label',
        textposition='inside',
        textfont=dict(size=14, color='#333'),
        hoverinfo='label+value+percent'
    )])
    fig1.update_layout(
        title=dict(text=f'审核完成进度<br><sup>{completion_rate:.1f}%</sup>', font=dict(size=16, color='#0D47A1'), y=0.95),
        showlegend=False,
        margin=dict(l=40, r=40, t=80, b=40),
        height=350
    )
    chart1_html = fig1.to_html(full_html=False, include_plotlyjs='div')
else:
    chart1_html = '<div style="text-align:center;padding:50px;color:#999;">暂无审核数据</div>'

# 图2: 发现项状态分布饼图
if not finding_df.empty and 'Status' in finding_df.columns:
    status_counts = finding_df['Status'].value_counts()
    status_label_map = {'Open': '开放', 'On-going': '进行中', 'Closed': '已关闭'}
    status_counts_index = status_counts.index.map(lambda x: status_label_map.get(x, x))
    colors_map = {'开放': '#EF6C00', '进行中': '#1E88E5', '已关闭': '#4CAF50'}
    fig2 = px.pie(
        values=status_counts.values,
        names=status_counts_index,
        color=status_counts_index,
        color_discrete_map=colors_map,
        hole=0.4,
        title=f'发现项状态分布 (共 {total_findings} 项)'
    )
    fig2.update_layout(
        title=dict(font=dict(size=16, color='#0D47A1'), y=0.95),
        margin=dict(l=40, r=40, t=80, b=40),
        height=350
    )
    chart2_html = fig2.to_html(full_html=False, include_plotlyjs='div')
else:
    chart2_html = '<div style="text-align:center;padding:50px;color:#999;">暂无发现项数据</div>'

# 图3: 各部门审核发现项数量
if not finding_df.empty and 'audit_name' in finding_df.columns:
    dept_counts = finding_df['audit_name'].value_counts().head(10)
    fig3 = px.bar(
        x=dept_counts.values,
        y=dept_counts.index,
        orientation='h',
        title='各部门审核发现项数量 (Top 10)',
        color=dept_counts.values,
        color_continuous_scale='Blues'
    )
    fig3.update_layout(
        title=dict(font=dict(size=16, color='#0D47A1'), y=0.95),
        xaxis_title='发现项数量',
        margin=dict(l=160, r=40, t=80, b=40),
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    chart3_html = fig3.to_html(full_html=False, include_plotlyjs='div')
else:
    chart3_html = '<div style="text-align:center;padding:50px;color:#999;">暂无部门数据</div>'

# 图4: 各部门整改完成率
if not finding_df.empty and 'audit_name' in finding_df.columns and 'Status' in finding_df.columns:
    dept_total = finding_df.groupby('audit_name').size()
    dept_closed = finding_df[finding_df['Status'] == 'Closed'].groupby('audit_name').size()
    dept_rate = (dept_closed / dept_total * 100).fillna(0).sort_values()
    if len(dept_rate) > 0:
        fig4 = px.bar(
            x=dept_rate.values,
            y=dept_rate.index,
            orientation='h',
            title='各部门整改完成率',
            color=dept_rate.values,
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=70
        )
        fig4.update_layout(
            title=dict(font=dict(size=16, color='#0D47A1'), y=0.95),
            xaxis_title='完成率 (%)',
            xaxis=dict(range=[0, 100]),
            margin=dict(l=120, r=40, t=80, b=40),
            height=400
        )
        chart4_html = fig4.to_html(full_html=False, include_plotlyjs='div')
    else:
        chart4_html = '<div style="text-align:center;padding:50px;color:#999;">暂无整改数据</div>'
else:
    chart4_html = '<div style="text-align:center;padding:50px;color:#999;">暂无整改数据</div>'

# ==================== 生成数据表格 HTML ====================
if not finding_df.empty:
    # 取前20条发现项
    display_cols = ['审核场次', '问题描述', '责任人', 'Status', 'DueDate'] if all(col in finding_df.columns for col in ['审核场次', '问题描述', '责任人', 'Status', 'DueDate']) else None
    if display_cols:
        # 本地化状态显示
        df_display = finding_df.head(20)[display_cols].copy()
        status_map = {'Open': '开放', 'On-going': '进行中', 'Closed': '已关闭'}
        if 'Status' in df_display.columns:
            df_display['Status'] = df_display['Status'].map(lambda x: status_map.get(x, x))
        df_display.columns = ['审核场次', '问题描述', '责任人', '状态', '计划完成日期']
        table_html = df_display.to_html(escape=False, index=False, border=0)
    else:
        table_html = finding_df.head(20).to_html(escape=False, index=False, border=0)
else:
    table_html = '<p style="text-align:center;color:#999;">暂无数据</p>'

# ==================== 构建完整 HTML ====================
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026 内审看板</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #FAFAFA;
            color: #333;
        }}
        .header {{
            background: linear-gradient(135deg, #0D47A1 0%, #1565C0 50%, #1E88E5 100%);
            color: white;
            padding: 30px 40px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }}
        .header h1 {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        .header .subtitle {{
            font-size: 14px;
            opacity: 0.9;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 40px;
        }}
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        .kpi-card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            text-align: center;
            border-top: 4px solid #1E88E5;
        }}
        .kpi-card.green {{ border-top-color: #4CAF50; }}
        .kpi-card.orange {{ border-top-color: #EF6C00; }}
        .kpi-card.blue {{ border-top-color: #1E88E5; }}
        .kpi-value {{
            font-size: 42px;
            font-weight: 700;
            color: #0D47A1;
            margin: 10px 0;
        }}
        .kpi-card.green .kpi-value {{ color: #2E7D32; }}
        .kpi-card.orange .kpi-value {{ color: #EF6C00; }}
        .kpi-label {{
            font-size: 14px;
            color: #666;
            font-weight: 500;
        }}
        .charts-row {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        .chart-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .chart-card.full-width {{
            grid-column: 1 / -1;
        }}
        .section-title {{
            font-size: 20px;
            font-weight: 600;
            color: #0D47A1;
            margin-bottom: 20px;
            padding-left: 12px;
            border-left: 4px solid #1E88E5;
        }}
        .table-container {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        th {{
            background-color: #0D47A1;
            color: white;
            padding: 12px 16px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 10px 16px;
            border-bottom: 1px solid #E0E0E0;
        }}
        tr:hover {{
            background-color: #F5F5F5;
        }}
        tr:nth-child(even) {{
            background-color: #FAFAFA;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }}
        .status-已关闭 {{
            background-color: #C8E6C9;
            color: #1B5E20;
        }}
        .status-开放 {{
            background-color: #FFE0B2;
            color: #E65100;
        }}
        .status-进行中 {{
            background-color: #BBDEFB;
            color: #0D47A1;
        }}
        .status-已延期 {{
            background-color: #E0E0E0;
            color: #616161;
        }}
        .footer {{
            margin-top: 40px;
            padding: 20px;
            background: linear-gradient(135deg, #F5F5F5 0%, #EEEEEE 100%);
            border-top: 3px solid #0D47A1;
            border-radius: 8px;
            text-align: center;
            color: #666;
            font-size: 13px;
        }}
        @media (max-width: 768px) {{
            .kpi-row {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .charts-row {{
                grid-template-columns: 1fr;
            }}
            .container {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 2026 内审看板</h1>
        <div class="subtitle">
            Internal Audit Dashboard 2026 | 数据更新时间: {update_time} | 静态导出版
        </div>
    </div>

    <div class="container">
        <!-- KPI 卡片 -->
        <div class="kpi-row">
            <div class="kpi-card blue">
                <div class="kpi-label">总审核次数</div>
                <div class="kpi-value">{total_audits}</div>
                <div class="kpi-label">Total Audits</div>
            </div>
            <div class="kpi-card green">
                <div class="kpi-label">审核完成率</div>
                <div class="kpi-value">{completion_rate:.1f}%</div>
                <div class="kpi-label">{completed_audits} / {total_audits} 已完成</div>
            </div>
            <div class="kpi-card orange">
                <div class="kpi-label">发现项总数</div>
                <div class="kpi-value">{total_findings}</div>
                <div class="kpi-label">Total Findings</div>
            </div>
            <div class="kpi-card green">
                <div class="kpi-label">整改完成率</div>
                <div class="kpi-value">{resolution_rate:.1f}%</div>
                <div class="kpi-label">{resolved_findings} / {total_findings} 已关闭</div>
            </div>
        </div>

        <!-- 图表区域 -->
        <h2 class="section-title">📈 内审总览仪表板</h2>
        <div class="charts-row">
            <div class="chart-card">
                {chart1_html}
            </div>
            <div class="chart-card">
                {chart2_html}
            </div>
            <div class="chart-card">
                {chart3_html}
            </div>
            <div class="chart-card">
                {chart4_html}
            </div>
        </div>

        <!-- 数据表格 -->
        <h2 class="section-title">📋 审核发现项明细 (前20条)</h2>
        <div class="table-container">
            {table_html}
        </div>
    </div>

    <div class="footer">
        <p><strong>2026 年内审完成进度及审核发现项看板</strong></p>
        <p>本文件为静态导出版本，数据截止至 {update_time}</p>
        <p>© 2026 iNova Quality Team | 仅供内部使用</p>
    </div>
</body>
</html>
"""

# ==================== 写入文件 ====================
output_path = os.path.join(base_dir, 'audit_dashboard_2026.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ HTML 文件已生成: {output_path}")
print(f"📊 数据概览:")
print(f"   - 总审核次数: {total_audits}")
print(f"   - 审核完成率: {completion_rate:.1f}%")
print(f"   - 发现项总数: {total_findings}")
print(f"   - 整改完成率: {resolution_rate:.1f}%")
print(f"\n📤 你可以直接发送这个 HTML 文件给他人，用浏览器打开即可查看。")
