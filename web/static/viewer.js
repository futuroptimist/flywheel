import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/OrbitControls.js';
import { OBJLoader } from 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/OBJLoader.js';

const select = document.getElementById('model-select');
const models = JSON.parse(select.dataset.models || '[]');

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
camera.position.z = 5;

function loadModel(name) {
  const loader = new OBJLoader();
  loader.load(`/static/models/${name}`, obj => {
    scene.clear();
    scene.add(obj);
  });
}

models.forEach(m => {
  const opt = document.createElement('option');
  opt.value = m;
  opt.textContent = m;
  select.appendChild(opt);
});

if (models.length) {
  loadModel(models[0]);
}

select.addEventListener('change', () => loadModel(select.value));

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

animate();
