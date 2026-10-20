import { constants } from 'node:fs';
import {
  lstat,
  open,
  readFile,
  realpath,
  rename,
  unlink,
} from 'node:fs/promises';
import { dirname, resolve, join } from 'node:path';
import { randomUUID } from 'node:crypto';

// Fail closed where POSIX permissions cannot demonstrate private storage. No ACL changes.
// The operator supplies a dedicated existing 0700 directory outside any checkout.
export async function privateCheckpoint(path) {
  if (process.platform === 'win32' || !process.getuid) throw new Error();
  const target = resolve(path);
  const parent = dirname(target);
  const directory = await lstat(parent);
  if (
    !directory.isDirectory() ||
    directory.isSymbolicLink() ||
    directory.uid !== process.getuid() ||
    (directory.mode & 0o077) !== 0 ||
    (await realpath(parent)) !== parent
  )
    throw new Error();
  for (let ancestor = parent; ; ancestor = dirname(ancestor)) {
    try {
      await lstat(join(ancestor, '.git'));
      throw new Error();
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
    }
    if (ancestor === dirname(ancestor)) break;
  }
  const lockPath = join(parent, '.attribution-scan.lock');
  const lock = await open(
    lockPath,
    constants.O_CREAT | constants.O_EXCL | constants.O_WRONLY,
    0o600
  );
  let temporary;
  const check = async () => {
    try {
      const stat = await lstat(target);
      if (
        !stat.isFile() ||
        stat.isSymbolicLink() ||
        stat.nlink !== 1 ||
        stat.uid !== process.getuid() ||
        (stat.mode & 0o077) !== 0 ||
        stat.size > 8 * 1024 * 1024
      )
        throw new Error();
      return true;
    } catch (error) {
      if (error.code === 'ENOENT') return false;
      throw error;
    }
  };
  return {
    async load() {
      if (!(await check())) return null;
      return JSON.parse(await readFile(target, 'utf8'));
    },
    async save(state) {
      await check();
      const bytes = JSON.stringify(state);
      if (Buffer.byteLength(bytes) > 8 * 1024 * 1024) throw new Error();
      temporary = join(parent, `.attribution-${randomUUID()}.tmp`);
      const file = await open(
        temporary,
        constants.O_CREAT | constants.O_EXCL | constants.O_WRONLY,
        0o600
      );
      try {
        await file.writeFile(bytes, 'utf8');
        await file.sync();
      } finally {
        await file.close();
      }
      await rename(temporary, target);
      temporary = undefined;
      const dir = await open(parent, constants.O_RDONLY);
      try {
        await dir.sync();
      } finally {
        await dir.close();
      }
    },
    async close() {
      try {
        if (temporary) await unlink(temporary);
      } finally {
        await lock.close();
        await unlink(lockPath);
      }
    },
  };
}
