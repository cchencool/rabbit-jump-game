# 打包发布配置

## 本地开发

### Linux (Ubuntu/Debian)

```bash
# 安装系统依赖
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-font-dev libsdl2-ttf-dev libsdl2-mixer-dev

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装 Python 依赖
pip install -r requirements.txt

# 运行游戏
python main.py
```

### Windows

```bash
# 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 运行游戏
python main.py

# 打包
pyinstaller rabbit_jump_game.spec
```

### macOS

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 运行游戏
python main.py

# 打包
pyinstaller rabbit_jump_game.spec
```

## 打包发布

```bash
# 打包
pyinstaller rabbit_jump_game.spec

# 生成的可执行文件在 dist/RabbitJumpGame (macOS/Linux) 或 dist/RabbitJumpGame.exe (Windows)
```

## 跨平台注意事项

1. **Joycon 支持**: 需要确保 hidapi 在目标平台正确安装
2. **Pygame**: 会自动包含必要的 SDL 库
3. **资源文件**: assets 目录会自动打包到可执行文件

## 优化建议

- 使用 `--onefile` 打包成单个可执行文件
- 使用 `--windowed` 隐藏控制台窗口（已配置）
- 添加游戏图标：在 spec 文件中配置 `icon='icon.ico'`
