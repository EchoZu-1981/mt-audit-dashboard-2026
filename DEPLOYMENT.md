# 2026 内审看板 - SharePoint 部署指南

## 📋 概述

本指南帮助你将内审看板部署到部门的 SharePoint 网站，确保有网站访问权限的人都能看到数据。

**目标网站**: https://mt1.sharepoint.com/sites/cn_pct/SitePages/ISO9001-Internal-audit-2021.aspx

---

## 🚀 部署方案（推荐：Streamlit Cloud + SharePoint 嵌入）

### 方案一：Streamlit Community Cloud（免费，推荐）

#### 步骤 1: 创建 GitHub 仓库

```bash
# 1. 在当前目录初始化 Git 仓库
git init
git add .
git commit -m "Initial commit: 2026 Internal Audit Dashboard"

# 2. 在 GitHub 上创建新仓库（例如：mt-internal-audit-dashboard）
# 3. 推送代码
git remote add origin https://github.com/your-username/mt-internal-audit-dashboard.git
git branch -M main
git push -u origin main
```

#### 步骤 2: 创建 `requirements.txt`

项目根目录已包含依赖文件，确保内容如下：

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
openpyxl>=3.1.0
```

#### 步骤 3: 部署到 Streamlit Cloud

1. 访问 https://share.streamlit.io/
2. 点击 **"New app"**
3. 连接 GitHub 账号
4. 选择你的仓库和 `app.py` 文件
5. 点击 **"Deploy!"**

部署成功后会获得一个公开 URL，例如：
`https://mt-internal-audit-dashboard.streamlit.app`

#### 步骤 4: 嵌入到 SharePoint 页面

1. 登录 SharePoint 网站：https://mt1.sharepoint.com/sites/cn_pct
2. 导航到 **ISO9001-Internal-audit-2021.aspx** 页面
3. 点击页面上的 **"+"** 添加新部件
4. 选择 **"Embed"**（嵌入）部件
5. 粘贴 Streamlit Cloud 的 URL
6. 调整部件大小（建议宽度：全宽，高度：800px）
7. 保存页面

---

### 方案二：Azure App Service（企业级，需要 IT 支持）

#### 优点
- 使用公司 Azure AD 认证，只有内部员工可访问
- 数据安全，符合公司合规要求
- 可与 SharePoint 权限集成

#### 步骤

1. **联系 IT 部门**申请 Azure App Service 实例
2. **配置 Azure AD 认证**
3. **部署 Python 应用**到 App Service
4. **在 SharePoint 中嵌入**或使用 Power BI 集成

---

### 方案三：Power BI 集成（最佳企业方案）

如果公司有 Power BI Premium：

1. 将数据导入 Power BI Dataset
2. 使用 Power BI 创建相同的仪表板
3. 发布到 Power BI Service
4. 通过 **"Power BI"** 部件嵌入到 SharePoint

---

## 🔐 数据更新方式

### 方式 1: 上传 Excel 文件（当前实现）

用户通过侧边栏的 **"📁 上传文件"** 按钮上传更新的 Excel 文件。

**限制**：数据只保存在浏览器 session 中，刷新后丢失。

### 方式 2: 持久化数据存储（推荐）

修改 `app.py`，将上传的文件保存到 SharePoint Document Library：

```python
# 在 app.py 中添加
import os

# 数据文件存储路径（部署到服务器后修改）
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

PLANNING_FILE = os.path.join(DATA_DIR, 'audit_planning.xlsx')
FINDINGS_FILE = os.path.join(DATA_DIR, 'audit_findings.xlsx')
```

### 方式 3: 直接从 Microsoft List 拉取（自动化）

需要配置：
1. Azure AD App Registration
2. 授予 List 读取权限
3. 使用 `sharepoint_client.py` 中的 API

---

## 📁 项目文件结构

```
Internal audit dashboard/
├── app.py                    # Streamlit 主应用
├── data_loader.py            # 数据加载和清洗模块
├── sharepoint_client.py      # SharePoint API 客户端
├── requirements.txt          # Python 依赖
├── 2026 Audit Planning_V1_20260821.xlsx   # 审核计划表
├── 2026内审发现项跟进表.xlsx              # 发现项跟进表
└── DEPLOYMENT.md             # 本文件
```

---

## ⚙️ 配置说明

### 修改数据文件路径

如果部署到服务器，修改 `app.py` 中的路径：

```python
# 原路径（本地）
base_dir = r"C:\Users\zu-5\OneDrive...\Internal audit dashboard"

# 修改为相对路径（部署后）
base_dir = os.path.dirname(os.path.abspath(__file__))
```

### 修改审核场次映射

编辑 `data_loader.py` 中的 `FINDING_TO_PLAN_MAP` 字典，添加新的审核场次。

---

## 📞 支持

如有问题，请联系：
- **开发者**: Zu WeiHong (weihong.zu@mt.com)
- **IT 支持**: 联系 MT China IT Helpdesk

---

## 📝 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-08-26 | 1.0 | 初始版本，包含 5 个视图页面 |
| 2026-08-26 | 1.1 | 添加文件上传、数据刷新功能 |
| 2026-08-26 | 1.2 | 突出显示中国区质量体系与文化宣传团队 |
