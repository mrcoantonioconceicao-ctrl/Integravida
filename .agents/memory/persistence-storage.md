---
name: Server persistence storage
description: The app uses a small server-side JSON store with a browser backup for persistence.
---
The app keeps records on the server rather than relying only on browser storage; browser storage remains a compatibility backup and migration source.

**Why:** The user needs records to remain available after logging out and returning later, while the project has no database dependency.

**How to apply:** Preserve the server API and atomic file writes when changing record mutations; do not expose or version the runtime data file.