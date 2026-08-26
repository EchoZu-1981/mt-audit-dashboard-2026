# 🚀 Streamlit Cloud 部署步骤

## ✅ 已完成准备

项目已经准备好部署到 Streamlit Cloud：
- ✅ `requirements.txt` - 依赖清单
- ✅ `README.md` - 项目说明
- ✅ `.gitignore` - 排除 Excel 文件和本地缓存
- ✅ `app.py` - 支持无本地文件运行（通过上传功能）

---

## 📋 部署步骤

### 第 1 步：安装 Git（如果未安装）

1. 访问 https://git-scm.com/download/win
2. 下载并安装 Git for Windows
3. 使用默认设置安装即可

### 第 2 步：初始化 Git 仓库

在 VS Code 终端中执行：

```powershell
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 2026 Internal Audit Dashboard"
```

### 第 3 步：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 填写：
   - **Repository name**: `mt-audit-dashboard-2026`（或其他名字）
   - **Description**: 2026 年内审数据看板
   - **Visibility**: ⚠️ 建议选 **Private**（私有，保护数据）
3. 点击 **Create repository**

### 第 4 步：推送代码到 GitHub

根据 GitHub 提示执行：

```powershell
# 添加远程仓库（替换 your-username 为你的 GitHub 用户名）
git remote add origin https://github.com/your-username/mt-audit-dashboard-2026.git

# 重命名主分支
git branch -M main

# 推送到 GitHub
git push -u origin main
```

### 第 5 步：部署到 Streamlit Cloud

1. 访问 https://share.streamlit.io/
2. 点击 **"New app"** 或使用 GitHub 登录
3. 授权 Streamlit 访问 GitHub
4. 填写部署配置：
   - **Repository**: 选择 `mt-audit-dashboard-2026`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. 点击 **"Deploy!"**

### 第 6 步：获取分享链接

部署成功后，你会获得一个类似这样的 URL：
```
https://mt-audit-dashboard-2026-your-username.streamlit.app
```

### 第 7 步：首次使用

1. 打开部署后的链接
2. 点击侧边栏的 **"📁 上传文件"**
3. 上传两个 Excel 文件：
   - 审核计划表
   - 发现项跟进表
4. 数据将自动加载并显示

---

## 🔄 更新代码

当你修改代码后：

```powershell
# 添加修改的文件
git add .

# 提交
git commit -m "描述你的修改"

# 推送
git push
```

Streamlit Cloud 会自动重新部署（通常 1-2 分钟内完成）。

---

## ⚠️ 注意事项

### 1. 数据安全
- Excel 文件**不会**上传到 GitHub（已在 `.gitignore` 中排除）
- 用户通过上传功能加载数据
- 数据只保存在浏览器 session 中，不会持久化

### 2. 仓库可见性
- **Private 仓库**：需要 Streamlit Cloud 付费计划（$5/月）
- **Public 仓库**：免费，但代码公开可见
- 建议：代码本身不包含敏感数据，可以设为 Public

### 3. 数据更新
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
