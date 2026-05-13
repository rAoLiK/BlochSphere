# 自定义初始态 & 多门串联功能设计文档

## 概述

对 Bloch Sphere 项目进行两项功能扩展：
1. **自定义初始态** — 通过极坐标 (θ, φ) 任意设置初始量子态，保留原有预设选项
2. **多门串联** — 支持多个量子门串联配置、顺序动画播放和最终态展示

两项功能均保持现有的复古未来主义黑橙 UI 风格。

## 功能一：自定义初始态

### 量子力学背景

任意单比特纯态可表示为：
|ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)·sin(θ/2)|1⟩

其中 θ ∈ [0, π] 为极角，φ ∈ [0, 2π] 为方位角。

### UI 方案

在现有 INITIAL STATE 下拉框中增加 "Custom" 选项：
- 选择 |0⟩/|1⟩/|+⟩ 时，行为不变
- 选择 Custom 时，下方出现两个滑块：
  - θ (极角): 0° ~ 180°, 步长 1°, 默认 90°
  - φ (方位角): 0° ~ 360°, 步长 1°, 默认 0°
- 滑块下方显示当前 θ/φ 对应的 Bloch 坐标预览

### 数据流

```
用户选择 Custom → 拖动 θ/φ 滑块
  → controls["initial_state"] == "Custom"
  → controls["custom_theta"], controls["custom_phi"]
  → BlochState(theta=θ, phi=φ)
  → bloch_vector() → 3D 场景更新
```

### 文件变更

#### `quantum/state.py`

`BlochState.__init__` 增加 `theta` 和 `phi` 参数：

```python
def __init__(self, ket=None, label="|0⟩", theta=None, phi=None):
    if ket is not None:
        self.ket = ket
    elif theta is not None and phi is not None:
        # 从极坐标构造
        alpha = np.cos(theta / 2)
        beta = np.exp(1j * phi) * np.sin(theta / 2)
        self.ket = Qobj([[alpha], [beta]])
    elif label == "|0⟩":
        self.ket = basis(2, 0)
    # ... 其余预设不变
```

#### `ui/controls.py`

- `INITIAL_STATES` 增加 `"Custom"`
- `render_controls()` 中，当选中 "Custom" 时渲染两个滑块
- 返回值增加 `custom_theta` 和 `custom_phi` 字段

#### `app.py`

初始态切换逻辑修改：

```python
if controls["initial_state"] == "Custom":
    st.session_state.bloch_state = BlochState(
        theta=controls["custom_theta"],
        phi=controls["custom_phi"],
    )
else:
    if controls["initial_state"] != st.session_state.bloch_state.to_ket_text():
        st.session_state.bloch_state = BlochState(label=controls["initial_state"])
```

---

## 功能二：多门串联

### 概述

在主页面底部新增 MULTI-GATE CHAIN 区域，支持：
- 配置多个量子门的串联序列
- 每个门独立配置（门类型 + 旋转角参数）
- 点击 APPLY 后顺序播放全部门的旋转动画
- 显示最终量子态

与单门模式完全独立运作。

### 页面布局

```
┌──────────────────────────────────────────────────────┐
│  [现有单门模式区域不变]                                │
├──────────────────────────────────────────────────────┤
│  MULTI-GATE CHAIN                                    │
│  ┌─ Gate 1: H ──────────┐  ┌─ Gate 2: Rx(1.57) ───┐ │
│  │ [radio: 门类型]       │  │ [radio: 门类型]       │ │
│  │ [slider: 旋转角]     │  │ [slider: 旋转角]     │ │
│  │ [REMOVE]             │  │ [REMOVE]             │ │
│  └──────────────────────┘  └──────────────────────┘ │
│  [+ ADD GATE]  [APPLY CHAIN]  [RESET CHAIN]         │
│                                                      │
│  FINAL STATE: 0.707|0⟩ + 0.707|1⟩                   │
│  Bloch Vector: (1.0000, 0.0000, 0.0000)             │
└──────────────────────────────────────────────────────┘
```

### 数据结构

Session state 新增：

```python
chain_gates = [
    {"type": "H", "theta": 0.0, "id": "gate_0"},
    {"type": "Rx", "theta": 1.5708, "id": "gate_1"},
]
chain_frames = []           # 预计算的全部帧 (x,y,z) 列表
chain_boundaries = [0, 80]  # 每门帧起始索引
chain_labels = ["H", "Rx"]  # 每门标签
chain_final_state = None    # 最终 BlochState
chain_trigger = 0           # 动画触发计数器
```

### 帧计算

新增 `quantum/evolution.py` 中的函数：

```python
def generate_chain_frames(initial, gates, num_frames_per_gate=80):
    """计算多门串联的全部动画帧。
    
    Returns:
        dict: {
            "frames": list[(x,y,z)],     # 全部帧
            "boundaries": list[int],      # 每门帧起始索引
            "labels": list[str],          # 每门标签
            "final_state": BlochState,    # 最终态
        }
    """
```

逻辑：
1. 从 `initial` 态开始
2. 对链上每个门：
   - 调用 `get_gate(type, theta)` 获取门定义
   - 调用 `generate_frames(current_state, gate, num_frames)` 获取该门的帧
   - 将帧追加到总帧列表
   - 记录帧起始索引到 `boundaries`
   - `current_state` 更新为该门的 `final_state`
3. 返回全部帧、边界索引、标签和最终态

### 3D 场景扩展

`visualization/scene.py` 中 `scene_data` 增加字段：

```python
{
    # ... 现有字段 ...
    "chain_frames": [...],        # 全部链帧
    "chain_boundaries": [0, 80],  # 门边界
    "chain_labels": ["H", "Rx"],  # 门标签
}
```

Three.js 动画逻辑改动：
- 当 `chain_frames` 非空时，优先播放链动画
- 动画帧索引 `i` 通过 `boundaries` 判断当前属于哪个门
- 更新 UI 上显示的门标签为当前正在播放的门
- 每个门的旋转段无缝衔接（前门终点 = 后门起点）
- 门切换时更新旋转轴高亮和轨迹弧

### UI 控件

新增 `ui/controls.py` 中的函数：

```python
def render_chain_controls() -> dict:
    """渲染多门链控制区域。
    
    Returns:
        dict: {
            "chain_gates": list[dict],
            "apply_clicked": bool,
            "reset_clicked": bool,
        }
    """
```

每个门用一个 Streamlit expander：
- 标题: `GATE {n} — {type}` 或 `GATE {n} — {type}({theta:.2f})`
- 内容:
  - 门类型 radio: X / Y / Z / H / Rx / Ry / Rz (horizontal)
  - 旋转角滑块: 仅 Rx/Ry/Rz 显示, 0° ~ 360°
  - REMOVE 按钮（链只有 1 个门时 disabled）

操作按钮行：
- `+ ADD GATE`: 链尾追加默认 X 门
- `APPLY CHAIN`: 触发帧计算和动画
- `RESET CHAIN`: 重置为单个 X 门

### `app.py` 集成

在现有布局下方新增：

```python
# ── Multi-gate chain ──────────────────────────────────────
st.markdown("---")
chain_controls = render_chain_controls()

if chain_controls["apply_clicked"] and len(chain_controls["chain_gates"]) > 0:
    result = generate_chain_frames(
        st.session_state.bloch_state,
        chain_controls["chain_gates"],
    )
    st.session_state.chain_frames = result["frames"]
    st.session_state.chain_boundaries = result["boundaries"]
    st.session_state.chain_labels = result["labels"]
    st.session_state.chain_final_state = result["final_state"]
    st.session_state.chain_trigger += 1

if chain_controls["reset_clicked"]:
    st.session_state.chain_frames = []
    st.session_state.chain_boundaries = []
    st.session_state.chain_labels = []
    st.session_state.chain_final_state = None
    st.session_state.chain_trigger += 1

# 显示最终态
if st.session_state.chain_final_state:
    final = st.session_state.chain_final_state
    # 显示态信息、概率、Bloch 向量
```

场景数据传递：
- 当 `chain_frames` 非空时，`scene_data` 包含链字段
- Three.js 优先使用 `chain_frames` 播放链动画
- 单门模式的 `frames` 字段仍然独立存在，互不干扰

---

## 文件变更总结

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `quantum/state.py` | 修改 | `__init__` 支持 θ/φ 参数 |
| `ui/controls.py` | 修改 | Custom 态滑块 + `render_chain_controls()` |
| `quantum/evolution.py` | 修改 | 新增 `generate_chain_frames()` |
| `visualization/scene.py` | 修改 | Three.js 支持链动画和门标签切换 |
| `app.py` | 修改 | Custom 态处理 + 底部多门链区域 |
| `ui/styles.py` | 微调 | expander/链相关样式 |

## 风格一致性

所有新增 UI 元素遵循现有设计规范：
- JetBrains Mono 字体
- 黑底 (#0a0a0a) + 橙色 (#ff6b00) 配色
- 直角风格，无圆角
- 大写字母标题，字间距 1.5px
- 按钮: 黑底橙边，hover 反转
- 滑块: 橙色轨道和滑块头
