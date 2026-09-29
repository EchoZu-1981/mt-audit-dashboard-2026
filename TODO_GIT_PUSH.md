# 🏠 回家后执行 Git Push

## 步骤

### 1. 打开 VS Code
打开这个项目文件夹：
```
C:\Users\zu-5\OneDrive - Mettler Toledo LLC\05 QMS Projects\20 QM AI Assistant Agency\Internal audit dashboard
```

### 2. 打开终端
按 `` Ctrl + ` `` 或点击 **终端 → 新终端**

### 3. 执行推送

```powershell
$env:PATH = "$env:LOCALAPPDATA\Programs\Git\bin;$env:PATH"
git push
```

### 4. 如遇认证提示
如果弹出浏览器要求 GitHub 认证，点击授权即可。

### 5. 验证成功
看到类似输出表示成功：
```
To https://github.com/EchoZu-1981/mt-audit-dashboard-2026.git
   2c3ef3c..ae62e1b  main -> main
```

### 6. 等待 Streamlit 自动更新
推送成功后，等待 **1-2 分钟**，Streamlit Cloud 会自动重新部署。

### 7. 验证部署
访问：
```
https://mt-audit-dashboard-2026-qj5xykpms6hjggih9uhro2.streamlit.app/
```

如果看到完整数据（KPI 卡片、图表等），说明部署成功！✅

---

## 📊 待推送内容

| 文件 | 说明 |
|------|------|
| `2026 Audit Planning_V1_20260821.xlsx` | 审核计划表 |
| `2026内审发现项跟进表.xlsx` | 发现项跟进表 |
| `app.py` | 代码更新（移除 st.stop） |
| `DEPLOY_NOTES.md` | 部署说明 |

---

## 🔗 分享链接

部署成功后，分享这个链接给团队：

```
https://mt-audit-dashboard-2026-qj5xykpms6hjggih9uhro2.streamlit.app/
```

---

## 📝 后续更新数据

每次更新 Excel 数据后：

```powershell
git add *.xlsx
git commit -m "更新数据：日期"
git push
```

Streamlit Cloud 会自动更新。
