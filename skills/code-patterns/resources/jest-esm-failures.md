# Jest ESM Dependency Transformation Override

## Rule

When Jest fails while parsing an ESM-only dependency under `node_modules`, it
is permitted to define a narrow `transformIgnorePatterns` exception in the
Jest configuration.

For projects using `next/jest`, it is also permitted to await the configuration
created by `nextJest` and replace its resolved `transformIgnorePatterns` value.
This replacement is necessary when a Next-generated ignore pattern would
otherwise take precedence over the project exception.

This is an accepted test-runner configuration pattern, not a compatibility
workaround in application code.

## Required diagnosis

Use this pattern only after confirming all of the following:

- Jest reports a parse-time syntax error such as `Unexpected token 'export'`
  or `Cannot use import statement outside a module`.
- The failing file belongs to an ESM dependency under `node_modules`.
- Jest's effective configuration excludes that dependency from transformation.
- The direct dependency and the ESM transitive dependency chain responsible for
  the failure have been identified.

Do not use this pattern for module-resolution errors, incorrect mocks, missing
exports, application syntax errors, or test-environment initialization errors.

## Approved pattern

Keep the exception as a negative lookahead that continues to ignore unrelated
packages:

```ts
const config: Config = {
  transformIgnorePatterns: [
    '/node_modules/(?!(?:allowed-package|allowed-scope|transitive-esm-package)/)',
  ],
};
```

When `next/jest` appends project patterns after its own `node_modules` ignore
patterns, replace the final value after resolving the generated configuration:

```ts
const buildJestConfig = createJestConfig(config);

export default async (): Promise<Config> => {
  const resolvedConfig = await buildJestConfig();
  return {
    ...resolvedConfig,
    transformIgnorePatterns: config.transformIgnorePatterns,
  };
};
```

Jest skips transformation when any ignore pattern matches. Appending a project
negative lookahead does not cancel an earlier broad `node_modules` match, which is
why replacing the resolved value is permitted in this case.

## Allowlist scope

- Include only packages proven to participate in the failing import chain.
- Include required ESM transitive dependencies; naming only the direct package
  is insufficient when its dependencies are separate `node_modules` packages.
- Permit package-family expressions such as `micromark[^/]*` or
  `mdast-util-[^/]+` only when multiple members of that family occur in the
  verified dependency chain.
- Keep unrelated `node_modules` packages ignored.
- Do not transform all of `node_modules`.
- Do not remove the override merely because the same direct package appears in
  Next's `transpilePackages`; verify whether its ESM transitive dependencies are
  covered by Jest's effective configuration first.

## Validation

- Run a test that imports the real dependency path which previously failed.
- Confirm the parse-time error is resolved without mocking the failing module.
- Run the related Jest test group to detect configuration regressions.
- Inspect Jest's effective configuration after framework or Jest upgrades.
- Remove an allowlisted package only after a real import of the affected path
  succeeds without that exception.
