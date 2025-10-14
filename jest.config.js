export default {
  collectCoverageFrom: [
    'webapp/static/js/viewer.js'
  ],
  coveragePathIgnorePatterns: [
    '<rootDir>/examples/',
    'OBJLoader.js',
    'three.core.min.js',
    'three.module.min.js'
  ],
  coverageThreshold: {
    global: {
      branches: 55,
      functions: 50,
      lines: 80,
      statements: 80
    }
  },
  testPathIgnorePatterns: [
    '/node_modules/',
    '/tests/js/.*\\.spec\\.js$'
  ]
};
