# 2026 内审看板

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 📊 项目简介

这是一个基于 Streamlit 的交互式内审数据看板，用于跟踪 2026 年内审进度和审核发现项。

**维护团队**: @中国区质量体系及文化宣传团队

## 🚀 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app.py
```

### 数据准备

将以下 Excel 文件放在项目根目录：
- `2026 Audit Planning_V1_20260821.xlsx` - 审核计划表
- `2026内审发现项跟进表.xlsx` - 发现项跟进表

或者通过应用侧边栏的 **"📁 上传文件"** 功能上传。

## 📋 功能特性

### 1. 总览仪表板
- KPI 指标卡（审核总数、完成率、发现项统计）
- 审核完成进度饼图
- 发现项状态分布
- 各部门审核发现项数量对比
- 各部门整改完成率
- 各部门整改时效对比

### 2. 审核进度
- 审核时间线甘特图
- 审核计划明细表

### 3. 发现项分析
- 问题类别分布
- 问题状态分布
- 各部门问题类型对比
- 发现项明细表

### 4. 整改时效
- 中位数/平均整改天数
- 整改时效箱线图
- 各部门整改效率对比

### 5. 开放问题清单
- 待处理问题筛选
- 逾期问题预警
- 问题跟踪明细

## 🎨 技术栈

- **Streamlit** - Web 应用框架
- **Pandas** - 数据处理
- **Plotly** - 数据可视化
- **OpenPyXL** - Excel 文件读取

## 📁 项目结构

```
Internal audit dashboard/
├── app.py                    # Streamlit 主应用
├── data_loader.py            # 数据加载和清洗模块
├── sharepoint_client.py      # SharePoint API 客户端（可选）
├── requirements.txt          # Python 依赖
├── README.md                 # 本文件
├── DEPLOYMENT.md             # 部署指南
└── .gitignore               # Git 忽略文件
```

## 🔧 配置

### 修改审核场次映射

编辑 `data_loader.py` 中的 `FINDING_TO_PLAN_MAP` 字典：

```python
FINDING_TO_PLAN_MAP = {
    "你的审核场次名": {
        "plan_id": "MTCN-2026-XXX",
        "audit_name": "显示名称",
        "lead_auditor": "主审人"
    },
    # ... 更多场次
}
```

## 🌐 部署

### Streamlit Cloud（推荐）

1. 将代码推送到 GitHub 仓库
2. 访问 [share.streamlit.io](https://share.streamlit.io/)
3. 点击 **New app**
4. 选择你的仓库和 `app.py`
5. 点击 **Deploy!**

详细步骤请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

### SharePoint 嵌入

部署到 Streamlit Cloud 后，可以在 SharePoint 页面通过 **Embed** 部件嵌入看板。

## 📝 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-08-26 | 1.0 | 初始版本，包含 5 个视图页面 |
| 2026-08-26 | 1.1 | 添加文件上传、数据刷新功能 |
| 2026-08-26 | 1.2 | 添加看板所有者声明 |
| 2026-08-26 | 1.3 | 支持 Streamlit Cloud 部署（无本地文件也可运行） |

## 👥 联系方式

如有问题或建议，请联系：
- **维护团队**: 中国区质量体系及文化宣传团队
- **开发者**: Zu WeiHong (weihong.zu@mt.com)

## 📄 许可证

内部使用，© 2026 Mettler-Toledo LLC
