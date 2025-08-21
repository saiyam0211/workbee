## Project structure

- `src/pages` default route containers (e.g., `Landing`)
- `src/components/ui` shadcn-style colocated UI primitives
- `src/lib/utils.ts` `cn` helper
- `src/styles/globals.css` Tailwind base and tokens (imported by `src/index.css`)

## shadcn CLI (optional)
If you want to scaffold more components the shadcn way:

1. Install CLI: `npx shadcn@latest init`
2. Set components path to `src/components/ui`
3. When generating components, the CLI will place files under `src/components/ui` and rely on `@/lib/utils`.
