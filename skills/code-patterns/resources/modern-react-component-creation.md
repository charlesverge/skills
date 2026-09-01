# Modern React Component Creation Without Module-Scope Mutation

## Purpose

Use this pattern when creating or updating React function components, especially components that accept refs, use `memo`, or expose related component parts.

Components must be fully defined when their module-scoped binding is created. Do not mutate the component, another module-scoped value, or a global object after declaration to add metadata or behavior.

## Default component pattern

Define a named function component. Its declaration provides the component name used by React debugging tools and component stacks.

```tsx
type StatusBadgeProps = {
  label: string;
};

export function StatusBadge({ label }: StatusBadgeProps) {
  return <span>{label}</span>;
}
```

Do not export an anonymous component and then assign a name later.

## React 19 ref pattern

React 19 supports `ref` as a function-component prop. New components should accept the correctly typed ref through their props and pass it directly to the owning element or component.

```tsx
import type { ComponentPropsWithRef } from 'react';

type TooltipIconButtonProps = ComponentPropsWithRef<'button'> & {
  tooltip: string;
};

export function TooltipIconButton({
  children,
  tooltip,
  ref,
  ...props
}: TooltipIconButtonProps) {
  return (
    <button ref={ref} aria-label={tooltip} {...props}>
      {children}
    </button>
  );
}
```

Do not introduce `forwardRef` for a new React 19 component. Do not preserve `forwardRef` merely for backward compatibility unless backward compatibility is explicitly required.

## Existing `forwardRef` components

Prefer migrating an existing component to the React 19 ref-prop pattern when its actual dependency and caller contracts support that migration.

When a framework or library contract still requires `forwardRef`, pass it a named render function. The name belongs to the function definition and does not require a later mutation.

```tsx
import { forwardRef, type ComponentPropsWithoutRef } from 'react';

type TooltipIconButtonProps = ComponentPropsWithoutRef<'button'> & {
  tooltip: string;
};

export const TooltipIconButton = forwardRef<HTMLButtonElement, TooltipIconButtonProps>(
  function TooltipIconButton({ children, tooltip, ...props }, ref) {
    return (
      <button ref={ref} aria-label={tooltip} {...props}>
        {children}
      </button>
    );
  },
);
```

## Memoized components

Give the function passed to `memo` a name. Do not add the name by mutating the returned component.

```tsx
import { memo } from 'react';

type ReasoningProps = {
  text: string;
};

export const Reasoning = memo(function Reasoning({ text }: ReasoningProps) {
  return <div>{text}</div>;
});
```

Only use `memo` when it is already required by the component contract or justified by an observed rendering cost. Naming a component does not require `memo`.

## Related component parts

Prefer named exports for related parts. Each part remains independently named, typed, and importable without attaching properties to another component.

```tsx
import type { ReactNode } from 'react';

type ReasoningPartProps = {
  children: ReactNode;
};

export function ReasoningRoot({ children }: ReasoningPartProps) {
  return <section>{children}</section>;
}

export function ReasoningTrigger({ children }: ReasoningPartProps) {
  return <button type="button">{children}</button>;
}

export function ReasoningContent({ children }: ReasoningPartProps) {
  return <div>{children}</div>;
}
```

If a new API has an immediate requirement for `Parts.Root` property access, construct a non-callable namespace with one object literal.

```tsx
export const ReasoningParts = {
  Root: ReasoningRoot,
  Trigger: ReasoningTrigger,
  Content: ReasoningContent,
} as const;
```

Do not make one value serve as both a callable component and a mutable namespace. Migrating an existing callable compound-component API requires updating its callers and public contract. If that change is outside the requested scope, report the conflict instead of hiding the mutation.

## Prohibited patterns

Do not assign `displayName` after creating a component.

```tsx
export const TooltipIconButton = forwardRef<HTMLButtonElement, TooltipIconButtonProps>(
  (props, ref) => <button ref={ref} {...props} />,
);

TooltipIconButton.displayName = 'TooltipIconButton';
```

Do not move the mutation into the initializer with `Object.assign`.

```tsx
export const TooltipIconButton = Object.assign(
  forwardRef<HTMLButtonElement, TooltipIconButtonProps>(
    (props, ref) => <button ref={ref} {...props} />,
  ),
  { displayName: 'TooltipIconButton' },
);
```

Do not use `Object.defineProperty`, `Reflect.set`, an alias, a factory, or a helper to perform the same mutation. A mutation executed while initializing a module is still a module-scope mutation, even when its target was created immediately beforehand.

## Migration decision sequence

1. Identify whether the assignment changes rendering behavior or only supplies debugging metadata.
1. Replace debugging metadata assignments with a named component function.
1. For React 19 code, accept `ref` through typed props and remove unnecessary `forwardRef` usage.
1. If `forwardRef` is still required, use a named render function.
1. Replace attached component parts with named exports or an immutable object-literal namespace when the requested scope permits the API change.
1. If preserving the current public API requires module-scope mutation and changing that API is not authorized, skip the file and report the architectural conflict.

## Review checklist

- The component function has a meaningful name at declaration.
- React 19 components receive `ref` as a typed prop.
- `forwardRef` is used only when an existing contract requires it.
- A `forwardRef` or `memo` callback is named.
- No component property is assigned after declaration.
- No `Object.assign`, `Object.defineProperty`, `Reflect.set`, alias, factory, or helper hides module-scope mutation.
- Related component parts use named exports or a non-callable object literal.
- Any public compound-component API migration updates all callers and tests in the authorized scope.

## References

- [React `forwardRef` reference](https://react.dev/reference/react/forwardRef "React forwardRef reference")
- [React 19 ref as a prop](https://react.dev/blog/2024/12/05/react-19#ref-as-a-prop "React 19 ref as a prop")
- [React component importing and exporting guidance](https://react.dev/learn/importing-and-exporting-components "React component naming guidance")
