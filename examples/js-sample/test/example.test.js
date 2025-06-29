import { hello } from '../src/index.js';

test('hello', () => {
  expect(hello('world')).toBe('Hello, world!');
});
