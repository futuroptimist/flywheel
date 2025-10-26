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
