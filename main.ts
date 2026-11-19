// news-image-20261119-r2 — entrypoint.
// Copies the composed front page (entry.png, built by compose.py) to the
// output directory, then verifies the copy landed whole. No network, no
// clock, no randomness: the same repo always produces the same bytes.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "entry.png");
const dest = join(outDir, "entry.png");
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
if (statSync(src).size !== statSync(dest).size) {
  throw new Error(`copy mismatch: ${src} did not land whole at ${dest}`);
}
