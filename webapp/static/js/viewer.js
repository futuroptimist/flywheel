import * as THREE from 'three';
import { OBJLoader } from './OBJLoader.js';

const DEFAULT_WIDTH = 800;
const DEFAULT_HEIGHT = 600;
const ROTATE_SPEED = 0.005;
const ZOOM_SPEED = 0.01;
const MIN_Z = 1;
const MAX_Z = 50;

export function createViewer({
  container = document.getElementById('viewer'),
  select = document.getElementById('model-select'),
  three = THREE,
  loader = null,
  loaderFactory = () => new OBJLoader(),
  scheduleFrame = (fn) => requestAnimationFrame(fn),
} = {}) {
  if (!container || !select) {
    return null;
  }

  const width = container.clientWidth || DEFAULT_WIDTH;
  const height = container.clientHeight || DEFAULT_HEIGHT;
  const renderer = new three.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  container.appendChild(renderer.domElement);

  const scene = new three.Scene();
  const camera = new three.PerspectiveCamera(75, width / height, 0.1, 1000);
  camera.position.z = 5;

  const light = new three.DirectionalLight(0xffffff, 1);
  const maybeVector = light.position.set(1, 1, 1);
  if (maybeVector && typeof maybeVector.normalize === 'function') {
    maybeVector.normalize();
  }
  scene.add(light);

  const modelLoader = loader ?? loaderFactory();

  let currentObject = null;

  function loadModel(name) {
    if (!name) {
      return;
    }
    modelLoader.load(`/models/${name}`, (obj) => {
      if (currentObject) {
        scene.remove(currentObject);
      }
      currentObject = obj;
      if (!currentObject.rotation) {
        currentObject.rotation = { x: 0, y: 0, z: 0 };
      }
      scene.add(obj);
    });
  }

  const canvas = renderer.domElement;
  if (typeof canvas.setPointerCapture !== 'function') {
    canvas.setPointerCapture = () => {};
  }
  if (typeof canvas.releasePointerCapture !== 'function') {
    canvas.releasePointerCapture = () => {};
  }

  let isDragging = false;
  let lastX = 0;
  let lastY = 0;
  let activePointerId = null;

  function endDrag(event) {
    if (!isDragging) {
      return;
    }
    isDragging = false;
    if (activePointerId !== null) {
      try {
        canvas.releasePointerCapture(activePointerId);
      } catch (err) {
        // Ignore browsers that throw when capture was not set.
      }
    }
    activePointerId = null;
    event?.preventDefault?.();
  }

  canvas.addEventListener('pointerdown', (event) => {
    if (event.button !== 0) {
      return;
    }
    isDragging = true;
    lastX = event.clientX;
    lastY = event.clientY;
    activePointerId = event.pointerId ?? null;
    if (activePointerId !== null) {
      try {
        canvas.setPointerCapture(activePointerId);
      } catch (err) {
        // Ignore when pointer capture is unsupported.
      }
    }
    event.preventDefault();
  });

  canvas.addEventListener('pointermove', (event) => {
    if (!isDragging || !currentObject) {
      return;
    }
    const dx = event.clientX - lastX;
    const dy = event.clientY - lastY;
    currentObject.rotation.y += dx * ROTATE_SPEED;
    currentObject.rotation.x += dy * ROTATE_SPEED;
    lastX = event.clientX;
    lastY = event.clientY;
    event.preventDefault();
  });

  canvas.addEventListener('pointerup', endDrag);
  canvas.addEventListener('pointerleave', endDrag);
  canvas.addEventListener('pointercancel', endDrag);

  canvas.addEventListener(
    'wheel',
    (event) => {
      event.preventDefault();
      const delta = event.deltaY ?? 0;
      const nextZ = camera.position.z + delta * ZOOM_SPEED;
      camera.position.z = Math.min(MAX_Z, Math.max(MIN_Z, nextZ));
    },
    { passive: false },
  );

  function animate() {
    if (currentObject && currentObject.rotation) {
      currentObject.rotation.y += 0.01;
    }
    renderer.render(scene, camera);
    scheduleFrame(animate);
  }
  scheduleFrame(animate);

  select.addEventListener('change', (event) => {
    loadModel(event.target.value);
  });

  if (select.value) {
    loadModel(select.value);
  }

  return {
    loadModel,
    getCurrentObject: () => currentObject,
    camera,
    scene,
    renderer,
    canvas,
  };
}

if (typeof window !== 'undefined' && !window.__FLYWHEEL_TEST__) {
  createViewer();
}
