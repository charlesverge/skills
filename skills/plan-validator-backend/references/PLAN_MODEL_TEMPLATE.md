# Model name

- Once sentence describing the model's purpose and what it represents.

## Stored record structure

The session record is the authentication record. `verify` creates it, so this plan owns its shape;
`plans/api/auth-session.md` reads it, `plans/api/auth-terms.md` operates under it, and
`plans/api/auth-logout.md` revokes it.

- **Database:** `zoracrew`
- **Collection:** `sessions`
- **Document fields:**
  - `_id`: `ObjectId`
  - `session_id`: `string` — opaque session token value carried in the `zc_session` cookie (the lookup key).
  - `user_id`: `string` — authenticated account the session belongs to.
  - `created_at`: `Date` — when the session was established by verify.
  - `expires_at`: `Date` — `created_at + 30 days`; bumped another 30 days from the request on each authenticated visit (sliding renewal).
  - `last_seen_at`: `Date` — last authenticated request time; drives the sliding renewal.
  - `revoked_at`: `Date | null` — set when logout revokes the session; `null` while active.
  - `ip`: `string` — client IP captured at creation (`clientIp(req)`).
  - `user_agent`: `string` — client user agent captured at creation (`clientUserAgent(req)`).
- **Index:** `{ session_id: 1 }` (unique) for cookie lookup, plus `{ user_id: 1 }` to revoke a user's sessions.
- **Validity:** a session is valid when `revoked_at` is `null` and `now < expires_at`; logout sets `revoked_at` and clears the cookie (`plans/api/auth-logout.md`).

## Common queries

- Create session: insert a new document with `session_id`, `user_id`, `created_at`, `expires_at`, `last_seen_at`, `revoked_at: null`, `ip`, and `user_agent`.
- Validate session: find document by `session_id`, check `revoked_at` is `null` and `expires_at` is in the future, update `last_seen_at` to now

## Related APIs

- `plan-file.md` - Short description of the API use of the model. ie - `auth-session.md` - Read auth session state

