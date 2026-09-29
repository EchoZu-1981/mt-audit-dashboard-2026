# 🚀 Streamlit Cloud 部署指南

## 概述

将 2026 内审看板部署到 Streamlit Cloud，其他人可通过链接直接访问，支持动态筛选和交互。

---

## 📋 完整部署步骤

### 第 1 步：安装 Git

访问 https://git-scm.com/download/win，下载并安装 Git for Windows（默认设置即可）。

### 第 2 步：初始化 Git 仓库

在项目文件夹中打开 PowerShell，执行：

```powershell
git init
git add .
git commit -m "Initial commit: 2026 Internal Audit Dashboard"
```

### 第 3 步：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 填写：
   - **Repository name**: `mt-audit-dashboard-2026`
   - **Description**: 2026 年内审数据看板
   - **Visibility**: 建议 **Private**（保护数据）
3. 点击 **Create repository**

### 第 4 步：推送代码到 GitHub

```powershell
git remote add origin https://github.com/你的用户名/mt-audit-dashboard-2026.git
git branch -M main
git push -u origin main
```

### 第 5 步：部署到 Streamlit Cloud

1. 访问 https://share.streamlit.io/
2. 使用 GitHub 账号登录
3. 点击 **"New app"**
4. 填写配置：
   - **Repository**: 选择 `mt-audit-dashboard-2026`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. 点击 **"Deploy!"**

### 第 6 步：获取分享链接

部署成功后，你会获得 URL：
```
https://mt-audit-dashboard-2026-你的用户名.streamlit.app
```

**直接将这个链接发给其他人即可！** 打开链接就能看到完整的动态看板。

---

## ✨ 功能说明

部署后的看板支持：
- ✅ **动态筛选**：按审核场次、状态筛选数据
- ✅ **交互式图表**：悬停查看详情、点击筛选
- ✅ **多视图切换**：总览/进度/发现项/时效/问题清单
- ✅ **数据刷新**：侧边栏可上传更新文件
- ✅ **数据已内置**：Excel 数据随代码一起部署，无需手动上传

## 🔄 更新代码或数据

```powershell
# 修改代码或更新 data/ 下的 Excel 文件后
git add .
git commit -m "更新描述"
git push
```

Streamlit Cloud 会在 1-2 分钟内自动重新部署。

## ⚠️ 注意事项

- **Private 仓库**需要 Streamlit Cloud 付费计划（$5/月），Public 仓库免费
- `data/` 文件夹包含 Excel 数据，**如数据敏感请设为 Private 仓库**
- 代码本身不含敏感凭证，设为 Public 也是安全的（只是数据文件会公开）
每次访问需要重新上传文件，或者：
- 方案 A：将 Excel 文件上传到 GitHub（不推荐，数据公开）
- 方案 B：集成 SharePoint API（需要 IT 支持）
- 方案 C：使用 Streamlit 的持久化存储（需要付费）

---

## 📞 需要帮助？

如果在部署过程中遇到问题：
1. 检查 Streamlit Cloud 的日志（点击页面顶部的 **Main menu** → **Settings**）
2. 参考 [DEPLOYMENT.md](DEPLOYMENT.md) 获取详细部署指南
3. 联系开发者：Zu WeiHong (weihong.zu@mt.com)

---

## 🎉 部署完成检查清单

- [ ] Git 已安装
- [ ] 本地 Git 仓库已初始化
- [ ] GitHub 仓库已创建
- [ ] 代码已推送到 GitHub
- [ ] Streamlit Cloud 应用已部署
- [ ] 可以通过链接访问
- [ ] 文件上传功能正常
- [ ] 链接已分享给团队成员
