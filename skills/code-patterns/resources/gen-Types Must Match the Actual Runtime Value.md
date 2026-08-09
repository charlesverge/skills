# Coding Pattern Rule: Types Must Match the Actual Runtime Value

## Context

When TypeScript reports that a value does not satisfy the required type, fix the value construction, type definition, library declaration, or call site that causes the mismatch.

The type system must describe the structure that actually exists at runtime. Compiler configuration, assertions, or suppression mechanisms must not be used to make an incompatible value appear compatible.

This applies especially when:

- composing functions or React components with attached static properties;
- adapting third-party library types;
- constructing objects incrementally;
- resolving declaration-file errors;
- satisfying generic or intersection types;
- addressing compiler errors introduced by dependencies.

## Pattern to Use

Construct the value so its runtime structure naturally satisfies the required type.

For compound values, create the complete structure in a typed operation:

```ts
const Component = Object.assign(memo(ComponentImpl), {
  Root: ComponentRoot,
  Trigger: ComponentTrigger,
  Content: ComponentContent,
});
```

When an explicit type is useful, validate the constructed value against that type:

```ts
const Component: CompoundComponent = Object.assign(
  memo(ComponentImpl),
  {
    Root: ComponentRoot,
    Trigger: ComponentTrigger,
    Content: ComponentContent,
  },
);
```

This ensures that:

1. the properties actually exist at runtime;
1. TypeScript verifies their names and types;
1. future changes that violate the contract produce a compiler error.

Keep normal compiler checks enabled. If declaration checking exposes an error, resolve the actual incompatibility at its source.

For example:

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

If a third-party declaration is incorrect, address the dependency, declaration, usage, or supported upstream typing mechanism rather than disabling checking for all declarations.

## Pattern Not to Use

Do not make a value appear to have a type that its construction does not establish.

Do not use double assertions such as:

```ts
const Component = memo(ComponentImpl) as unknown as CompoundComponent;

Component.Root = ComponentRoot;
Component.Trigger = ComponentTrigger;
Component.Content = ComponentContent;
```

The assertion tells the compiler to trust a type that has not yet been demonstrated by the value. It bypasses the exact verification the type checker is intended to provide.

Do not disable compiler checking to make type errors disappear:

```json
{
  "compilerOptions": {
    "skipLibCheck": true
  }
}
```

Do not substitute similar mechanisms such as:

- `as unknown as SomeType`;
- `as any`;
- `@ts-ignore`;
- `@ts-expect-error` used to bypass a production incompatibility;
- weakening a specific type to `unknown`, `object`, or a broad union;
- adding wrapper or alias types solely to hide an incompatibility;
- globally disabling type-checker rules;
- excluding problematic source or declaration files from checking.

## Rule

A type error must be resolved by making the implementation and its declared contract agree.

Prefer construction patterns that let TypeScript verify the real runtime shape.

Never use assertions, suppressions, compiler exclusions, or weakened types as a substitute for establishing the required structure correctly.
