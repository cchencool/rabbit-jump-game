# Rabbit Jump Game 🐰

一个 2D 像素风格的跑酷游戏，主角是一只可以换装的小兔子，支持 Joycon 手柄体感控制和双人模式。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 特性

- 🎮 **2D 像素风格** - 经典复古的游戏画面
- 🐰 **换装系统** - 9 种颜色可选， customization 你的小兔子
- 🎯 **Joycon 体感控制** - 挥动手柄实现跳跃
- 👥 **双人模式** - 同屏双玩家，一起跳跃闯关
- 🌍 **多主题背景** - 草原、海洋、冰川、城市
- 📈 **难度递增** - 关卡推进，障碍速度越来越快

## 🎮 控制说明

| 操作 | 键盘 | Joycon |
|------|------|--------|
| 跳跃 | SPACE / ↑ / W | A 按钮 / 向上挥动 |
| 切换服装 | C | - |
| 选择服装（菜单） | ← → | - |
| 双人模式 | T | - |
| Joycon 模式 | J | - |
| 开始/确认 | ENTER | - |
| 暂停 | ESC | - |

## 🚀 快速开始

### 安装依赖

**Ubuntu/Debian:**
```bash
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-font-dev libsdl2-ttf-dev libsdl2-mixer-dev
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 运行游戏

```bash
# 激活虚拟环境
source venv/bin/activate  # Windows: venv\Scripts\activate

# 运行游戏
python main.py
```

## 📦 打包发布

```bash
pip install pyinstaller
pyinstaller rabbit_jump_game.spec
```

生成的可执行文件在 `dist/` 目录中。

## 🏗️ 项目结构

```
rabbit_jump_game/
├── main.py              # 游戏入口
├── settings.py          # 配置常量
├── requirements.txt     # Python 依赖
├── BUILD.md             # 详细构建说明
├── CLAUDE.md            # 开发指南
├── game/
│   ├── __init__.py
│   └── core.py          # 游戏主类、状态管理
├── player/
│   ├── __init__.py
│   ├── player.py        # 玩家角色类
│   ├── controller.py    # 键盘/Joycon 控制器
│   └── costumes.py      # 换装系统
├── level/
│   ├── __init__.py
│   ├── obstacles.py     # 障碍物生成
│   ├── background.py    # 多主题背景
│   └── difficulty.py    # 难度曲线
├── input/
│   ├── __init__.py
│   └── joycon.py        # Joycon 体感控制
└── assets/              # 美术资源
```

## 🎯 游戏玩法

1. 按 **ENTER** 开始游戏
2. 按 **SPACE/↑/W** 跳跃躲避障碍
3. 每越过一个障碍得 1 分
4. 每 10 分升一级，障碍速度增加
5. 撞到障碍游戏结束

### 菜单功能

- 使用 **← →** 选择服装颜色
- 按 **T** 切换双人模式
- 按 **J** 切换 Joycon 模式

## 🛠️ 开发

```bash
# 克隆仓库
git clone <repository-url>
cd rabbit_jump_game

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行游戏
python main.py
```

## 📝 许可证

MIT License
