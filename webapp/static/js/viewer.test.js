/** @jest-environment jsdom */

import { jest } from '@jest/globals';

function createThreeStub() {
  class WebGLRenderer {
    constructor() {
      this.domElement = document.createElement('canvas');
      this.domElement.setPointerCapture = jest.fn();
      this.domElement.releasePointerCapture = jest.fn();
    }
    setSize = jest.fn();
    render = jest.fn();
  }

  class Scene {
    constructor() {
      this.objects = [];
    }
    add(obj) {
      this.objects.push(obj);
    }
    remove(obj) {
      this.objects = this.objects.filter((item) => item !== obj);
    }
  }

  class PerspectiveCamera {
    constructor() {
      this.position = { z: 0 };
    }
  }

  class DirectionalLight {
    constructor() {
      const normalize = jest.fn();
      this.position = {
        set: jest.fn(() => ({ normalize })),
      };
    }
  }

  return { WebGLRenderer, Scene, PerspectiveCamera, DirectionalLight };
}

beforeAll(() => {
  if (typeof window !== 'undefined' && !window.PointerEvent) {
    class PointerEvent extends window.MouseEvent {
      constructor(type, props = {}) {
        super(type, props);
        this.pointerId = props.pointerId ?? 1;
      }
    }
    window.PointerEvent = PointerEvent;
    global.PointerEvent = PointerEvent;
  }
});

beforeEach(() => {
  jest.resetModules();
  globalThis.__FLYWHEEL_TEST__ = true;
  document.body.innerHTML = `
    <div id="viewer"></div>
    <select id="model-select">
      <option value="model1.obj" selected>model1.obj</option>
    </select>
  `;
});

afterEach(() => {
  delete globalThis.__FLYWHEEL_TEST__;
});

const scheduleNoop = () => {};

it('rotates the model when dragging with the pointer', async () => {
  const loaderStub = {
    load: jest.fn((path, onLoad) => {
      loaderStub.path = path;
      loaderStub.onLoad = onLoad;
    }),
  };
  const threeStub = createThreeStub();
  const { createViewer } = await import('./viewer.js');
  const viewer = createViewer({
    three: threeStub,
    loaderFactory: () => loaderStub,
    scheduleFrame: scheduleNoop,
  });

  expect(loaderStub.load).toHaveBeenCalledWith('/models/model1.obj', expect.any(Function));

  const model = { rotation: { x: 0, y: 0, z: 0 } };
  loaderStub.onLoad(model);
  const canvas = viewer.canvas;

  canvas.dispatchEvent(
    new window.PointerEvent('pointerdown', {
      pointerId: 1,
      button: 0,
      clientX: 10,
      clientY: 10,
    }),
  );
  canvas.dispatchEvent(
    new window.PointerEvent('pointermove', {
      pointerId: 1,
      clientX: 30,
      clientY: 0,
    }),
  );
  canvas.dispatchEvent(
    new window.PointerEvent('pointerup', {
      pointerId: 1,
    }),
  );

  expect(model.rotation.y).toBeGreaterThan(0);
  expect(model.rotation.x).toBeLessThan(0);
});

it('zooms the camera with the mouse wheel', async () => {
  const loaderStub = {
    load: jest.fn((path, onLoad) => {
      loaderStub.onLoad = onLoad;
    }),
  };
  const threeStub = createThreeStub();
  const { createViewer } = await import('./viewer.js');
  const viewer = createViewer({
    three: threeStub,
    loaderFactory: () => loaderStub,
    scheduleFrame: scheduleNoop,
  });
  loaderStub.onLoad({ rotation: { x: 0, y: 0, z: 0 } });

  const canvas = viewer.canvas;
  const initialZ = viewer.camera.position.z;

  const zoomOutEvent = new window.WheelEvent('wheel', { deltaY: 120 });
  const preventSpy = jest.spyOn(zoomOutEvent, 'preventDefault');
  canvas.dispatchEvent(zoomOutEvent);
  expect(preventSpy).toHaveBeenCalled();
  const afterZoomOut = viewer.camera.position.z;
  expect(afterZoomOut).toBeGreaterThan(initialZ);

  const zoomInEvent = new window.WheelEvent('wheel', { deltaY: -480 });
  canvas.dispatchEvent(zoomInEvent);
  expect(viewer.camera.position.z).toBeLessThan(afterZoomOut);
  expect(viewer.camera.position.z).toBeGreaterThanOrEqual(1);
});
