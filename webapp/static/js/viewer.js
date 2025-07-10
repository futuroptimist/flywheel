import * as THREE from 'three';
import { OBJLoader } from 'https://unpkg.com/three@0.178.0/examples/jsm/loaders/OBJLoader.js';

const container = document.getElementById('viewer');
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth || 800, 600);
container.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, (container.clientWidth || 800) / 600, 0.1, 1000);
camera.position.z = 5;
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(1,1,1).normalize();
scene.add(light);

let currentObject;

function loadModel(name) {
  const loader = new OBJLoader();
  loader.load(`/models/${name}`, obj => {
    if (currentObject) scene.remove(currentObject);
    currentObject = obj;
    scene.add(obj);
  });
}

function animate() {
  requestAnimationFrame(animate);
  if (currentObject) currentObject.rotation.y += 0.01;
  renderer.render(scene, camera);
}

document.getElementById('model-select').addEventListener('change', (e) => {
  loadModel(e.target.value);
});

if (document.getElementById('model-select').value) {
  loadModel(document.getElementById('model-select').value);
}
animate();
