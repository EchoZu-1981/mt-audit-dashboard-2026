"""
数据加载、清洗、映射模块
"""
import pandas as pd
import os

# ==================== 审核场次 ↔ 计划编号 映射表 ====================
# 根据实际数据建立的映射关系
FINDING_TO_PLAN_MAP = {
    # S01: Module D / VCAP专项审核 for MTCT&MTCZ
    "Module D&VCAP_MTCT": {"plan_id": "MTCN-2026-S01", "audit_name": "Module D/VCAP (MTCT)", "lead_auditor": "Lai YaRu"},
    "Module D&VCAP_MTCZ": {"plan_id": "MTCN-2026-S01", "audit_name": "Module D/VCAP (MTCZ)", "lead_auditor": "Lai YaRu"},
    
    # S03: MTCS防爆专项审核
    "MTCS 防爆专项内审": {"plan_id": "MTCN-2026-S03", "audit_name": "MTCS防爆专项", "lead_auditor": "Liu YuChun"},
    
    # S04: POIND-VEH
    "POIND-VEH": {"plan_id": "MTCN-2026-S04", "audit_name": "POIND-VEH", "lead_auditor": "Zhou Xue"},
    
    # S05: ASBU
    "ASBU": {"plan_id": "MTCN-2026-S05", "audit_name": "ASBU", "lead_auditor": "Shi ZhiDan"},
    
    # S06: 中心仓库（外仓）
    "CDC": {"plan_id": "MTCN-2026-S06", "audit_name": "中心仓库(CDC)", "lead_auditor": "Zu WeiHong"},
    
    # S07: MTCD
    "MTCD": {"plan_id": "MTCN-2026-S07", "audit_name": "MTCD", "lead_auditor": "Zu WeiHong"},
    
    # S08: SCM
    "SCM": {"plan_id": "MTCN-2026-S08", "audit_name": "SCM", "lead_auditor": "Xie Lin"},
    
    # S09: POPI
    "POPI": {"plan_id": "MTCN-2026-S09", "audit_name": "POPI", "lead_auditor": "Lu GuoQiang"},
    
    # S11: POIND (excluded VEH) 研发+RT研发
    "POIND研发-IW": {"plan_id": "MTCN-2026-S11", "audit_name": "POIND研发-IW", "lead_auditor": "Shi ZhiDan"},
    "POIND研发-S&I": {"plan_id": "MTCN-2026-S11", "audit_name": "POIND研发-S&I", "lead_auditor": "Shi ZhiDan"},
    "POIND研发-T&L": {"plan_id": "MTCN-2026-S11", "audit_name": "POIND研发-T&L", "lead_auditor": "Shi ZhiDan"},
    "PORT研发": {"plan_id": "MTCN-2026-S11", "audit_name": "PORT研发", "lead_auditor": "Shi ZhiDan"},
    
    # S12: POIND (excluded VEH) 运营&质量
    "POIND运营&质量(exc.VEH)": {"plan_id": "MTCN-2026-S12", "audit_name": "POIND运营&质量", "lead_auditor": "Wang B"},
    
    # S14: MTCS (研发&运营&质量&采购)
    "MTCS": {"plan_id": "MTCN-2026-S14", "audit_name": "MTCS综合", "lead_auditor": "Wu DuanZi"},
    
    # S16: AP-HUB
    "AP-HUB": {"plan_id": "MTCN-2026-S16", "audit_name": "AP-HUB", "lead_auditor": "Wu DuanZi"},
    
    # S17: MTCT2-POLC
    "MTCT2-POLC研发&运营（含OEM）": {"plan_id": "MTCN-2026-S17", "audit_name": "MTCT2-POLC", "lead_auditor": "Lai YaRu"},
    
    # S19: POQM - 中国区质量体系与文化宣传团队
    "POQM": {"plan_id": "MTCN-2026-S19", "audit_name": "POQM", "lead_auditor": "Xie Ting"},
    
    # S02: Module D / VCAP专项审核 for MTCS
    "Module D&VCAP Audit_MTCS": {"plan_id": "MTCN-2026-S02", "audit_name": "Module D/VCAP (MTCS)", "lead_auditor": "Xie Lin"},
    
    # S24: MTCS PLM+实验室专项审核
    "MTCS PLM+实验室专项审核": {"plan_id": "MTCN-2026-S24", "audit_name": "MTCS PLM+实验室", "lead_auditor": "Wu DuanZi"},
}

# 计划表中的月份列映射
MONTH_COLUMNS = {
    "J": "Jan", "F": "Feb", "M_1": "Mar", "A_1": "Apr",
    "M_2": "May", "J_2": "Jun", "J_3": "Jul", "A_2": "Aug",
    "S": "Sep", "O": "Oct", "N": "Nov", "D": "Dec"
}


def load_planning_data(filepath):
    """加载内审计划表 Planning sheet"""
    xl = pd.ExcelFile(filepath)
    df = pd.read_excel(xl, sheet_name='Planning', header=1)
    
    # 重命名列
    df.columns = ['seq', 'audit_no', 'audit_area', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                  'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'lead_auditor', 'co_auditor',
                  'plan_created', 'report_communicated', 'closed_ncs', 'open_ncs', 'remarks']
    
    # 过滤有效行（删除空行和汇总行）
    df = df.dropna(subset=['audit_no'])
    df = df[df['audit_no'].str.contains('MTCN', na=False)].copy()
    
    # 确定计划月份和完成状态
    month_cols = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    df['plan_month'] = ''
    df['status'] = 'Planned'
    
    for idx, row in df.iterrows():
        for i, col in enumerate(month_cols):
            val = str(row[col]).strip() if pd.notna(row[col]) else ''
            if val == 'P':
                df.at[idx, 'plan_month'] = month_names[i]
                df.at[idx, 'status'] = 'Planned'
            elif val == '✅' or val == '✓':
                df.at[idx, 'plan_month'] = month_names[i]
                df.at[idx, 'status'] = 'Completed'
    
    # 根据 Plan created 和 Report communicated 更新状态
    df.loc[(df['plan_created'] == 'X') & (df['report_communicated'] == 'X'), 'status'] = 'Completed'
    
    # 清理数值列
    for col in ['closed_ncs', 'open_ncs']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df


def load_findings_data(filepath):
    """加载内审发现项跟进表"""
    df = pd.read_excel(filepath, sheet_name='query')
    
    # 转换日期列（发现日期 = 审核日期）
    df['发现日期'] = pd.to_datetime(df['发现日期'], errors='coerce')
    df['DueDate'] = pd.to_datetime(df['DueDate'], errors='coerce')
    
    # 添加映射信息
    df['plan_id'] = df['审核场次'].map(lambda x: FINDING_TO_PLAN_MAP.get(x, {}).get('plan_id', 'Unmapped'))
    df['audit_name'] = df['审核场次'].map(lambda x: FINDING_TO_PLAN_MAP.get(x, {}).get('audit_name', x))
    df['lead_auditor'] = df['审核场次'].map(lambda x: FINDING_TO_PLAN_MAP.get(x, {}).get('lead_auditor', 'N/A'))
    
    # 计算整改天数 (DueDate - 发现日期)
    df['整改天数'] = (df['DueDate'] - df['发现日期']).dt.days
    
    # 标准化 Status
    df['Status'] = df['Status'].str.strip()
    
    return df


def compute_department_stats(findings_df):
    """计算各部门统计指标"""
    stats = []
    
    for audit, group in findings_df.groupby('audit_name'):
        total = len(group)
        nc_count = len(group[group['问题类别'] == '一般不符合'])
        oi_count = len(group[group['问题类别'] == '改进建议项'])
        closed = len(group[group['Status'] == 'Closed'])
        ongoing = len(group[group['Status'] == 'On-going'])
        open_count = len(group[group['Status'] == 'Open'])
        
        # 整改天数统计（仅 Closed 项）
        closed_days = group[group['Status'] == 'Closed']['整改天数'].dropna()
        median_days = closed_days.median() if len(closed_days) > 0 else None
        mean_days = closed_days.mean() if len(closed_days) > 0 else None
        
        # 所有项的预计整改天数
        all_days = group['整改天数'].dropna()
        median_due = all_days.median() if len(all_days) > 0 else None
        
        stats.append({
            'audit_name': audit,
            'plan_id': group['plan_id'].iloc[0],
            'lead_auditor': group['lead_auditor'].iloc[0],
            'total_findings': total,
            'nc_count': nc_count,
            'oi_count': oi_count,
            'closed': closed,
            'ongoing': ongoing,
            'open': open_count,
            'completion_rate': round(closed / total * 100, 1) if total > 0 else 0,
            'median_days_closed': int(median_days) if median_days else None,
            'mean_days_closed': int(round(mean_days)) if mean_days else None,
            'median_due_days': int(median_due) if median_due else None,
            'audit_date': group['发现日期'].min(),
        })
    
    return pd.DataFrame(stats)


def load_all_data(base_dir):
    """加载所有数据并返回（兼容旧接口）"""
    planning_file = os.path.join(base_dir, '2026 Audit Planning_V1_20260821.xlsx')
    findings_file = os.path.join(base_dir, '2026年内审发现跟进表.xlsx')
    return load_all_data_from_files(planning_file, findings_file)


def load_all_data_from_files(planning_file, findings_file):
    """从指定文件加载所有数据并返回"""
    planning_df = load_planning_data(planning_file)
    findings_df = load_findings_data(findings_file)
    dept_stats = compute_department_stats(findings_df)
    
    return planning_df, findings_df, dept_stats


def load_planning_from_uploaded_file(uploaded_file):
    """从上传的文件加载审核计划数据"""
    df = pd.read_excel(uploaded_file, sheet_name='Planning', header=1)
    
    # 重命名列
    df.columns = ['seq', 'audit_no', 'audit_area', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                  'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'lead_auditor', 'co_auditor',
                  'plan_created', 'report_communicated', 'closed_ncs', 'open_ncs', 'remarks']
    
    # 过滤有效行
    df = df.dropna(subset=['audit_no'])
    df = df[df['audit_no'].str.contains('MTCN', na=False)].copy()
    
    # 确定计划月份和完成状态
    month_cols = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    df['plan_month'] = ''
    df['status'] = 'Planned'
    
    for idx, row in df.iterrows():
        for i, col in enumerate(month_cols):
            val = str(row[col]).strip() if pd.notna(row[col]) else ''
            if val == 'P':
                df.at[idx, 'plan_month'] = month_names[i]
                df.at[idx, 'status'] = 'Planned'
            elif val == '✅' or val == '✓':
                df.at[idx, 'plan_month'] = month_names[i]
                df.at[idx, 'status'] = 'Completed'
    
    # 根据 Plan created 和 Report communicated 更新状态
    df.loc[(df['plan_created'] == 'X') & (df['report_communicated'] == 'X'), 'status'] = 'Completed'
    
    # 清理数值列
    for col in ['closed_ncs', 'open_ncs']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df


def load_findings_from_uploaded_file(uploaded_file):
    """从上传的文件加载发现项数据"""
    df = pd.read_excel(uploaded_file, sheet_name='query')
    
    # 转换日期列
    df['发现日期'] = pd.to_datetime(df['发现日期'], errors='coerce')
    df['DueDate'] = pd.to_datetime(df['DueDate'], errors='coerce')
    
    # 添加映射信息
    df['plan_id'] = df['审核场次'].map(lambda x: FINDING_TO_PLAN_MAP.get(x, {}).get('plan_id', 'Unmapped'))
    df['audit_name'] = df['审核场次'].map(lambda x: FINDING_TO_PLAN_MAP.get(x, {}).get('audit_name', x))
    df['lead_auditor'] = df['审核场次'].map(lambda x: FINDING_TO_PLAN_MAP.get(x, {}).get('lead_auditor', 'N/A'))
    
    # 计算整改天数
    df['整改天数'] = (df['DueDate'] - df['发现日期']).dt.days
    
    # 标准化 Status
    df['Status'] = df['Status'].str.strip()
    
    return df
