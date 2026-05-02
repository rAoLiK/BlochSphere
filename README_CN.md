# 布洛赫球 — 交互式单量子比特门演化演示

**基于布洛赫球的量子态与门操作交互式 3D 可视化工具。**

技术栈：Streamlit + QuTiP + Three.js

## 功能特性

- **3D 布洛赫球**：支持旋转、缩放、平移交互
- **量子态矢量**：门操作下平滑动画演化
- **轨迹弧线**：记录并展示量子态在球面上的演化路径
- **支持门类型**：X, Y, Z（泡利门）、H（阿达马门）、Rx, Ry, Rz（参数化旋转门）
- **初始态选择**：|0⟩、|1⟩、|+⟩
- **实时数据显示**：狄拉克符号、测量概率、布洛赫坐标
- **复古未来主义界面**：黑橙配色、CRT 扫描线效果、等宽字体排版

## 快速开始

### 环境要求

- [Miniforge](https://github.com/conda-forge/miniforge) 或 Anaconda
- Git

### 安装运行

**Linux / WSL:**
```bash
bash env/setup.sh
conda activate bloch
streamlit run app.py
```

**Windows:**
```cmd
env\setup.bat
conda activate bloch
streamlit run app.py
```

浏览器访问 http://localhost:8501

## 使用说明

1. 从侧边栏选择**初始态**（|0⟩、|1⟩ 或 |+⟩）
2. 选择**量子门**（X, Y, Z, H, Rx, Ry, Rz）
3. 对于旋转门（Rx/Ry/Rz），使用滑块设置**旋转角度**
4. 点击 **APPLY** 执行门操作并观看动画
5. 使用**鼠标**拖拽旋转 3D 视图，滚轮缩放
6. 使用球体下方的**动画控件**控制播放

## 项目结构

```
bloch/
├── app.py                    # Streamlit 主程序入口
├── quantum/                  # 量子后端 (QuTiP)
│   ├── state.py              # BlochState 量子态类
│   ├── gates.py              # 量子门定义
│   └── evolution.py          # 动画帧生成
├── ui/                       # Streamlit UI 组件
│   ├── styles.py             # 复古未来主义 CSS 样式
│   ├── controls.py           # 侧边栏控件
│   └── display.py            # 状态信息展示
├── visualization/            # 3D 渲染
│   └── scene.py              # Three.js 场景构建器
├── env/                      # Conda 环境配置
│   ├── environment.yml
│   ├── setup.sh
│   └── setup.bat
├── report/                   # 学术报告
└── README_CN.md              # 本文件
```

## 技术细节

- **量子后端**：使用 QuTiP 进行量子态表示与门操作计算
- **3D 渲染**：Three.js（CDN 加载）通过 `st.components.html()` 嵌入 Streamlit
- **动画机制**：通过分步旋转门操作插值生成动画帧，JavaScript 实时渲染
- **界面样式**：自定义 CSS，JetBrains Mono 字体，黑橙配色方案

## 需求清单

- [x] 交互式 3D 布洛赫球可视化
- [x] 泡利门（X, Y, Z）支持
- [x] 阿达马门（H）支持
- [x] 参数化旋转门（Rx, Ry, Rz）含角度滑块
- [x] 平滑 3D 动画与轨迹弧线
- [x] 实时状态数据显示
- [x] 跨平台运行（Windows + Linux）
- [x] Conda 环境管理
- [x] Git 版本控制

## 屏幕截图

## Screen shot

![ScreenShot](./fig/ScreenShot.png)