# Dependency security updates

The October 2026 repair addresses GitHub's Dependabot alerts with these minimum versions:

| Package                 | Required minimum                       |
| ----------------------- | -------------------------------------- |
| Vite                    | 6.4.5                                  |
| esbuild                 | 0.25.0 or newer, resolved through Vite |
| Zod                     | 4.6.6                                  |
| source-map-js           | 1.2.2                                  |
| postcss-selector-parser | 6.1.5                                  |
| uuid                    | 11.1.1                                 |

The `firebase-admin` override replaces uuid 9 in its Google Cloud dependencies.
Those consumers use the CommonJS `v4()` API, which uuid 11 retains. Keep this
override until an upstream Firebase/Google Cloud update resolves a patched uuid
without it. Do not substitute uuid 12 or newer without reviewing CommonJS support.

Vite scans the application's `index.html` entry only. Generated previews, build
outputs, and runtime data are excluded from its watcher to avoid unnecessary
dependency scans and reloads during local development.

Verify updates with `npm run test:backend`, `npm run test:client`, and the Vite
production build. Also check the resolved lockfile against GitHub's advisory
ranges: the npm audit service reported zero findings while GitHub still had open
alerts during this repair.
