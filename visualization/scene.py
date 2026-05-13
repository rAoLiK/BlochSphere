import json


def build_scene_html(data: dict) -> str:
    """Build a complete HTML string with an embedded Three.js Bloch sphere scene."""
    data_json = json.dumps(data)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        background: #0a0a0a;
        overflow: hidden;
        font-family: 'JetBrains Mono', 'Courier New', monospace;
    }}
    #container {{ width: 100%; height: 100vh; position: relative; }}
    canvas {{ display: block; }}

    #container::after {{
        content: '';
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            rgba(0,0,0,0.12) 0px,
            transparent 2px,
            transparent 4px
        );
        pointer-events: none; z-index: 10;
    }}

    #controls {{
        position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
        display: flex; gap: 10px; z-index: 20;
        background: rgba(10,10,10,0.94); padding: 8px 16px;
        border: 2px solid #ff6b00;
    }}
    #controls button {{
        background: #0a0a0a; color: #ff6b00;
        border: 2px solid #ff6b00; padding: 6px 14px;
        font-family: inherit; font-size: 12px; cursor: pointer;
        text-transform: uppercase; letter-spacing: 1px;
        min-width: 60px;
    }}
    #controls button:hover {{ background: #ff6b00; color: #0a0a0a; }}
    #controls button.active {{ background: #ff6b00; color: #0a0a0a; }}

    #speed-label {{
        color: #ff8c00; font-size: 10px; align-self: center; letter-spacing: 1px;
        min-width: 70px; text-align: center;
    }}
    #speed-slider {{
        -webkit-appearance: none; appearance: none;
        background: #1a1a1a; border: 2px solid #ff6b00;
        height: 5px; width: 80px; align-self: center; cursor: pointer;
    }}
    #speed-slider::-webkit-slider-thumb {{
        -webkit-appearance: none; width: 12px; height: 12px;
        background: #ff6b00; border: none;
    }}
    #speed-slider::-moz-range-thumb {{
        width: 12px; height: 12px; background: #ff6b00; border: none; border-radius: 0;
    }}

    #info {{
        position: absolute; top: 12px; left: 12px; z-index: 20;
        color: #ff8c00; font-size: 11px; letter-spacing: 1px;
        background: rgba(10,10,10,0.88); padding: 8px 14px;
        border-left: 3px solid #ff6b00;
    }}
    #info .label {{ color: #777; }}
    #info .value {{ color: #ffaa00; }}
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

// ── Scene setup ──────────────────────────────────────
const container = document.getElementById('container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0a);
scene.fog = new THREE.Fog(0x0a0a0a, 3, 8);

const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 20);
camera.up.set(0, 0, 1);
camera.position.set(1.8, -2.0, 2.2);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({{ antialias: true }});
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
container.appendChild(renderer.domElement);

// ── Lighting ─────────────────────────────────────────
scene.add(new THREE.AmbientLight(0x332211, 1.5));
const pl1 = new THREE.PointLight(0xff6b00, 30, 10);
pl1.position.set(3, 3, 3);
scene.add(pl1);
const pl2 = new THREE.PointLight(0xff4400, 15, 8);
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
    color: 0xff6b00, emissive: 0xff4400, emissiveIntensity: 1.2,
    roughness: 0.3, metalness: 0.1
}});
const matX = new THREE.MeshStandardMaterial({{ color: 0xff3333, emissive: 0xff0000, emissiveIntensity: 0.6, roughness: 0.4 }});
const matY = new THREE.MeshStandardMaterial({{ color: 0x33ff33, emissive: 0x00ff00, emissiveIntensity: 0.6, roughness: 0.4 }});
const matZ = new THREE.MeshStandardMaterial({{ color: 0x3388ff, emissive: 0x0044ff, emissiveIntensity: 0.6, roughness: 0.4 }});

// ── Sphere wireframe ─────────────────────────────────
const sphereGeo = new THREE.SphereGeometry(1, 64, 48);
const wireGeo = new THREE.EdgesGeometry(sphereGeo);
scene.add(new THREE.LineSegments(wireGeo,
    new THREE.LineBasicMaterial({{ color: 0x332211, transparent: true, opacity: 0.4 }})));

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
scene.add(ring(1, 0, 0, 0, 0x332211, 0.25));
scene.add(ring(1, Math.PI/2, 0, 0, 0x332233, 0.18));
scene.add(ring(1, 0, 0, Math.PI/2, 0x332222, 0.18));

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
// Pole labels — placed away from axis tips
makeLabel('|0⟩', new THREE.Vector3(0, 0, 1.35), '#ff6b00');
makeLabel('|1⟩', new THREE.Vector3(0, 0, -1.20), '#ff6b00');
// Axis labels — placed well beyond arrowheads (which end at +/-1.25)
makeLabel('X', new THREE.Vector3(1.40, 0, 0), '#ff3333');
makeLabel('Y', new THREE.Vector3(0, 1.40, 0), '#33ff33');
makeLabel('Z', new THREE.Vector3(0, 0, 1.50), '#3388ff');

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

    // Solid backbone line (subtle)
    const spinePts = [dir.clone().multiplyScalar(-1.3), dir.clone().multiplyScalar(1.3)];
    const spineGeo = new THREE.BufferGeometry().setFromPoints(spinePts);
    axisHL.add(new THREE.Line(spineGeo,
        new THREE.LineBasicMaterial({{ color: 0xffaa00, transparent: true, opacity: 0.3 }})));

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
        new THREE.LineBasicMaterial({{ color: 0xffcc00, transparent: true, opacity: 0.9 }})));

    // Arrow cones at both ends to indicate axis direction
    [1, -1].forEach(function(sign) {{
        const tip = dir.clone().multiplyScalar(sign * 1.35);
        const coneGeo = new THREE.ConeGeometry(0.05, 0.14, 8);
        const cone = new THREE.Mesh(coneGeo,
            new THREE.MeshStandardMaterial({{ color: 0xffcc00, emissive: 0xff8800,
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
        color: 0xff8c00, emissive: 0xff4400, emissiveIntensity: 0.8,
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

    const segIdx = getGateIndex(frameIdx);
    const segStart = boundaries[segIdx] || 0;
    const segEnd = (segIdx + 1 < boundaries.length) ? boundaries[segIdx + 1] : frames.length;
    const shown = frames.slice(segStart, Math.min(frameIdx + 1, segEnd));
    if (shown.length < 2) return;

    const curve = new THREE.CatmullRomCurve3(
        shown.map(p => new THREE.Vector3(p[0], p[1], p[2])));
    const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.015, 8, false);
    const tube = new THREE.Mesh(tubeGeo, new THREE.MeshStandardMaterial({{
        color: 0xff8c00, emissive: 0xff4400, emissiveIntensity: 0.8,
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
