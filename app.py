"""
2026 年内审完成进度及审核发现项看板
Internal Audit Dashboard - 2026
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from data_loader import load_all_data, load_all_data_from_files, FINDING_TO_PLAN_MAP

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="2026 内审看板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义 CSS ====================
st.markdown("""
<style>
    /* MT 主题色板 */
    :root {
        --mt-dark-blue: #0D47A1;
        --mt-mid-blue: #1565C0;
        --mt-blue: #1E88E5;
        --mt-light-blue: #42A5F5;
        --mt-lighter-blue: #90CAF9;
        --mt-lightest-blue: #BBDEFB;
        --mt-dark-green: #1B5E20;
        --mt-mid-green: #2E7D32;
        --mt-green: #4CAF50;
        --mt-light-green: #66BB6A;
        --mt-lighter-green: #A5D6A7;
        --mt-lightest-green: #C8E6C9;
        --mt-dark-orange: #E65100;
        --mt-orange: #EF6C00;
        --mt-light-orange: #FFA726;
        --mt-lightest-orange: #FFE0B2;
    }
    .main-header {
        font-size: 28px;
        font-weight: bold;
        color: var(--mt-dark-blue);
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 18px;
        font-weight: 600;
        color: var(--mt-mid-blue);
        margin-top: 20px;
        margin-bottom: 10px;
        border-left: 4px solid var(--mt-blue);
        padding-left: 10px;
    }
    .status-completed { color: var(--mt-mid-green); font-weight: bold; }
    /* 全局背景色 */
    .stApp {
        background-color: #FAFAFA;
    }
    section[data-testid="stSidebar"] {
        background-color: var(--mt-dark-blue);
    }
    /* 侧边栏标题和文本用白色 */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: white !important;
    }
    /* 侧边栏按钮用深色文字，白色背景 */
    section[data-testid="stSidebar"] button {
        color: #0D47A1 !important;
        background-color: #FFFFFF !important;
        border: 2px solid #42A5F5 !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] button:hover {
        background-color: #BBDEFB !important;
        border-color: #1E88E5 !important;
        color: #0D47A1 !important;
    }
    section[data-testid="stSidebar"] button span {
        color: #0D47A1 !important;
    }
    section[data-testid="stSidebar"] button p {
        color: #0D47A1 !important;
    }
    /* 看板底部所有者声明样式 */
    .dashboard-footer {
        margin-top: 40px;
        padding: 20px;
        background: linear-gradient(135deg, #F5F5F5 0%, #EEEEEE 100%);
        border-top: 3px solid var(--mt-dark-blue);
        border-radius: 8px;
        text-align: center;
    }
    .footer-owner {
        font-size: 16px;
        font-weight: 600;
        color: var(--mt-dark-blue);
        margin-bottom: 8px;
    }
    .footer-badge {
        display: inline-block;
        background-color: var(--mt-dark-blue);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        margin-top: 5px;
    }
    .footer-info {
        font-size: 12px;
        color: #757575;
        margin-top: 10px;
    }    /* 侧边栏 radio 和 multiselect 文字用白色 */
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    .status-planned { color: var(--mt-orange); font-weight: bold; }
    .status-pending { color: #9E9E9E; font-weight: bold; }
    .stDataFrame { font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# ==================== 加载数据 ====================
def get_data_from_files(planning_file=None, findings_file=None):
    """从文件加载数据"""
    base_dir = r"C:\Users\zu-5\OneDrive - Mettler Toledo LLC\05 QMS Projects\20 QM AI Assistant Agency\Internal audit dashboard"
    
    if planning_file is None:
        planning_file = os.path.join(base_dir, '2026 Audit Planning_V1_20260821.xlsx')
    if findings_file is None:
        findings_file = os.path.join(base_dir, '2026内审发现项跟进表.xlsx')
    
    return load_all_data_from_files(planning_file, findings_file)


# 初始化 session state
if 'planning_df' not in st.session_state:
    # 尝试从本地文件加载，如果失败则创建空 DataFrame（等待用户上传）
    try:
        planning_df, findings_df, dept_stats = get_data_from_files()
        st.session_state.has_data = True
    except FileNotFoundError:
        # 文件不存在，创建空 DataFrame
        planning_df = pd.DataFrame()
        findings_df = pd.DataFrame()
        dept_stats = pd.DataFrame()
        st.session_state.has_data = False
    
    st.session_state.planning_df = planning_df
    st.session_state.findings_df = findings_df
    st.session_state.dept_stats = dept_stats
    st.session_state.last_updated = datetime.now()

planning_df = st.session_state.planning_df
findings_df = st.session_state.findings_df
dept_stats = st.session_state.dept_stats

# 检查是否有数据
if not st.session_state.get('has_data', False) or len(findings_df) == 0:
    st.info("📢 **欢迎使用 2026 内审看板！**")
    st.markdown("""
    ### 请先上传数据文件
    
    请通过侧边栏的 **"📁 上传文件"** 按钮上传以下 Excel 文件：
    1. **审核计划表** - `2026 Audit Planning_V1_20260821.xlsx`
    2. **发现项跟进表** - `2026内审发现项跟进表.xlsx`
    
    上传后看板将自动加载并显示数据。
    """)
    st.stop()  # 停止渲染后续内容

# ==================== 侧边栏 ====================
st.sidebar.markdown("""
<div class='main-header'>📊 2026 内审看板</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"**数据更新时间**: {st.session_state.last_updated.strftime('%Y-%m-%d %H:%M')}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 数据管理")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("🔄 刷新数据", use_container_width=True):
        st.session_state.last_updated = datetime.now()
        st.success("数据已刷新！")
        st.rerun()
with col2:
    if st.button("📁 上传文件", use_container_width=True):
        st.session_state.show_upload = True

# 文件上传区域
if st.session_state.get('show_upload', False):
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📤 上传更新文件")
    
    uploaded_type = st.sidebar.radio("选择文件类型", ["审核计划表", "发现项跟进表"], horizontal=True)
    uploaded_file = st.sidebar.file_uploader("上传 Excel 文件", type=['xlsx', 'xls'], accept_multiple_files=False)
    
    if uploaded_file is not None:
        try:
            from data_loader import load_planning_from_uploaded_file, load_findings_from_uploaded_file, compute_department_stats
            
            if uploaded_type == "审核计划表":
                new_planning = load_planning_from_uploaded_file(uploaded_file)
                st.session_state.planning_df = new_planning
                st.sidebar.success(f"✅ 审核计划已更新！共 {len(new_planning)} 个项目")
            else:
                new_findings = load_findings_from_uploaded_file(uploaded_file)
                st.session_state.findings_df = new_findings
                st.session_state.dept_stats = compute_department_stats(new_findings)
                st.sidebar.success(f"✅ 发现项已更新！共 {len(new_findings)} 条记录")
            
            st.session_state.last_updated = datetime.now()
            st.session_state.show_upload = False
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"❌ 文件处理失败: {str(e)}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 导航")
page = st.sidebar.radio(
    "选择视图",
    ["📈 总览仪表板", "📋 审核进度", "🔍 发现项分析", "⏱️ 整改时效", "📝 开放问题清单"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 筛选")
all_audits = sorted(dept_stats['audit_name'].unique().tolist())
selected_audits = st.sidebar.multiselect(
    "选择审核场地",
    all_audits,
    default=all_audits
)

# 筛选数据
filtered_findings = findings_df[findings_df['audit_name'].isin(selected_audits)]
filtered_stats = dept_stats[dept_stats['audit_name'].isin(selected_audits)]

# ==================== 总览仪表板 ====================
if page == "📈 总览仪表板":
    st.markdown("<div class='main-header'>📈 内审总览仪表板</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # KPI 指标卡
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_audits = len(planning_df)
    completed_audits = len(planning_df[planning_df['status'] == 'Completed'])
    total_findings = len(findings_df)
    closed_findings = len(findings_df[findings_df['Status'] == 'Closed'])
    open_findings = len(findings_df[findings_df['Status'].isin(['Open', 'On-going'])])
    
    col1.metric("审核项目总数", f"{total_audits}")
    col2.metric("已完成审核", f"{completed_audits}", f"{completed_audits/total_audits*100:.0f}%")
    col3.metric("审核发现总数", f"{total_findings}")
    col4.metric("已关闭发现项", f"{closed_findings}", f"{closed_findings/total_findings*100:.0f}%")
    col5.metric("开放/进行中", f"{open_findings}", delta=None if open_findings == 0 else f"{open_findings} 待处理")
    
    st.markdown("---")
    
    # 第一行图表
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='sub-header'>审核完成进度</div>", unsafe_allow_html=True)
        status_counts = planning_df['status'].value_counts()
        fig_status = go.Figure(data=[go.Pie(
            labels=['已完成', '计划中'],
            values=[status_counts.get('Completed', 0), status_counts.get('Planned', 0)],
            hole=0.6,
            marker_colors=['#2E7D32', '#EF6C00'],
            textinfo='percent+label',
            textposition='inside'
        )])
        fig_status.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(t=0, b=0, l=0, r=0),
            height=300
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        st.markdown("<div class='sub-header'>发现项状态分布</div>", unsafe_allow_html=True)
        status_dist = filtered_findings['Status'].value_counts()
        fig_finding_status = go.Figure(data=[go.Pie(
            labels=['Closed', 'On-going', 'Open'],
            values=[
                status_dist.get('Closed', 0),
                status_dist.get('On-going', 0),
                status_dist.get('Open', 0)
            ],
            hole=0.6,
            marker_colors=['#0f9d58', '#f9ab00', '#d93025'],
            textinfo='percent+label',
            textposition='inside'
        )])
        fig_finding_status.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(t=0, b=0, l=0, r=0),
            height=300
        )
        st.plotly_chart(fig_finding_status, use_container_width=True)
    
    # 第二行：各部门发现项数量
    st.markdown("<div class='sub-header'>各部门审核发现项数量</div>", unsafe_allow_html=True)
    
    chart_data = filtered_stats[['audit_name', 'nc_count', 'oi_count']].copy()
    chart_data = chart_data.melt(id_vars='audit_name', var_name='类型', value_name='数量')
    chart_data['类型'] = chart_data['类型'].map({'nc_count': '一般不符合项', 'oi_count': '改进建议项'})
    
    fig_bar = px.bar(
        chart_data,
        x='audit_name',
        y='数量',
        color='类型',
        barmode='group',
        color_discrete_map={'一般不符合项': '#E65100', '改进建议项': '#1E88E5'},
        text='数量'
    )
    fig_bar.update_layout(
        xaxis_tickangle=-45,
        height=400,
        showlegend=True,
        margin=dict(t=0, b=100, l=60, r=20)
    )
    fig_bar.update_traces(textposition='outside', textfont=dict(size=10))
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # 第三行：完成率排行
    st.markdown("<div class='sub-header'>各部门整改完成率</div>", unsafe_allow_html=True)
    
    completion_data = filtered_stats[['audit_name', 'completion_rate', 'total_findings']].copy()
    completion_data = completion_data.sort_values('completion_rate', ascending=True)
    
    fig_completion = px.bar(
        completion_data,
        y='audit_name',
        x='completion_rate',
        orientation='h',
        color='completion_rate',
        color_continuous_scale='RdYlGn',
        text='completion_rate'
    )
    fig_completion.update_layout(
        height=max(300, len(completion_data) * 30),
        xaxis_title='完成率 (%)',
        xaxis_range=[0, 100],
        margin=dict(t=0, b=30, l=150, r=50),
        coloraxis_showscale=False
    )
    fig_completion.update_traces(texttemplate='%{x:.1f}%', textposition='outside', textfont=dict(size=10))
    st.plotly_chart(fig_completion, use_container_width=True)

# ==================== 审核进度 ====================
elif page == "📋 审核进度":
    st.markdown("<div class='main-header'>📋 审核项目进度甘特图</div>", unsafe_allow_html=True)
    
    # 甘特图数据准备
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_nums = list(range(1, 13))
    
    gantt_data = []
    for _, row in planning_df.iterrows():
        if row['plan_month']:
            month_idx = month_order.index(row['plan_month']) if row['plan_month'] in month_order else 0
            color = '#0f9d58' if row['status'] == 'Completed' else '#f9ab00'
            gantt_data.append({
                'audit_no': row['audit_no'],
                'audit_area': row['audit_area'],
                'lead_auditor': row['lead_auditor'],
                'start': month_nums[month_idx],
                'end': month_nums[month_idx],
                'status': row['status'],
                'color': color,
                'closed_ncs': int(row['closed_ncs']),
                'open_ncs': int(row['open_ncs'])
            })
    
    gantt_df = pd.DataFrame(gantt_data)
    
    # 使用 bar chart 替代 Gantt（Plotly go.Gantt 不存在）
    fig_gantt = go.Figure()
    
    for _, row in gantt_df.iterrows():
        color = '#2E7D32' if row['status'] == 'Completed' else '#EF6C00'
        fig_gantt.add_trace(go.Bar(
            orientation='h',
            x=[1],
            y=[row['audit_area']],
            name=row['audit_no'],
            marker_color=color,
            hovertext=f"<b>{row['audit_area']}</b><br>审核编号: {row['audit_no']}<br>主审: {row['lead_auditor']}<br>已关闭 NC: {row['closed_ncs']}<br>开放 NC: {row['open_ncs']}<br>状态: {row['status']}",
            hoverinfo='text',
            showlegend=False
        ))
    
    fig_gantt.update_layout(
        xaxis=dict(title='月份', tickvals=month_nums, ticktext=month_order, showgrid=False, zeroline=False),
        yaxis=dict(autorange="reversed", showgrid=False),
        height=max(500, len(gantt_df) * 35),
        margin=dict(t=30, b=80, l=200, r=50),
        bargap=0.3,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_gantt, use_container_width=True)
    
    # 审核计划明细表
    st.markdown("<div class='sub-header'>审核计划明细</div>", unsafe_allow_html=True)
    
    display_df = planning_df[['audit_no', 'audit_area', 'plan_month', 'status', 'lead_auditor', 
                               'closed_ncs', 'open_ncs', 'remarks']].copy()
    display_df.columns = ['审核编号', '审核范围', '计划月份', '状态', '主审', '已关闭NC', '开放NC', '备注']
    display_df['状态'] = display_df['状态'].map({'Completed': '✅ 已完成', 'Planned': '📋 计划中'})
    
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)

# ==================== 发现项分析 ====================
elif page == "🔍 发现项分析":
    st.markdown("<div class='main-header'>🔍 审核发现项详细分析</div>", unsafe_allow_html=True)
    
    # 按问题类别和状态的堆叠柱状图
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='sub-header'>问题类别分布</div>", unsafe_allow_html=True)
        category_dist = filtered_findings['问题类别'].value_counts()
        fig_category = go.Figure(data=[go.Pie(
            labels=category_dist.index,
            values=category_dist.values,
            hole=0.6,
            marker_colors=['#E65100', '#1E88E5'],
            textinfo='percent+label+value',
            textposition='inside'
        )])
        fig_category.update_layout(height=350, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        st.markdown("<div class='sub-header'>状态分布</div>", unsafe_allow_html=True)
        status_dist = filtered_findings['Status'].value_counts()
        fig_status = go.Figure(data=[go.Pie(
            labels=['Closed', 'On-going', 'Open'],
            values=[
                status_dist.get('Closed', 0),
                status_dist.get('On-going', 0),
                status_dist.get('Open', 0)
            ],
            hole=0.6,
            marker_colors=['#0f9d58', '#f9ab00', '#d93025'],
            textinfo='percent+label+value',
            textposition='inside'
        )])
        fig_status.update_layout(height=350, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_status, use_container_width=True)
    
    # 各部门发现项堆叠图
    st.markdown("<div class='sub-header'>各部门发现项 × 状态 堆叠图</div>", unsafe_allow_html=True)
    
    pivot_data = filtered_findings.groupby(['audit_name', 'Status']).size().unstack(fill_value=0)
    pivot_data = pivot_data.reindex(columns=['Closed', 'On-going', 'Open'], fill_value=0)
    pivot_data['audit_name'] = pivot_data.index
    pivot_data = pivot_data.melt(id_vars='audit_name', var_name='Status', value_name='count')
    pivot_data['Status'] = pivot_data['Status'].map({'Closed': '已关闭', 'On-going': '进行中', 'Open': '开放'})
    
    fig_stacked = px.bar(
        pivot_data,
        x='audit_name',
        y='count',
        color='Status',
        barmode='stack',
        color_discrete_map={'已关闭': '#2E7D32', '进行中': '#FFA726', '开放': '#E65100'},
        text='count'
    )
    fig_stacked.update_layout(
        xaxis_tickangle=-45,
        height=450,
        margin=dict(t=0, b=100, l=60, r=20)
    )
    fig_stacked.update_traces(textposition='inside', textfont=dict(size=9))
    st.plotly_chart(fig_stacked, use_container_width=True)
    
    # 详细数据表
    st.markdown("<div class='sub-header'>各部门统计汇总</div>", unsafe_allow_html=True)
    
    summary_df = filtered_stats[['audit_name', 'plan_id', 'lead_auditor', 'total_findings', 
                                  'nc_count', 'oi_count', 'closed', 'ongoing', 'open', 
                                  'completion_rate']].copy()
    summary_df = summary_df.sort_values('total_findings', ascending=False)
    summary_df.columns = ['审核场次', '计划编号', '主审', '发现项总数', '不符合项', '改进建议项',
                          '已关闭', '进行中', '开放', '完成率(%)']
    
    st.dataframe(summary_df, use_container_width=True, hide_index=True, height=400)
    
    # 详细发现项列表
    st.markdown("<div class='sub-header'>审核发现项明细</div>", unsafe_allow_html=True)
    
    detail_df = filtered_findings[['审核场次', '审核日期', '问题描述', '问题类别', '责任人', 
                                    'DueDate', 'Status']].copy()
    detail_df.columns = ['审核场次', '审核日期', '问题描述', '问题类别', '责任人', '预计完成日期', '状态']
    detail_df['审核日期'] = detail_df['审核日期'].dt.strftime('%Y-%m-%d')
    detail_df['预计完成日期'] = detail_df['预计完成日期'].dt.strftime('%Y-%m-%d')
    
    # 状态颜色标记 - 返回与列数相同的列表
    def status_color(row):
        if row['状态'] == 'Closed':
            return ['background-color: #C8E6C9'] * len(row)  # Closed - 浅绿
        elif row['状态'] == 'On-going':
            return ['background-color: #FFE0B2'] * len(row)  # On-going - 浅橙
        else:
            return ['background-color: #FFCCBC'] * len(row)  # Open - 浅红
    
    st.dataframe(
        detail_df.style.apply(status_color, axis=1),
        use_container_width=True,
        hide_index=True,
        height=500
    )

# ==================== 整改时效分析 ====================
elif page == "⏱️ 整改时效":
    st.markdown("<div class='main-header'>⏱️ 整改时效分析</div>", unsafe_allow_html=True)
    
    # 关键指标
    col1, col2, col3 = st.columns(3)
    
    closed_days = filtered_findings[filtered_findings['Status'] == 'Closed']['整改天数'].dropna()
    all_days = filtered_findings['整改天数'].dropna()
    
    col1.metric("已关闭项整改中位数", f"{int(closed_days.median())} 天" if len(closed_days) > 0 else "N/A")
    col2.metric("已关闭项整改平均值", f"{closed_days.mean():.0f} 天" if len(closed_days) > 0 else "N/A")
    col3.metric("预计整改天数中位数", f"{int(all_days.median())} 天" if len(all_days) > 0 else "N/A")
    
    st.markdown("---")
    
    # 各部门整改天数箱线图
    st.markdown("<div class='sub-header'>各部门整改天数分布 (箱线图)</div>", unsafe_allow_html=True)
    
    closed_findings = filtered_findings[filtered_findings['Status'] == 'Closed'].copy()
    
    if len(closed_findings) > 0:
        fig_box = px.box(
            closed_findings,
            x='audit_name',
            y='整改天数',
            color='audit_name',
            points='all',
            title='各部门已关闭项整改天数分布',
            labels={'整改天数': '整改天数 (天)', 'audit_name': '审核场次'}
        )
        fig_box.update_layout(
            xaxis_tickangle=-45,
            height=450,
            showlegend=False,
            margin=dict(t=50, b=100, l=60, r=20)
        )
        st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.info("暂无已关闭的发现项数据")
    
    # 各部门时效对比柱状图
    st.markdown("<div class='sub-header'>各部门整改时效对比</div>", unsafe_allow_html=True)
    
    efficiency_data = filtered_stats[['audit_name', 'median_days_closed', 'mean_days_closed', 'median_due_days']].copy()
    efficiency_data = efficiency_data.dropna(subset=['median_days_closed'])
    
    if len(efficiency_data) > 0:
        efficiency_data = efficiency_data.melt(
            id_vars='audit_name',
            var_name='指标',
            value_name='天数'
        )
        efficiency_data['指标'] = efficiency_data['指标'].map({
            'median_days_closed': '实际整改中位数',
            'mean_days_closed': '实际整改平均值',
            'median_due_days': '预计整改中位数'
        })
        
        fig_efficiency = px.bar(
            efficiency_data,
            x='audit_name',
            y='天数',
            color='指标',
            barmode='group',
            color_discrete_map={
                '实际整改中位数': '#1E88E5',
                '实际整改平均值': '#757575',
                '预计整改中位数': '#FFA726'
            },
            text='天数'
        )
        fig_efficiency.update_layout(
            xaxis_tickangle=-45,
            height=450,
            yaxis_title='天数',
            margin=dict(t=0, b=100, l=60, r=20)
        )
        fig_efficiency.update_traces(textposition='outside', textfont=dict(size=9))
        st.plotly_chart(fig_efficiency, use_container_width=True)
    
    # 详细数据表
    st.markdown("<div class='sub-header'>各部门时效详细数据</div>", unsafe_allow_html=True)
    
    eff_df = filtered_stats[['audit_name', 'total_findings', 'closed', 'completion_rate',
                              'median_days_closed', 'mean_days_closed', 'median_due_days']].copy()
    eff_df = eff_df.sort_values('median_days_closed', ascending=True)
    eff_df.columns = ['审核场次', '发现项总数', '已关闭数', '完成率(%)', 
                      '整改中位数(天)', '整改平均值(天)', '预计天数中位数(天)']
    
    st.dataframe(eff_df, use_container_width=True, hide_index=True, height=400)

# ==================== 开放问题清单 ====================
elif page == "📝 开放问题清单":
    st.markdown("<div class='main-header'>📝 开放/进行中问题清单</div>", unsafe_allow_html=True)
    
    open_findings = filtered_findings[filtered_findings['Status'].isin(['Open', 'On-going'])].copy()
    
    # 统计
    col1, col2, col3 = st.columns(3)
    ongoing_count = len(open_findings[open_findings['Status'] == 'On-going'])
    open_count = len(open_findings[open_findings['Status'] == 'Open'])
    
    # 计算逾期（DueDate < 今天）
    today = pd.Timestamp(datetime.now())
    overdue = len(open_findings[open_findings['DueDate'] < today])
    
    col1.metric("进行中 (On-going)", ongoing_count)
    col2.metric("开放 (Open)", open_count)
    col3.metric("⚠️ 已逾期", overdue, delta=None if overdue == 0 else f"需关注")
    
    st.markdown("---")
    
    if len(open_findings) > 0:
        # 筛选选项
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect(
                "按状态筛选",
                ['On-going', 'Open'],
                default=['On-going', 'Open']
            )
        with col2:
            show_overdue_only = st.checkbox("仅显示已逾期项", value=False)
        
        filtered_open = open_findings[open_findings['Status'].isin(status_filter)]
        if show_overdue_only:
            filtered_open = filtered_open[filtered_open['DueDate'] < today]
        
        # 按审核场地分组展示
        st.markdown("<div class='sub-header'>问题详情</div>", unsafe_allow_html=True)
        
        for audit_name, group in filtered_open.groupby('audit_name'):
            with st.expander(f"📁 {audit_name} ({len(group)} 项)", expanded=False):
                detail_df = group[['审核场次', '审核日期', '问题描述', '问题类别', '责任人', 
                                    '原因分析及纠正措施', 'DueDate', 'Status']].copy()
                detail_df.columns = ['审核场次', '审核日期', '问题描述', '问题类别', '责任人', 
                                     '纠正措施', '预计完成日期', '状态']
                detail_df['审核日期'] = detail_df['审核日期'].dt.strftime('%Y-%m-%d')
                detail_df['预计完成日期'] = detail_df['预计完成日期'].dt.strftime('%Y-%m-%d')
                
                # 标记逾期 - 返回与列数相同的列表
                def overdue_marker(row):
                    due = pd.to_datetime(row['预计完成日期'], errors='coerce')
                    if pd.notna(due) and due < today:
                        return ['background-color: #FFCCBC'] * len(row)  # 逾期 - 浅红
                    elif row['状态'] == 'On-going':
                        return ['background-color: #FFE0B2'] * len(row)  # 进行中 - 浅橙
                    return [''] * len(row)
                
                st.dataframe(
                    detail_df.style.apply(overdue_marker, axis=1),
                    use_container_width=True,
                    hide_index=True
                )
        
        # 汇总表格
        st.markdown("<div class='sub-header'>汇总列表</div>", unsafe_allow_html=True)
        
        summary_open = filtered_open[['audit_name', '问题描述', '问题类别', '责任人', 'DueDate', 'Status']].copy()
        summary_open = summary_open.sort_values('DueDate')
        summary_open.columns = ['审核场次', '问题描述', '问题类别', '责任人', '预计完成日期', '状态']
        
        st.dataframe(summary_open, use_container_width=True, hide_index=True)
    
    else:
        st.success("🎉 恭喜！所有审核发现项已全部关闭！")

# ==================== 看板底部所有者声明（所有页面通用） ====================
st.markdown("---")
st.markdown("""
<div style="margin-top: 30px; padding: 20px; 
            background: linear-gradient(135deg, #F5F5F5 0%, #EEEEEE 100%);
            border-top: 3px solid #0D47A1;
            border-radius: 8px;
            text-align: center;">
    <div style="font-size: 16px; font-weight: 600; color: #0D47A1; margin-bottom: 10px;">
        📊 2026 年内审看板 - 数据维护与技术支持
    </div>
    <div style="display: inline-block; background-color: #0D47A1; color: white; 
                padding: 8px 20px; border-radius: 20px; 
                font-size: 15px; font-weight: bold; margin-top: 5px;">
        @中国区质量体系及文化宣传团队
    </div>
    <div style="font-size: 12px; color: #757575; margin-top: 12px;">
        数据更新时间：2026-08-26 | 如有数据问题请联系中国区质量体系及文化宣传团队
    </div>
</div>
""", unsafe_allow_html=True)
