/**
 * Convert CrimeMatrix SVGs to high-quality PNGs for README / PPT.
 * Usage: node docs/scripts/render-diagrams.mjs
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { dirname, join, basename } from 'node:path'
import { fileURLToPath } from 'node:url'
import { Resvg } from '@resvg/resvg-js'

const __dirname = dirname(fileURLToPath(import.meta.url))
const root = join(__dirname, '..', '..')

const jobs = [
  { svg: 'docs/diagrams/01-user-flow-sequence.svg', png: 'docs/diagrams/01-user-flow-sequence.png', width: 1920 },
  { svg: 'docs/diagrams/02-hybrid-architecture.svg', png: 'docs/diagrams/02-hybrid-architecture.png', width: 1920 },
  { svg: 'docs/diagrams/03-use-case-map.svg', png: 'docs/diagrams/03-use-case-map.png', width: 1920 },
  { svg: 'docs/diagrams/04-ai-crime-intelligence-ecosystem.svg', png: 'docs/diagrams/04-ai-crime-intelligence-ecosystem.png', width: 1920 },
  { svg: 'docs/assets/readme-hero.svg', png: 'docs/assets/readme-hero.png', width: 1600 },
  { svg: 'docs/assets/readme-impact.svg', png: 'docs/assets/readme-impact.png', width: 1600 },
]

for (const job of jobs) {
  const svgPath = join(root, job.svg)
  const pngPath = join(root, job.png)
  mkdirSync(dirname(pngPath), { recursive: true })
  // Force UTF-8 string; strip BOM / stray control chars that break resvg
  let svg = readFileSync(svgPath, 'utf8')
  svg = svg.replace(/^\uFEFF/, '').replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '-')
  const resvg = new Resvg(svg, {
    fitTo: { mode: 'width', value: job.width },
    font: { loadSystemFonts: true },
    background: 'transparent',
  })
  const png = resvg.render().asPng()
  writeFileSync(pngPath, png)
  console.log(`OK  ${basename(pngPath)}  (${png.length} bytes)`)
}
