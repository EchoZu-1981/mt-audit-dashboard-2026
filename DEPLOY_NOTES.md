# 2026 内审看板 - 部署说明

## ✅ 当前状态

| 项目 | 状态 |
|------|------|
| Streamlit Cloud 部署 | ✅ 已完成 |
| 应用链接 | https://mt-audit-dashboard-2026-qj5xykpms6hjggih9uhro2.streamlit.app/ |
| GitHub 仓库 | EchoZu-1981/mt-audit-dashboard-2026 |

---

## 📋 数据更新流程

### 管理员（你）更新数据

1. **修改 Excel 文件**
   - `2026 Audit Planning_V1_20260821.xlsx` - 审核计划表
   - `2026内审发现项跟进表.xlsx` - 发现项跟进表

2. **提交到 GitHub**
   ```powershell
   # 在 VS Code 终端执行
   git add *.xlsx
   git commit -m "更新数据：2026-08-26"
   git push
   ```

3. **Streamlit Cloud 自动更新**
   - 推送后 1-2 分钟内自动重新部署
   - 所有访问者看到最新数据

### 查看者访问

1. 打开链接：https://mt-audit-dashboard-2026-qj5xykpms6hjggih9uhro2.streamlit.app/
2. 直接查看数据，无需上传文件
3. 可以使用侧边栏筛选功能

---

## 🔗 分享链接

**主链接**：
```
https://mt-audit-dashboard-2026-qj5xykpms6hjggih9uhro2.streamlit.app/
```

**分享模板**：

> 各位同事，
> 
> 2026 年内审数据看板已上线，请访问：
> 
> 🔗 https://mt-audit-dashboard-2026-qj5xykpms6hjggih9uhro2.streamlit.app/
> 
> 功能模块：
> - 📈 总览仪表板 - KPI 指标和整体进度
> - 📋 审核进度 - 时间线和计划明细
> - 🔍 发现项分析 - 问题类别和状态分布
> - ⏱️ 整改时效 - 整改天数统计
> - 📝 开放问题清单 - 待处理问题跟踪
> 
> 数据由 @中国区质量体系及文化宣传团队 维护更新
> 
> 谢谢！

---

## ⚠️ 注意事项

1. **数据文件已上传到 GitHub**
   - Excel 文件包含在内审数据
   - 仓库设为 Public，代码公开但无敏感信息

2. **更新频率**
   - 建议每周更新一次
   - 审核后及时更新发现项

3. **数据持久性**
   - 数据保存在 GitHub，永久有效
   - 用户无需上传文件

---

## 📞 技术支持

如有问题请联系：
- **维护团队**: 中国区质量体系及文化宣传团队
- **开发者**: Zu WeiHong (weihong.zu@mt.com)
