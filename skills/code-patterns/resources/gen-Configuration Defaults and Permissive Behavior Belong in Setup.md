# Coding Pattern Rule: Configuration Defaults and Permissive Behavior Belong in Setup

## Context

Test infrastructure, development tooling, and application bootstrap code may intentionally define defaults or permissive behavior needed to establish a predictable execution environment.

Examples include:

- allowing a test command to succeed when no tests match;
- assigning a default test database connection;
- supplying development-only configuration defaults;
- configuring test-runner behavior;
- installing global test polyfills or environment-specific setup.

These behaviors are valid when they are intentionally defined in the configuration or setup layer responsible for establishing that environment.

## Pattern to Use

Define defaults and execution-policy decisions explicitly in the configuration or setup boundary that owns them.

A test runner may intentionally allow an empty test selection:

```ts
const config = {
  passWithNoTests: true,
};
```

Test setup may provide a default environment value when the caller did not supply one:

```ts
if (process.env.MONGODB_URI === undefined) {
  process.env.MONGODB_URI = 'mongodb://localhost:27017/test';
}
```

The default must preserve an explicitly supplied value. Setup establishes the environment; application and feature code consume it.

Defaults should therefore follow this pattern:

```ts
if (configurationValue === undefined) {
  configurationValue = DEFAULT_VALUE;
}
```

rather than overwriting an explicit configuration:

```ts
configurationValue = DEFAULT_VALUE;
```

Configuration behavior should remain centralized and discoverable in the relevant setup or configuration files.

## Pattern Not to Use

Do not move setup-owned defaults or execution-policy decisions into feature, component, domain, transport, or business-logic code.

For example, application code should not repair missing process configuration:

```ts
async function loadData() {
  if (process.env.MONGODB_URI === undefined) {
    process.env.MONGODB_URI = 'mongodb://localhost:27017/test';
  }

  // ...
}
```

Do not:

- mutate process environment variables from ordinary application code;
- introduce test-environment defaults from individual tests or components;
- duplicate the same default across multiple implementation layers;
- overwrite explicitly supplied configuration values with defaults;
- add feature-level fallback behavior to compensate for test-runner configuration;
- treat valid setup/configuration features as workarounds solely because they change default tool behavior.

## Rule

Setup and configuration layers may intentionally define defaults, permissive behavior, and environment initialization.

Defaults must apply only when the corresponding value is absent and must not override explicit configuration.

Outside the owning setup or configuration boundary, code must consume the established configuration rather than mutate, duplicate, or repair it.
