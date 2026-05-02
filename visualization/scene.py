import json


def build_scene_html(data: dict) -> str:
    """Build a complete HTML string with an embedded Three.js Bloch sphere scene.

    Args:
        data: dict with keys:
            bloch_vector: [x, y, z] — current state position
            frames: [[x,y,z], ...] — animation trajectory frames
            axis: [ax, ay, az] — rotation axis (normalized)
            angle: float — total rotation angle in radians
            gate_label: str — name of the applied gate
            prob0, prob1: float — measurement probabilities
            state_text: str — Dirac ket notation
            speed: float — animation speed multiplier (default 1.0)
    """
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
    #container {{ width: 100vw; height: 100vh; position: relative; }}
    canvas {{ display: block; }}

    /* CRT scanline overlay */
    #container::after {{
        content: '';
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            rgba(0,0,0,0.15) 0px,
            transparent 2px,
            transparent 4px
        );
        pointer-events: none; z-index: 10;
    }}

    /* Control overlay */
    #controls {{
        position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
        display: flex; gap: 12px; z-index: 20;
        background: rgba(10,10,10,0.92); padding: 10px 20px;
        border: 2px solid #ff6b00;
    }}
    #controls button {{
        background: #0a0a0a; color: #ff6b00;
        border: 2px solid #ff6b00; padding: 8px 18px;
        font-family: inherit; font-size: 13px; cursor: pointer;
        text-transform: uppercase; letter-spacing: 1px;
    }}
    #controls button:hover {{ background: #ff6b00; color: #0a0a0a; }}
    #controls button.active {{ background: #ff6b00; color: #0a0a0a; }}

    #speed-label {{
        color: #ff8c00; font-size: 11px; align-self: center;
        letter-spacing: 1px;
    }}
    #speed-slider {{
        -webkit-appearance: none; background: #1a1a1a;
        border: 2px solid #ff6b00; height: 6px; width: 100px;
        align-self: center; cursor: pointer;
    }}
    #speed-slider::-webkit-slider-thumb {{
        -webkit-appearance: none; width: 14px; height: 14px;
        background: #ff6b00; border: none;
    }}

    /* Info overlay */
    #info {{
        position: absolute; top: 16px; left: 16px; z-index: 20;
        color: #ff8c00; font-size: 12px; letter-spacing: 1px;
        background: rgba(10,10,10,0.85); padding: 10px 16px;
        border-left: 3px solid #ff6b00;
    }}
    #info .label {{ color: #888; }}
    #info .value {{ color: #ffaa00; }}
</style>
</head>
<body>
<div id="container">
    <div id="controls">
        <button id="btn-play" onclick="togglePlay()">&#9654; PLAY</button>
        <button id="btn-pause" onclick="pause()">&#9646;&#9646; PAUSE</button>
        <button id="btn-reset" onclick="resetAnim()">&#8634; RESET</button>
        <span id="speed-label">SPD 1.0x</span>
        <input type="range" id="speed-slider" min="0.25" max="4" step="0.25" value="1"
               oninput="setSpeed(this.value)">
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

// ── Read initial data ──────────────────────────────────────────────
const DATA = {data_json};

// ── Scene setup ────────────────────────────────────────────────────
const container = document.getElementById('container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0a);
scene.fog = new THREE.Fog(0x0a0a0a, 3, 8);

const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 20);
camera.position.set(2.2, 1.4, 2.2);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({{ antialias: true }});
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
container.appendChild(renderer.domElement);

// ── Lighting ───────────────────────────────────────────────────────
scene.add(new THREE.AmbientLight(0x332211, 1.5));
const pointLight = new THREE.PointLight(0xff6b00, 30, 10);
pointLight.position.set(3, 3, 3);
scene.add(pointLight);
const pointLight2 = new THREE.PointLight(0xff4400, 15, 8);
pointLight2.position.set(-3, -2, -3);
scene.add(pointLight2);

// ── OrbitControls ──────────────────────────────────────────────────
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 1.5;
controls.maxDistance = 6;
controls.target.set(0, 0, 0);
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;

// ── Materials ──────────────────────────────────────────────────────
const matOrangeGlow = new THREE.MeshStandardMaterial({{
    color: 0xff6b00, emissive: 0xff4400, emissiveIntensity: 1.2,
    roughness: 0.3, metalness: 0.1
}});
const matOrangeLine = new THREE.MeshBasicMaterial({{ color: 0xff6b00, transparent: true, opacity: 0.6 }});
const matAxisX = new THREE.MeshStandardMaterial({{ color: 0xff3333, emissive: 0xff0000, emissiveIntensity: 0.6, roughness: 0.4 }});
const matAxisY = new THREE.MeshStandardMaterial({{ color: 0x33ff33, emissive: 0x00ff00, emissiveIntensity: 0.6, roughness: 0.4 }});
const matAxisZ = new THREE.MeshStandardMaterial({{ color: 0x3388ff, emissive: 0x0044ff, emissiveIntensity: 0.6, roughness: 0.4 }});
const matYellow = new THREE.MeshBasicMaterial({{ color: 0xffaa00, transparent: true, opacity: 0.8 }});

// ── Bloch Sphere (wireframe) ───────────────────────────────────────
const sphereGeo = new THREE.SphereGeometry(1, 64, 48);
const wireframeGeo = new THREE.EdgesGeometry(sphereGeo);
const sphereWire = new THREE.LineSegments(wireframeGeo,
    new THREE.LineBasicMaterial({{ color: 0x332211, transparent: true, opacity: 0.4 }}));
scene.add(sphereWire);

// Grid rings (equator + meridians)
function createRing(radius, rotX, rotY, rotZ, color, opacity) {{
    const pts = [];
    const n = 128;
    for (let i = 0; i <= n; i++) {{
        const angle = (i / n) * Math.PI * 2;
        pts.push(new THREE.Vector3(Math.cos(angle) * radius, Math.sin(angle) * radius, 0));
    }}
    const geo = new THREE.BufferGeometry().setFromPoints(pts);
    const line = new THREE.Line(geo, new THREE.LineBasicMaterial({{ color, transparent: true, opacity }}));
    line.rotation.set(rotX, rotY, rotZ);
    return line;
}}
scene.add(createRing(1, 0, 0, 0, 0x332211, 0.25));   // XY equator
scene.add(createRing(1, Math.PI/2, 0, 0, 0x332233, 0.2)); // XZ
scene.add(createRing(1, 0, 0, Math.PI/2, 0x332222, 0.2)); // YZ

// ── Axes ───────────────────────────────────────────────────────────
function createAxis(from, to, material) {{
    const dir = new THREE.Vector3().subVectors(to, from);
    const len = dir.length();
    const mid = new THREE.Vector3().addVectors(from, to).multiplyScalar(0.5);
    const cylGeo = new THREE.CylinderGeometry(0.015, 0.015, len, 8);
    const cyl = new THREE.Mesh(cylGeo, material);
    cyl.position.copy(mid);
    const axis = dir.normalize();
    cyl.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), axis);
    scene.add(cyl);

    // Cone arrowhead
    const coneGeo = new THREE.ConeGeometry(0.04, 0.12, 8);
    const cone = new THREE.Mesh(coneGeo, material);
    cone.position.copy(to);
    cone.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), axis);
    scene.add(cone);
    return cyl;
}}
createAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(1.25, 0, 0), matAxisX);
createAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 1.25, 0), matAxisY);
createAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, 1.25), matAxisZ);
createAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(-1.05, 0, 0), matAxisX);
createAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, -1.05, 0), matAxisY);
createAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, -1.05), matAxisZ);

// ── Pole labels (sprites) ──────────────────────────────────────────
function createLabel(text, position, color) {{
    const canvas = document.createElement('canvas');
    canvas.width = 128; canvas.height = 64;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = color;
    ctx.font = 'bold 32px monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, 64, 32);
    const texture = new THREE.CanvasTexture(canvas);
    texture.minFilter = THREE.LinearFilter;
    const spriteMat = new THREE.SpriteMaterial({{ map: texture, transparent: true, opacity: 0.9 }});
    const sprite = new THREE.Sprite(spriteMat);
    sprite.position.copy(position);
    sprite.scale.set(0.4, 0.2, 1);
    scene.add(sprite);
}}
createLabel('|0⟩', new THREE.Vector3(0, 1.15, 0), '#ff6b00');
createLabel('|1⟩', new THREE.Vector3(0, -1.15, 0), '#ff6b00');

// Axis labels
createLabel('X', new THREE.Vector3(1.4, 0, 0), '#ff3333');
createLabel('Y', new THREE.Vector3(0, 1.4, 0), '#33ff33');
createLabel('Z', new THREE.Vector3(0, 0, 1.4), '#3388ff');

// ── State vector arrow ─────────────────────────────────────────────
const arrowGroup = new THREE.Group();
scene.add(arrowGroup);

function updateArrow(x, y, z) {{
    while (arrowGroup.children.length > 0) arrowGroup.remove(arrowGroup.children[0]);

    const len = Math.sqrt(x*x + y*y + z*z);
    if (len < 0.001) return;

    const dir = new THREE.Vector3(x, y, z).normalize();
    const tip = new THREE.Vector3(x, y, z);

    // Shaft
    const shaftLen = len - 0.08;
    const midPt = dir.clone().multiplyScalar(shaftLen / 2);
    const shaftGeo = new THREE.CylinderGeometry(0.025, 0.025, shaftLen, 12);
    const shaft = new THREE.Mesh(shaftGeo, matOrangeGlow);
    shaft.position.copy(midPt);
    shaft.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
    arrowGroup.add(shaft);

    // Cone head
    const headGeo = new THREE.ConeGeometry(0.06, 0.15, 12);
    const head = new THREE.Mesh(headGeo, matOrangeGlow);
    head.position.copy(tip);
    head.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
    arrowGroup.add(head);

    // Glow sphere at origin
    const dotGeo = new THREE.SphereGeometry(0.04, 16, 16);
    const dot = new THREE.Mesh(dotGeo, matOrangeGlow);
    arrowGroup.add(dot);
}}

// ── Rotation axis highlight ────────────────────────────────────────
const axisHighlight = new THREE.Group();
scene.add(axisHighlight);

function updateAxisHighlight(ax, ay, az, visible) {{
    while (axisHighlight.children.length > 0) axisHighlight.remove(axisHighlight.children[0]);
    if (!visible) return;

    const len = Math.sqrt(ax*ax + ay*ay + az*az);
    if (len < 0.001) return;
    const dir = new THREE.Vector3(ax, ay, az).normalize();

    const dashPts = [];
    const dashCount = 16;
    const dashLen = 1.25 / dashCount;
    for (let i = 0; i < dashCount; i += 2) {{
        const t1 = -1.25 + i * dashLen * 2;
        const t2 = -1.25 + (i + 1) * dashLen * 2;
        dashPts.push(dir.clone().multiplyScalar(t1));
        dashPts.push(dir.clone().multiplyScalar(t2));
    }}
    const dashGeo = new THREE.BufferGeometry().setFromPoints(dashPts);
    const dashLine = new THREE.LineSegments(dashGeo,
        new THREE.LineBasicMaterial({{ color: 0xffaa00, transparent: true, opacity: 0.7, linewidth: 1 }}));
    axisHighlight.add(dashLine);
}}

// ── Trajectory arc ─────────────────────────────────────────────────
const trajectoryGroup = new THREE.Group();
scene.add(trajectoryGroup);

function updateTrajectory(framePoints, currentIdx) {{
    while (trajectoryGroup.children.length > 0) trajectoryGroup.remove(trajectoryGroup.children[0]);
    if (!framePoints || framePoints.length < 2) return;

    const shown = framePoints.slice(0, currentIdx + 1);
    if (shown.length < 2) return;

    const curve = new THREE.CatmullRomCurve3(
        shown.map(p => new THREE.Vector3(p[0], p[1], p[2]))
    );
    const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.015, 8, false);
    const tubeMat = new THREE.MeshStandardMaterial({{
        color: 0xff8c00, emissive: 0xff4400, emissiveIntensity: 0.8,
        roughness: 0.2, transparent: true, opacity: 0.85
    }});
    const tube = new THREE.Mesh(tubeGeo, tubeMat);
    trajectoryGroup.add(tube);

    // Glow points along trajectory
    for (let i = 0; i < shown.length; i += Math.max(1, Math.floor(shown.length / 20))) {{
        const p = shown[i];
        const dotGeo = new THREE.SphereGeometry(0.02, 8, 8);
        const dot = new THREE.Mesh(dotGeo, matOrangeGlow);
        dot.position.set(p[0], p[1], p[2]);
        trajectoryGroup.add(dot);
    }}
}}

// ── Animation state ────────────────────────────────────────────────
let frames = DATA.frames || [];
let currentFrame = 0;
let playing = true;
let speed = DATA.speed || 1.0;
const frameInterval = 0.016; // ~60fps per frame step

let elapsed = 0;
let animDone = false;

// ── Initialize scene ───────────────────────────────────────────────
if (DATA.bloch_vector) {{
    updateArrow(DATA.bloch_vector[0], DATA.bloch_vector[1], DATA.bloch_vector[2]);
}}
if (DATA.axis) {{
    updateAxisHighlight(DATA.axis[0], DATA.axis[1], DATA.axis[2], true);
}}
updateInfo();

function updateInfo() {{
    const g = DATA.gate_label || '-';
    const bv = DATA.bloch_vector || [0,0,0];
    document.getElementById('info-gate').textContent = g;
    document.getElementById('info-bloch').textContent =
        '(' + bv.map(v => v.toFixed(3)).join(', ') + ')';
}}

// ── Playback controls (JS-side) ────────────────────────────────────
window.togglePlay = function() {{
    playing = !playing;
    document.getElementById('btn-play').classList.toggle('active', playing);
}};
window.pause = function() {{
    playing = false;
    document.getElementById('btn-play').classList.remove('active');
}};
window.resetAnim = function() {{
    currentFrame = 0;
    playing = true;
    animDone = false;
    document.getElementById('btn-play').classList.add('active');
    if (frames.length > 0) {{
        const f = frames[0];
        updateArrow(f[0], f[1], f[2]);
        updateTrajectory(frames, 0);
    }}
}};
window.setSpeed = function(v) {{
    speed = parseFloat(v);
    document.getElementById('speed-label').textContent = 'SPD ' + speed.toFixed(2) + 'x';
}};

// Init button states
document.getElementById('btn-play').classList.add('active');

// ── Render loop ────────────────────────────────────────────────────
const clock = new THREE.Clock();

function animate() {{
    requestAnimationFrame(animate);

    const dt = Math.min(clock.getDelta(), 0.1);
    controls.update();

    // Animation playback
    if (playing && frames.length > 1 && !animDone) {{
        elapsed += dt * speed;
        const stepsPerSecond = 1 / frameInterval;
        currentFrame = Math.min(Math.floor(elapsed * stepsPerSecond), frames.length - 1);

        const f = frames[currentFrame];
        updateArrow(f[0], f[1], f[2]);
        updateTrajectory(frames, currentFrame);

        if (currentFrame >= frames.length - 1) {{
            animDone = true;
            playing = false;
            document.getElementById('btn-play').classList.remove('active');
        }}
    }}

    renderer.render(scene, camera);
}}

animate();

// ── Responsive resize ──────────────────────────────────────────────
window.addEventListener('resize', () => {{
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}});
</script>
</body>
</html>"""
