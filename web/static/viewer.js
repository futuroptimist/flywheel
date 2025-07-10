import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';
import { OBJLoader } from 'https://unpkg.com/three@0.160.0/examples/jsm/loaders/OBJLoader.js';
import { OrbitControls } from 'https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js';

export function init(objPath) {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.getElementById('viewer').appendChild(renderer.domElement);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.addEventListener('change', render);
  window.viewerControls = controls;

  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(1, 1, 1).normalize();
  scene.add(light);

  const loader = new OBJLoader();
  loader.load(objPath, (object) => {
    scene.add(object);
    resetView();
    animate();
  });

  camera.position.z = 5;

  function animate() {
    requestAnimationFrame(animate);
    controls.update();
  }

  function render() {
    renderer.render(scene, camera);
  }

  function resetView() {
    controls.reset();
    render();
  }

  window.addEventListener('dblclick', resetView);
}

window.init = init;
