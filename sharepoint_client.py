"""
从 Microsoft List (SharePoint) 获取内审发现项数据
"""
import pandas as pd
import requests
from typing import Optional


def fetch_from_sharepoint_list(
    site_url: str,
    list_name: str,
    access_token: Optional[str] = None,
    headers: Optional[dict] = None
) -> pd.DataFrame:
    """
    从 SharePoint List 获取数据
    
    Args:
        site_url: SharePoint site URL
        list_name: List 名称
        access_token: Azure AD access token (如果提供 headers 则忽略)
        headers: 完整的请求 headers (包含 Authorization)
    
    Returns:
        DataFrame 包含 List 数据
    """
    if headers is None and access_token:
        headers = {
            'Accept': 'application/json;odata=verbose',
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json;odata=verbose'
        }
    elif headers is None:
        raise ValueError("需要提供 access_token 或 headers")
    
    # 构建 API URL
    api_url = f"{site_url}/_api/web/lists/getbytitle('{list_name}')/items"
    api_url += "?$select=Title,ID,Modified,Author/Email,Editor/Email&$expand=Author,Editor"
    
    all_items = []
    current_url = api_url
    
    while current_url:
        response = requests.get(current_url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        items = data.get('d', {}).get('results', [])
        all_items.extend(items)
        
        # 检查是否有下一页
        current_url = data.get('d', {}).get('__next', None)
    
    # 转换为 DataFrame
    if not all_items:
        return pd.DataFrame()
    
    df = pd.DataFrame(all_items)
    
    # 清理列名（移除特殊字符）
    df.columns = [str(col).replace(' ', '_').replace('-', '_') for col in df.columns]
    
    return df


def fetch_list_metadata(site_url: str, list_name: str, headers: dict) -> dict:
    """获取 List 的元数据（字段信息）"""
    api_url = f"{site_url}/_api/web/lists/getbytitle('{list_name}')/fields"
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    fields = data.get('d', {}).get('results', [])
    
    return {
        'field_name': [f.get('InternalName', '') for f in fields],
        'display_name': [f.get('Title', '') for f in fields],
        'field_type': [f.get('Type', '') for f in fields]
    }


# ==================== 预配置的 List 信息 ====================
# 用户可以根据实际情况修改
LIST_CONFIG = {
    'site_url': 'https://mt1-my.sharepoint.com/personal/weihong_zu_mt_com',
    'list_name': '2026 Internal Audit Findings Followup',
    # 字段映射：SharePoint List 字段 -> 内部字段名
    'field_mapping': {
        'Title': '问题描述',
        'Audited_x0020_Dept_x002F_Item': '审核场次',  # audited dept./item
        'AuditDate': '审核日期',
        'IssueCategory': '问题类别',
        'QNNumber': 'QN号',
        'Owner': '责任人',
        'CorrectiveAction': '原因分析及纠正措施',
        'DueDate': 'DueDate',
        'Status': 'Status'
    }
}
