@echo off
chcp 65001 >nul
echo ========================================
echo   2026 内审看板 - 环境安装
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python！
    echo.
    echo 请先安装 Python 3.10 或更高版本：
    echo https://www.python.org/downloads/
    echo.
    echo 安装时请勾选 "Add Python to PATH"
    echo ========================================
    pause
    exit /b 1
)

echo [1/3] 检查 Python 版本...
python --version
echo.

echo [2/3] 创建虚拟环境...
python -m venv .venv
if errorlevel 1 (
    echo [错误] 创建虚拟环境失败！
    pause
    exit /b 1
)
echo 虚拟环境创建成功！
echo.

echo [3/3] 安装依赖包...
.venv\Scripts\pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 安装依赖失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 现在可以双击 run.bat 启动看板
echo 看板会自动在浏览器中打开
echo.
pause
