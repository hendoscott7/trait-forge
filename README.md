# Trait Forge

Roll three d20s and get a **belief**, a **habit** and a **flaw** for your character.

- Tap a die or its emblem to reroll it; the d20 button rolls everything that isn't locked.
- Lock the traits you like; lock all three to copy them in one go.
- Tap any trait to copy it.
- Pick an alignment from the grid up top: it shapes the traits and reskins the dice (chaotic evil burns).
- Nat 20s are legendary. Nat 1s are not.
- Tap the logo to switch between dark and light.

One self-contained `index.html`, using three.js from a CDN. No build step.

## Building

Edit `src/index.html`, then run:

```
npm install
npm run build
```

That writes the minified `index.html` the site serves. It needs Python 3 with Pillow and ffmpeg: the build shrinks the sound clips and the logo before minifying.
