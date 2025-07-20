const mv = document.getElementById('mv');
const explode = document.getElementById('explode');
const legend = document.getElementById('legend');
const dark = document.getElementById('dark');
let nodes = [];

mv.addEventListener('load', () => {
  const scene = mv.model?.scene;
  if (!scene) return;
  nodes = scene.children;
  legend.innerHTML = '';
  nodes.forEach((n, i) => {
    const li = document.createElement('li');
    li.textContent = n.name || `part-${i}`;
    li.onclick = () => {
      if (li.classList.toggle('hidden')) {
        n.visible = false;
      } else {
        const solo = legend.querySelector('.solo');
        if (solo && solo !== li) {
          nodes.forEach((m) => (m.visible = true));
          solo.classList.remove('solo');
        }
        if (li.classList.toggle('solo')) {
          nodes.forEach((m, j) => (m.visible = j === i));
        } else {
          nodes.forEach((m) => (m.visible = true));
        }
      }
    };
    legend.appendChild(li);
  });
});

explode.addEventListener('input', () => {
  const f = parseFloat(explode.value);
  nodes.forEach((n, i) => {
    n.position.z = i * f * 10;
  });
});

dark.addEventListener('click', () => {
  document.body.classList.toggle('dark');
});
