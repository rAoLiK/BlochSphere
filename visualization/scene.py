import json


def build_scene_html(data: dict) -> str:
    """Build a complete HTML string with an embedded Three.js Bloch sphere scene.

    Supports ``data["theme"]`` ("dark" or "light") to adapt colors.
    """
    data_json = json.dumps(data)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        overflow: hidden;
        font-family: 'Inter', 'JetBrains Mono', 'Courier New', monospace;
    }}
    #container {{ width: 100%; height: 100vh; position: relative; }}
    canvas {{ display: block; }}

    #container::after {{
        content: '';
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        pointer-events: none; z-index: 10;
    }}

    #controls {{
        position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
        display: flex; gap: 10px; z-index: 20;
        padding: 8px 18px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 8px;
    }}
    #controls button {{
        padding: 6px 14px;
        font-family: inherit; font-size: 12px; font-weight: 600; cursor: pointer;
        text-transform: uppercase; letter-spacing: 1px;
        min-width: 60px;
        border-radius: 6px;
        transition: all 0.18s ease;
    }}
    #controls button:hover {{ transform: translateY(-1px); }}
    #controls button:active {{ transform: translateY(0); }}

    #speed-label {{
        font-size: 10px; align-self: center; letter-spacing: 1px;
        min-width: 70px; text-align: center; font-weight: 600;
    }}
    #speed-slider {{
        -webkit-appearance: none; appearance: none;
        height: 5px; width: 80px; align-self: center; cursor: pointer;
        border-radius: 3px;
    }}
    #speed-slider::-webkit-slider-thumb {{
        -webkit-appearance: none; width: 12px; height: 12px;
        border: none; border-radius: 50%;
    }}
    #speed-slider::-moz-range-thumb {{
        width: 12px; height: 12px; border: none; border-radius: 50%;
    }}

    #info {{
        position: absolute; top: 10px; left: 10px; z-index: 20;
        font-size: 10px; letter-spacing: 1px;
        padding: 5px 10px;
        border-left: 2px solid;
        border-radius: 4px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        line-height: 1.5;
    }}
    #info .label {{ font-weight: 600; text-transform: uppercase; font-size: 9px; letter-spacing: 1.5px; }}
</style>
</head>
<body>
<div id="container">
    <div id="controls">
        <button id="btn-play">PLAY</button>
        <button id="btn-pause">PAUSE</button>
        <button id="btn-reset">RESET</button>
        <span id="speed-label">SPD 1.00x</span>
        <input type="range" id="speed-slider" min="0.25" max="4" step="0.25" value="1">
    </div>
    <div id="info">
        <span class="label">GATE</span> <span class="value" id="info-gate">-</span><br>
        <span class="label">BLOCH</span> <span class="value" id="info-bloch">-</span>
    </div>
</div>

<script type="importmap">
{{
    "imports": {{
        "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
    }}
}}
</script>

<script type="module">
import * as THREE from 'three';
import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';

const DATA = {data_json};
const THEME = DATA.theme || 'dark';

// ── Theme palettes ────────────────────────────────────
const palette = THEME === 'light'
    ? {{
        bg:         0xe8e3de,
        fog:        0xe8e3de,
        wire:       0xc0b8b0,
        wireOp:     0.40,
        ring1:      0xbab2aa,
        ring2:      0xc2bab2,
        ring3:      0xc6beb6,
        ringOp1:    0.30,
        ringOp2:    0.22,
        ambient:    0xe8e0d8,
        ambInt:     1.0,
        pl1Col:     0xc46860,
        pl1Int:     18,
        pl2Col:     0xa0403a,
        pl2Int:     8,
        glow:       0xa0403a,
        glowEmit:   0x8a3630,
        glowEmitI:  0.9,
        axisHL:     0xa0403a,
        axisHLEmit: 0x8a3630,
        dashCol:    0xb54a44,
        spineCol:   0xc8a8a4,
        spineOp:    0.35,
        dashOp:     0.85,
        coneEmit:   0x8a3630,
        trajCol:    0xa0403a,
        trajEmit:   0x8a3630,
        trajEmitI:  0.5,
        label0:     '#a0403a',
        label1:     '#a0403a',
        labelX:     '#cc3333',
        labelY:     '#33aa33',
        labelZ:     '#3366cc',
        ctrlsBg:    'rgba(232,227,222,0.88)',
        ctrlsBorder:'1.5px solid #a0403a',
        btnBg:      '#eae6e1',
        btnColor:   '#a0403a',
        btnBorder:  '1.5px solid #a0403a',
        btnHoverBg: '#a0403a',
        btnHoverCol:'#ffffff',
        spdColor:   '#a0403a',
        spdTrack:   '#d8d0ca',
        spdThumb:   '#a0403a',
        infoBg:     'rgba(232,227,222,0.88)',
        infoBorder: '#a0403a',
        infoLabel:  '#8a7c7c',
        infoValue:  '#a0403a',
    }}
    : {{
        bg:         0x0a0a0a,
        fog:        0x0a0a0a,
        wire:       0x332211,
        wireOp:     0.4,
        ring1:      0x332211,
        ring2:      0x332233,
        ring3:      0x332222,
        ringOp1:    0.25,
        ringOp2:    0.18,
        ambient:    0x332211,
        ambInt:     1.5,
        pl1Col:     0xff6b00,
        pl1Int:     30,
        pl2Col:     0xff4400,
        pl2Int:     15,
        glow:       0xff6b00,
        glowEmit:   0xff4400,
        glowEmitI:  1.2,
        axisHL:     0xffcc00,
        axisHLEmit: 0xff8800,
        dashCol:    0xffcc00,
        spineCol:   0xffaa00,
        spineOp:    0.3,
        dashOp:     0.9,
        coneEmit:   0xff8800,
        trajCol:    0xff8c00,
        trajEmit:   0xff4400,
        trajEmitI:  0.8,
        label0:     '#ff6b00',
        label1:     '#ff6b00',
        labelX:     '#ff3333',
        labelY:     '#33ff33',
        labelZ:     '#3388ff',
        ctrlsBg:    'rgba(10,10,10,0.94)',
        ctrlsBorder:'2px solid #ff6b00',
        btnBg:      '#0a0a0a',
        btnColor:   '#ff6b00',
        btnBorder:  '2px solid #ff6b00',
        btnHoverBg: '#ff6b00',
        btnHoverCol:'#0a0a0a',
        spdColor:   '#ff8c00',
        spdTrack:   '#1a1a1a',
        spdThumb:   '#ff6b00',
        infoBg:     'rgba(10,10,10,0.88)',
        infoBorder: '#ff6b00',
        infoLabel:  '#777777',
        infoValue:  '#ffaa00',
    }};

// ── Apply theme to CSS elements ───────────────────────
(function applyCssTheme() {{
    const c = document.getElementById('controls');
    c.style.background = palette.ctrlsBg;
    c.style.border = palette.ctrlsBorder;
    c.querySelectorAll('button').forEach(b => {{
        b.style.background = palette.btnBg;
        b.style.color = palette.btnColor;
        b.style.border = palette.btnBorder;
        b.onmouseenter = () => {{ b.style.background = palette.btnHoverBg; b.style.color = palette.btnHoverCol; }};
        b.onmouseleave = () => {{ b.style.background = palette.btnBg; b.style.color = palette.btnColor; }};
    }});
    document.getElementById('speed-label').style.color = palette.spdColor;
    const sl = document.getElementById('speed-slider');
    sl.style.background = palette.spdTrack;
    // thumb color via CSS custom property trick
    document.documentElement.style.setProperty('--thumb-color', palette.spdThumb);

    const info = document.getElementById('info');
    info.style.background = palette.infoBg;
    info.style.borderColor = palette.infoBorder;
    info.querySelectorAll('.label').forEach(l => l.style.color = palette.infoLabel);
    info.querySelectorAll('.value').forEach(v => v.style.color = palette.infoValue);
    document.body.style.background = '#' + palette.bg.toString(16).padStart(6, '0');
}})();

// Inject thumb color into stylesheet
const styleTag = document.createElement('style');
const scanOp = THEME === 'light' ? '0.03' : '0.12';
styleTag.textContent =
    '#speed-slider::-webkit-slider-thumb {{ background: ' + palette.spdThumb + ' !important; }}' +
    '#speed-slider::-moz-range-thumb {{ background: ' + palette.spdThumb + ' !important; }}' +
    '#controls button:hover {{ background: ' + palette.btnHoverBg + ' !important; color: ' + palette.btnHoverCol + ' !important; }}' +
    '#controls button.active {{ background: ' + palette.btnHoverBg + ' !important; color: ' + palette.btnHoverCol + ' !important; }}' +
    '#container::after {{ background: repeating-linear-gradient(rgba(0,0,0,' + scanOp + ') 0px, transparent 2px, transparent 4px); }}';
document.head.appendChild(styleTag);

// ── Scene setup ──────────────────────────────────────
const container = document.getElementById('container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(palette.bg);
scene.fog = new THREE.Fog(palette.fog, 3, 8);

const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 20);
camera.up.set(0, 0, 1);
camera.position.set(1.8, -2.0, 2.2);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({{ antialias: true }});
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
container.appendChild(renderer.domElement);

// ── Lighting ─────────────────────────────────────────
scene.add(new THREE.AmbientLight(palette.ambient, palette.ambInt));
const pl1 = new THREE.PointLight(palette.pl1Col, palette.pl1Int, 10);
pl1.position.set(3, 3, 3);
scene.add(pl1);
const pl2 = new THREE.PointLight(palette.pl2Col, palette.pl2Int, 8);
pl2.position.set(-3, -2, -3);
scene.add(pl2);

// ── OrbitControls ────────────────────────────────────
const orbitCtrl = new OrbitControls(camera, renderer.domElement);
orbitCtrl.enableDamping = true;
orbitCtrl.dampingFactor = 0.08;
orbitCtrl.minDistance = 1.5;
orbitCtrl.maxDistance = 6;
orbitCtrl.target.set(0, 0, 0);
orbitCtrl.autoRotate = true;
orbitCtrl.autoRotateSpeed = 0.3;

// ── Materials ────────────────────────────────────────
const matGlow = new THREE.MeshStandardMaterial({{
    color: palette.glow, emissive: palette.glowEmit, emissiveIntensity: palette.glowEmitI,
    roughness: 0.3, metalness: 0.1
}});
const matX = new THREE.MeshStandardMaterial({{ color: 0xff3333, emissive: 0xff0000, emissiveIntensity: 0.6, roughness: 0.4 }});
const matY = new THREE.MeshStandardMaterial({{ color: 0x33ff33, emissive: 0x00ff00, emissiveIntensity: 0.6, roughness: 0.4 }});
const matZ = new THREE.MeshStandardMaterial({{ color: 0x3388ff, emissive: 0x0044ff, emissiveIntensity: 0.6, roughness: 0.4 }});

// ── Sphere wireframe ─────────────────────────────────
const sphereGeo = new THREE.SphereGeometry(1, 64, 48);
const wireGeo = new THREE.EdgesGeometry(sphereGeo);
scene.add(new THREE.LineSegments(wireGeo,
    new THREE.LineBasicMaterial({{ color: palette.wire, transparent: true, opacity: palette.wireOp }})));

// ── Reference rings ──────────────────────────────────
function ring(r, rx, ry, rz, col, op) {{
    const pts = [];
    for (let i = 0; i <= 128; i++) {{
        const a = (i / 128) * Math.PI * 2;
        pts.push(new THREE.Vector3(Math.cos(a) * r, Math.sin(a) * r, 0));
    }}
    const g = new THREE.BufferGeometry().setFromPoints(pts);
    const l = new THREE.Line(g, new THREE.LineBasicMaterial({{ color: col, transparent: true, opacity: op }}));
    l.rotation.set(rx, ry, rz);
    return l;
}}
scene.add(ring(1, 0, 0, 0, palette.ring1, palette.ringOp1));
scene.add(ring(1, Math.PI/2, 0, 0, palette.ring2, palette.ringOp2));
scene.add(ring(1, 0, 0, Math.PI/2, palette.ring3, palette.ringOp2));

// ── Axes ─────────────────────────────────────────────
function createAxis(from, to, mat) {{
    const dir = new THREE.Vector3().subVectors(to, from);
    const len = dir.length();
    const mid = new THREE.Vector3().addVectors(from, to).multiplyScalar(0.5);
    const cg = new THREE.CylinderGeometry(0.015, 0.015, len, 8);
    const cyl = new THREE.Mesh(cg, mat);
    cyl.position.copy(mid);
    const ax = dir.normalize();
    cyl.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), ax);
    scene.add(cyl);
    const coneG = new THREE.ConeGeometry(0.04, 0.12, 8);
    const cone = new THREE.Mesh(coneG, mat);
    cone.position.copy(to);
    cone.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), ax);
    scene.add(cone);
}}
createAxis(new THREE.Vector3(0,0,0), new THREE.Vector3(1.25,0,0), matX);
createAxis(new THREE.Vector3(0,0,0), new THREE.Vector3(0,1.25,0), matY);
createAxis(new THREE.Vector3(0,0,0), new THREE.Vector3(0,0,1.25), matZ);
createAxis(new THREE.Vector3(0,0,0), new THREE.Vector3(-1.05,0,0), matX);
createAxis(new THREE.Vector3(0,0,0), new THREE.Vector3(0,-1.05,0), matY);
createAxis(new THREE.Vector3(0,0,0), new THREE.Vector3(0,0,-1.05), matZ);

// ── Labels (sprites) ─────────────────────────────────
function makeLabel(text, pos, color) {{
    const canvas = document.createElement('canvas');
    canvas.width = 128; canvas.height = 64;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = color;
    ctx.font = 'bold 30px monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, 64, 32);
    const tex = new THREE.CanvasTexture(canvas);
    tex.minFilter = THREE.LinearFilter;
    const sp = new THREE.Sprite(new THREE.SpriteMaterial({{ map: tex, transparent: true, opacity: 0.9 }}));
    sp.position.copy(pos);
    sp.scale.set(0.4, 0.2, 1);
    scene.add(sp);
}}
makeLabel('|0⟩', new THREE.Vector3(0, 0, 1.35), palette.label0);
makeLabel('|1⟩', new THREE.Vector3(0, 0, -1.20), palette.label0);
makeLabel('X', new THREE.Vector3(1.40, 0, 0), palette.labelX);
makeLabel('Y', new THREE.Vector3(0, 1.40, 0), palette.labelY);
makeLabel('Z', new THREE.Vector3(0, 0, 1.50), palette.labelZ);

// ── State vector arrow ───────────────────────────────
const arrowGroup = new THREE.Group();
scene.add(arrowGroup);

function updateArrow(x, y, z) {{
    while (arrowGroup.children.length > 0) arrowGroup.remove(arrowGroup.children[0]);
    const len = Math.sqrt(x*x + y*y + z*z);
    if (len < 0.001) return;
    const dir = new THREE.Vector3(x, y, z).normalize();
    const tip = new THREE.Vector3(x, y, z);
    const shaftLen = len - 0.08;
    const midPt = dir.clone().multiplyScalar(shaftLen / 2);
    const shaftGeo = new THREE.CylinderGeometry(0.025, 0.025, shaftLen, 12);
    const shaft = new THREE.Mesh(shaftGeo, matGlow);
    shaft.position.copy(midPt);
    shaft.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
    arrowGroup.add(shaft);
    const headGeo = new THREE.ConeGeometry(0.06, 0.15, 12);
    const head = new THREE.Mesh(headGeo, matGlow);
    head.position.copy(tip);
    head.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
    arrowGroup.add(head);
    const dotGeo = new THREE.SphereGeometry(0.04, 16, 16);
    arrowGroup.add(new THREE.Mesh(dotGeo, matGlow));
}}

// ── Rotation axis highlight ──────────────────────────
const axisHL = new THREE.Group();
scene.add(axisHL);

function updateAxisHighlight(ax, ay, az, visible) {{
    while (axisHL.children.length > 0) axisHL.remove(axisHL.children[0]);
    if (!visible) return;
    const l = Math.sqrt(ax*ax + ay*ay + az*az);
    if (l < 0.001) return;
    const dir = new THREE.Vector3(ax, ay, az).normalize();

    // Solid backbone line
    const spinePts = [dir.clone().multiplyScalar(-1.3), dir.clone().multiplyScalar(1.3)];
    const spineGeo = new THREE.BufferGeometry().setFromPoints(spinePts);
    axisHL.add(new THREE.Line(spineGeo,
        new THREE.LineBasicMaterial({{ color: palette.spineCol, transparent: true, opacity: palette.spineOp }})));

    // Dashed highlight segments
    const dashPts = [];
    const nDashes = 20;
    const segLen = 1.30 / nDashes;
    for (let i = 0; i < nDashes; i += 2) {{
        const t1 = -1.30 + i * segLen * 2;
        const t2 = -1.30 + (i + 1) * segLen * 2;
        dashPts.push(dir.clone().multiplyScalar(t1));
        dashPts.push(dir.clone().multiplyScalar(t2));
    }}
    const dg = new THREE.BufferGeometry().setFromPoints(dashPts);
    axisHL.add(new THREE.LineSegments(dg,
        new THREE.LineBasicMaterial({{ color: palette.dashCol, transparent: true, opacity: palette.dashOp }})));

    // Arrow cones at both ends
    [1, -1].forEach(function(sign) {{
        const tip = dir.clone().multiplyScalar(sign * 1.35);
        const coneGeo = new THREE.ConeGeometry(0.05, 0.14, 8);
        const cone = new THREE.Mesh(coneGeo,
            new THREE.MeshStandardMaterial({{ color: palette.axisHL, emissive: palette.coneEmit,
                emissiveIntensity: 0.5, roughness: 0.4 }}));
        cone.position.copy(tip);
        cone.quaternion.setFromUnitVectors(
            new THREE.Vector3(0, 1, 0), dir.clone().multiplyScalar(sign));
        axisHL.add(cone);
    }});
}}

// ── Trajectory arc ───────────────────────────────────
const trajGroup = new THREE.Group();
scene.add(trajGroup);

function updateTrajectory(framePoints, currentIdx) {{
    while (trajGroup.children.length > 0) trajGroup.remove(trajGroup.children[0]);
    if (!framePoints || framePoints.length < 2) return;
    const shown = framePoints.slice(0, currentIdx + 1);
    if (shown.length < 2) return;
    const curve = new THREE.CatmullRomCurve3(
        shown.map(p => new THREE.Vector3(p[0], p[1], p[2])));
    const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.015, 8, false);
    const tube = new THREE.Mesh(tubeGeo, new THREE.MeshStandardMaterial({{
        color: palette.trajCol, emissive: palette.trajEmit, emissiveIntensity: palette.trajEmitI,
        roughness: 0.2, transparent: true, opacity: 0.85
    }}));
    trajGroup.add(tube);
    for (let i = 0; i < shown.length; i += Math.max(1, Math.floor(shown.length / 20))) {{
        const p = shown[i];
        const dotGeo = new THREE.SphereGeometry(0.02, 8, 8);
        const dot = new THREE.Mesh(dotGeo, matGlow);
        dot.position.set(p[0], p[1], p[2]);
        trajGroup.add(dot);
    }}
}}

// ── Animation state ──────────────────────────────────
const frames = DATA.chain_frames && DATA.chain_frames.length > 0
    ? DATA.chain_frames : (DATA.frames || []);
const boundaries = DATA.chain_boundaries || [];
const chainLabels = DATA.chain_labels || [];
const chainDetails = DATA.chain_details || [];
const isChain = boundaries.length > 0;

let currentFrame = 0;
let playing = true;
let speed = DATA.speed || 1.0;
const frameInterval = 0.016;
let elapsed = 0;
let animDone = false;
let currentGateIdx = 0;

// ── Initialize ───────────────────────────────────────
if (DATA.bloch_vector) {{
    updateArrow(DATA.bloch_vector[0], DATA.bloch_vector[1], DATA.bloch_vector[2]);
}}
if (isChain && chainDetails.length > 0) {{
    const d = chainDetails[0];
    updateAxisHighlight(d.axis[0], d.axis[1], d.axis[2], true);
}} else if (DATA.axis) {{
    updateAxisHighlight(DATA.axis[0], DATA.axis[1], DATA.axis[2], true);
}}

function updateInfo() {{
    let g;
    if (isChain && chainLabels.length > 0) {{
        g = chainLabels[currentGateIdx] || '-';
    }} else {{
        g = DATA.gate_label || '-';
    }}
    const bv = DATA.bloch_vector || [0,0,0];
    document.getElementById('info-gate').textContent = g;
    document.getElementById('info-bloch').textContent =
        '(' + bv.map(v => v.toFixed(3)).join(', ') + ')';
}}
updateInfo();

// ── Chain gate segment tracking ──────────────────────
function getGateIndex(frameIdx) {{
    if (!isChain || boundaries.length === 0) return 0;
    for (let i = boundaries.length - 1; i >= 0; i--) {{
        if (frameIdx >= boundaries[i]) return i;
    }}
    return 0;
}}

function updateChainTrajectory(frameIdx) {{
    while (trajGroup.children.length > 0) trajGroup.remove(trajGroup.children[0]);
    if (!frames || frames.length < 2) return;

    const currentSeg = getGateIndex(frameIdx);

    // Render completed segments with fading opacity
    for (let s = 0; s < currentSeg; s++) {{
        const sStart = boundaries[s] || 0;
        const sEnd = (s + 1 < boundaries.length) ? boundaries[s + 1] : frames.length;
        const segFrames = frames.slice(sStart, sEnd);
        if (segFrames.length < 2) continue;

        const fadeFactor = (currentSeg - s);
        const opacity = Math.max(0.12, 0.6 - fadeFactor * 0.2);

        const curve = new THREE.CatmullRomCurve3(
            segFrames.map(p => new THREE.Vector3(p[0], p[1], p[2])));
        const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.015, 8, false);
        const tube = new THREE.Mesh(tubeGeo, new THREE.MeshStandardMaterial({{
            color: palette.trajCol, emissive: palette.trajEmit, emissiveIntensity: palette.trajEmitI * 0.5,
            roughness: 0.2, transparent: true, opacity: opacity
        }}));
        trajGroup.add(tube);
    }}

    // Render current segment up to current frame
    const segStart = boundaries[currentSeg] || 0;
    const segEnd = (currentSeg + 1 < boundaries.length) ? boundaries[currentSeg + 1] : frames.length;
    const shown = frames.slice(segStart, Math.min(frameIdx + 1, segEnd));
    if (shown.length < 2) return;

    const curve = new THREE.CatmullRomCurve3(
        shown.map(p => new THREE.Vector3(p[0], p[1], p[2])));
    const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.015, 8, false);
    const tube = new THREE.Mesh(tubeGeo, new THREE.MeshStandardMaterial({{
        color: palette.trajCol, emissive: palette.trajEmit, emissiveIntensity: palette.trajEmitI,
        roughness: 0.2, transparent: true, opacity: 0.85
    }}));
    trajGroup.add(tube);
    for (let i = 0; i < shown.length; i += Math.max(1, Math.floor(shown.length / 20))) {{
        const p = shown[i];
        const dotGeo = new THREE.SphereGeometry(0.02, 8, 8);
        const dot = new THREE.Mesh(dotGeo, matGlow);
        dot.position.set(p[0], p[1], p[2]);
        trajGroup.add(dot);
    }}
}}

// ── Controls via addEventListener ────────────────────
const btnPlay = document.getElementById('btn-play');
const btnPause = document.getElementById('btn-pause');
const btnReset = document.getElementById('btn-reset');
const spdSlider = document.getElementById('speed-slider');
const spdLabel = document.getElementById('speed-label');

btnPlay.addEventListener('click', function() {{
    if (animDone) {{
        currentFrame = 0;
        elapsed = 0;
        animDone = false;
        currentGateIdx = 0;
        playing = true;
        btnPlay.classList.add('active');
        if (frames.length > 0) {{
            updateArrow(frames[0][0], frames[0][1], frames[0][2]);
            if (isChain) {{
                updateChainTrajectory(0);
                if (chainDetails.length > 0) {{
                    const d = chainDetails[0];
                    updateAxisHighlight(d.axis[0], d.axis[1], d.axis[2], true);
                }}
            }} else {{
                updateTrajectory(frames, 0);
            }}
        }}
    }} else {{
        playing = !playing;
        btnPlay.classList.toggle('active', playing);
    }}
}});

btnPause.addEventListener('click', function() {{
    playing = false;
    btnPlay.classList.remove('active');
}});

btnReset.addEventListener('click', function() {{
    currentFrame = 0;
    elapsed = 0;
    playing = false;
    animDone = false;
    currentGateIdx = 0;
    btnPlay.classList.remove('active');
    if (frames.length > 0) {{
        const f = frames[0];
        updateArrow(f[0], f[1], f[2]);
        if (isChain) {{
            updateChainTrajectory(0);
            if (chainDetails.length > 0) {{
                const d = chainDetails[0];
                updateAxisHighlight(d.axis[0], d.axis[1], d.axis[2], true);
            }}
        }} else {{
            updateTrajectory(frames, 0);
        }}
    }}
}});

spdSlider.addEventListener('input', function() {{
    speed = parseFloat(this.value);
    spdLabel.textContent = 'SPD ' + speed.toFixed(2) + 'x';
}});

btnPlay.classList.add('active');
spdSlider.value = DATA.speed || 1;
spdLabel.textContent = 'SPD ' + (DATA.speed || 1).toFixed(2) + 'x';

// ── Render loop ──────────────────────────────────────
const clock = new THREE.Clock();

function animate() {{
    requestAnimationFrame(animate);
    const dt = Math.min(clock.getDelta(), 0.1);
    orbitCtrl.update();

    if (playing && frames.length > 1 && !animDone) {{
        elapsed += dt * speed;
        const fps = 1 / frameInterval;
        currentFrame = Math.min(Math.floor(elapsed * fps), frames.length - 1);
        const f = frames[currentFrame];
        updateArrow(f[0], f[1], f[2]);

        if (isChain) {{
            const newGateIdx = getGateIndex(currentFrame);
            if (newGateIdx !== currentGateIdx) {{
                currentGateIdx = newGateIdx;
                if (currentGateIdx < chainDetails.length) {{
                    const d = chainDetails[currentGateIdx];
                    updateAxisHighlight(d.axis[0], d.axis[1], d.axis[2], true);
                }}
            }}
            updateChainTrajectory(currentFrame);
            document.getElementById('info-gate').textContent =
                chainLabels[currentGateIdx] || '-';
        }} else {{
            updateTrajectory(frames, currentFrame);
        }}

        document.getElementById('info-bloch').textContent =
            '(' + f[0].toFixed(3) + ', ' + f[1].toFixed(3) + ', ' + f[2].toFixed(3) + ')';

        if (currentFrame >= frames.length - 1) {{
            animDone = true;
            playing = false;
            btnPlay.classList.remove('active');
        }}
    }}
    renderer.render(scene, camera);
}}
animate();

// ── Resize ───────────────────────────────────────────
window.addEventListener('resize', () => {{
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}});
</script>
</body>
</html>"""
