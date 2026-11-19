// news-image-20261119-r2 — entrypoint.
// Copies the composed front page (entry.png, built by compose.py) to the
// output directory. No network, no clock, no randomness: the same repo
// always produces the same bytes.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
