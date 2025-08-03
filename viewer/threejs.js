/* eslint-env browser */
import * as THREE from 'https://unpkg.com/three@0.162.0/build/three.module.js';
import { OrbitControls } from 'https://unpkg.com/three@0.162.0/examples/jsm/controls/OrbitControls.js';
import { STLLoader } from 'https://unpkg.com/three@0.162.0/examples/jsm/loaders/STLLoader.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x202020);

const camera = new THREE.PerspectiveCamera(
  45,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
camera.position.set(0, -120, 60);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);

const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1.0);
scene.add(light);

const loader = new STLLoader();
let wheelGroup;

function loadMesh(path, color) {
  return new Promise((resolve) => {
    loader.load(path, (geometry) => {
      geometry.center();
      geometry.computeBoundingSphere();
      const material = new THREE.MeshStandardMaterial({ color });
      const mesh = new THREE.Mesh(geometry, material);
      resolve(mesh);
    });
  });
}

Promise.all([
  loadMesh('../stl/flywheel.stl', 0x777777),
  loadMesh('../stl/shaft.stl', 0x333333),
]).then(([wheel, shaft]) => {
  wheelGroup = new THREE.Group();
  wheelGroup.add(wheel);
  scene.add(wheelGroup);
  scene.add(shaft);
  addBearings(wheel.geometry.boundingSphere.radius - 2);
  animate();
});

function addBearings(radius) {
  const balls = new THREE.Group();
  const ballGeo = new THREE.SphereGeometry(2, 32, 32);
  const ballMat = new THREE.MeshStandardMaterial({ color: 0xffffff });
  const count = 12;
  for (let i = 0; i < count; i += 1) {
    const angle = (i / count) * Math.PI * 2;
    const x = Math.cos(angle) * radius;
    const y = Math.sin(angle) * radius;
    const ball = new THREE.Mesh(ballGeo, ballMat);
    ball.position.set(x, y, 0);
    balls.add(ball);
  }
  wheelGroup.add(balls);
}

function animate() {
  requestAnimationFrame(animate);
  if (wheelGroup) {
    wheelGroup.rotation.z += 0.01;
  }
  controls.update();
  renderer.render(scene, camera);
}

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
