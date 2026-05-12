# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Rabbit Jump Game - 一个 2D 像素风格的跑酷游戏，主角是一只可以换装的小兔子，支持 Joycon 手柄体感控制和双人模式。

## Architecture

### 技术栈
- **游戏引擎**: Pygame
- **语言**: Python 3.8+
- **手柄支持**: pygame joystick 模块 / hidapi
- **打包工具**: PyInstaller

### 核心模块
- **game/** - 游戏核心（主循环、状态机、碰撞检测）
- **player/** - 玩家系统（角色、换装、输入控制）
- **level/** - 关卡系统（障碍物、背景、难度曲线）
- **input/** - Joycon 手柄集成（陀螺仪体感）

### 项目结构
```
rabbit_jump_game/
├── main.py              # 游戏入口
├── settings.py          # 配置常量
├── pyproject.toml       # uv 项目配置
├── uv.lock              # 依赖锁定文件
├── requirements.txt     # 依赖（备用）
├── BUILD.md             # 打包发布说明
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
│   ├── obstacles.py     # 障碍物生成和管理
│   ├── background.py    # 多主题背景
│   └── difficulty.py    # 难度曲线
├── input/
│   ├── __init__.py
│   └── joycon.py        # Joycon 体感控制
└── assets/              # 美术资源
```

## Commands

### 使用 uv（推荐）

```bash
# 首次设置 - 创建虚拟环境并安装依赖
uv sync

# 运行游戏
uv run python main.py

# 添加新依赖
uv add <package>

# 更新依赖
uv lock --upgrade

# 同步依赖（与 lock 文件保持一致）
uv sync

# 安装开发依赖
uv sync --group dev

# 查看已安装的包
uv pip list
```

### 使用 requirements.txt（备用）

```bash
# 安装依赖
pip install -r requirements.txt

# 运行游戏
python main.py
```

## Controls

- **移动**: SPACE / ↑ / W - 跳跃
- **换装**: C - 切换服装颜色
- **菜单**: ← → - 选择服装，T - 切换双人模式，J - 切换 Joycon 模式
- **暂停**: ESC
- **开始/重新开始**: ENTER

## Key Features

1. **Joycon 体感控制** - 通过陀螺仪感应向上挥动实现跳跃
2. **换装系统** - 9 种颜色可选（默认、蓝、绿、黄、紫、橙、粉、黑、白、金）
3. **双人模式** - 同屏双玩家，第二个玩家自动跟随跳跃
4. **多主题背景** - 草原、海洋、冰川、城市（Background 类支持切换）
5. **难度递增** - 每 10 分升一级，障碍速度增加

## Development Notes

- 像素美术建议规格：角色 32x32 或 64x64
- Joycon 通过蓝牙连接，pygame.joystick 读取输入
- 双人模式为同屏设计，非分屏
- 跨平台目标：Windows、macOS
- 地面 Y 坐标：`GROUND_Y = SCREEN_HEIGHT - 80`
