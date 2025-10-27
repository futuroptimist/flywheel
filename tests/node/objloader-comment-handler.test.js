import { OBJLoader } from '../../webapp/static/js/OBJLoader.js';

test('OBJLoader forwards comments to a registered handler', () => {
  const loader = new OBJLoader();
  const seen = [];

  const chained = loader.setCommentHandler((comment, lineNumber, rawLine) => {
    seen.push({ comment, lineNumber, rawLine });
  });

  expect(chained).toBe(loader);

  const objData = `# header comment
v 0 0 0
v 1 0 0
v 0 1 0
# trailing note
f 1 2 3
`;

  const group = loader.parse(objData);

  expect(group).toBeDefined();
  expect(group.isGroup).toBe(true);
  expect(seen).toEqual([
    { comment: 'header comment', lineNumber: 1, rawLine: '# header comment' },
    { comment: 'trailing note', lineNumber: 5, rawLine: '# trailing note' },
  ]);
});

test('OBJLoader splits smoothing groups without explicit materials', () => {
  const loader = new OBJLoader();

  const objData = `v 0 0 0
v 1 0 0
v 0 1 0
v 0 0 1
s 1
f 1 2 3
s off
f 1 3 4
`;

  const group = loader.parse(objData);

  expect(group.children).toHaveLength(1);
  const mesh = group.children[0];

  expect(Array.isArray(mesh.material)).toBe(true);
  expect(mesh.material).toHaveLength(2);
  expect(mesh.material[0].flatShading).toBe(false);
  expect(mesh.material[1].flatShading).toBe(true);

  expect(mesh.geometry.groups).toHaveLength(2);
  const [firstGroup, secondGroup] = mesh.geometry.groups;
  expect(firstGroup.count).toBeGreaterThan(0);
  expect(secondGroup.count).toBeGreaterThan(0);
  expect(secondGroup.start).toBe(firstGroup.start + firstGroup.count);
});
