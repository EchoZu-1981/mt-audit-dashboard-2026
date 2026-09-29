@echo off
chcp 65001 >nul
echo ========================================
echo   2026 内审看板 - 启动程序
echo ========================================
echo.

REM 检查是否有虚拟环境
if exist ".venv\Scripts\python.exe" (
    echo 使用本地虚拟环境启动...
    .venv\Scripts\python.exe -m streamlit run app.py
) else (
    echo 未找到虚拟环境，尝试使用系统 Python...
    python -m streamlit run app.py
    if errorlevel 1 (
        echo.
        echo ========================================
        echo 错误：未找到 Python 或 streamlit
        echo.
        echo 请先运行 setup.bat 安装依赖
        echo ========================================
        pause
        exit /b 1
    )
)
