# exercise_python

这是一个 Python 练习仓库。

我会在这里记录学习过程中写的小脚本和练习项目，包括自动化脚本和实用工具。

## 项目示例

### 1. 自动化 12306 查询脚本
- 使用 Selenium + Pytest 自动化查询火车票
- 支持单程、往返、中转等多种查询场景
- 自动截图保存查询结果
- 脚本路径：`school/12306.py`
- 简单、易用，适合作为初学者练习自动化测试的入门项目

### 2. 携程 (Ctrip) 自动化脚本
- 使用 Selenium + Pytest 自动化查询携程火车票
- 支持往返票、动车/高铁、不同出发地和目的地
- 自动截图保存查询结果
- 脚本路径：`school/XC.py`
- 页面元素复杂，逻辑多样，是高级练习项目

## 使用说明
1. 克隆仓库到本地
2. 安装依赖：
```bash
pip install selenium pytest

确保 ChromeDriver 路径正确
使用 Pytest 运行测试脚本：
pytest school/12306.py
pytest school/XC.py

欢迎大家提出建议
