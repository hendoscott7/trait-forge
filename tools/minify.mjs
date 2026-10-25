import { readFileSync, writeFileSync } from "node:fs";
import { minify } from "html-minifier-terser";

const [, , input, output] = process.argv;
const html = readFileSync(input, "utf8");
const out = await minify(html, {
  collapseWhitespace: true,
  removeComments: true,
  removeRedundantAttributes: true,
  removeScriptTypeAttributes: true,
  removeStyleLinkTypeAttributes: true,
  useShortDoctype: true,
  minifyCSS: { level: 1 },
  minifyJS: { compress: { passes: 2 }, mangle: { toplevel: true }, format: { comments: false } },
});
writeFileSync(output, out);
