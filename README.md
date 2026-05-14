# Rabbit Jump Game 🐰

一个 2D 像素风格的跑酷游戏，主角是一只可以换装的小兔子，支持 Joycon 手柄体感控制和双人模式。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 特性

-  **2D 像素风格** - 经典复古的游戏画面
- 🐰 **换装系统** - 9 种颜色可选，customization 你的小兔子
- 🎯 **Joycon 体感控制** - 挥动手柄实现跳跃
- 👥 **双人模式** - 同屏双玩家，一起跳跃闯关
- 🌍 **多主题背景** - 草原、海洋、冰川、城市
- 🌤️ **动态天气系统** - 7 种天气随机切换（晴天/多云/阴天/大雾/雨天/下雪/花瓣）
- ⚡ **5 档速度调节** - 游戏过程中实时调整速度（1.0x ~ 3.0x）
- 🛡️ **护盾系统** - 拾取金币获得无敌护盾，可撞碎障碍物
-  **Debug 模式** - 实时显示帧率和帧率曲线
-  **难度递增** - 关卡推进，障碍速度越来越快

## 🎮 控制说明

### 键盘控制

| 操作 | 按键 |
|------|------|
| 跳跃 | SPACE / ↑ / W |
| 切换服装 | C |
| 选择服装（菜单） | ← → |
| 双人模式 | T |
| Joycon 模式 | J |
| 练习模式 | P |
| Debug 模式 | D |
| 加速 | + |
| 减速 | - |
| 开始/确认 | ENTER |
| 暂停 | ESC |
| 退出确认 | Q |

### Joycon 控制

| 操作 | Joycon |
|------|--------|
| 跳跃 | A 按钮 / 向上挥动 |

## 🌤️ 天气系统

游戏过程中会随机出现以下天气，每种天气持续 20-40 秒：

- ☀️ **晴天** - 阳光明媚
- ☁️ **多云** - 轻微变暗
- 🌥️ **阴天** - 浓云蔽日，多层厚云遮挡阳光
- 🌫️ **大雾** - 动态雾气效果，雾气粒子缓慢移动
- 🌧️ **雨天** - 蓝色雨滴斜向飘落
- ️ **下雪** - 白色雪花缓慢飘落，带左右摇摆
- 🌸 **花瓣** - 粉色花瓣旋转飘落

天气切换时有淡入淡出过渡效果。

##  速度调节

游戏过程中可以实时调整速度，共 5 档：

| 档位 | 倍率 | 说明 |
|------|------|------|
| 1 | 1.0x | 正常速度 |
| 2 | 1.5x | 较快 |
| 3 | 2.0x | 快速 |
| 4 | 2.5x | 很快 |
| 5 | 3.0x | 极速 |

速度调节采用"快放"效果，所有运动元素（背景、障碍物、道具）按比例加速，但兔子的跳跃物理（重力、跳跃力度）保持不变，确保跳跃高度和水平距离在所有倍率下一致。

## 🛡️ 护盾系统

- 拾取金币获得 10 秒无敌护盾
- 护盾状态下撞击障碍物会将其撞碎
- 障碍物被撞碎后会向上旋转飞出屏幕
- 护盾撞击有独特的破坏音效

## 🎨 Debug 模式

按 **D** 键切换 Debug 模式，显示：
- 当前 FPS
- 平均 FPS
- 最低/最高 FPS
- 实时帧率曲线图

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
── main.py              # 游戏入口
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
│   ── costumes.py      # 换装系统
── level/
│   ├── __init__.py
│   ├── obstacles.py     # 障碍物生成
│   ├── background.py    # 多主题背景
│   ├── difficulty.py    # 难度曲线
│   └── weather.py       # 天气系统
├── input/
│   ├── __init__.py
│   └── joycon.py        # Joycon 体感控制
└── assets/              # 美术资源
```

##  游戏玩法

1. 按 **ENTER** 开始游戏
2. 按 **SPACE/↑/W** 跳跃躲避障碍
3. 每越过一个障碍得 1 分
4. 每 10 分升一级，障碍速度增加
5. 撞到障碍游戏结束

### 菜单功能

- 使用 **← →** 选择服装颜色
- 按 **T** 切换双人模式
- 按 **J** 切换 Joycon 模式
- 按 **P** 切换练习模式（无敌）
- 按 **D** 切换 Debug 模式

### 游戏内功能

- 按 **C** 切换服装
- 按 **+/-** 调整速度
- 按 **ESC** 暂停

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
