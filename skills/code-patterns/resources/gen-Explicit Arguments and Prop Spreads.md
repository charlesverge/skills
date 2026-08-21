# Coding Pattern: Explicit Arguments and Prop Spreads

## Purpose

Use explicit arguments and props when a function or component has a defined contract.

Do not use `...args`, `...props`, or other object-spread patterns as a way to make TypeScript accept code that does not clearly match the target type.

A spread should not hide which values are being passed across a typed boundary.

## Primary rule

When the destination has a small, known, strongly typed contract, pass the values explicitly.

Prefer:

```tsx
render: ({ fresh, review, rewrites }) => (
  <StorybookAppHarness>
    <ResumeReviewChatOutput
      fresh={fresh}
      review={review}
      rewrites={rewrites}
    />
  </StorybookAppHarness>
),
```

Avoid:

```tsx
render: (args) => (
  <StorybookAppHarness>
    <ResumeReviewChatOutput {...args} />
  </StorybookAppHarness>
),
```

The explicit form makes the contract visible and requires TypeScript to validate every field being passed to the component.

## Do not use spreads to work around typing errors

When TypeScript reports that a property no longer exists on a component or function contract, fix the call site to match the current contract.

Do not replace explicit invalid arguments with a spread merely because the spread happens to type-check.

For example, assume the component contract is:

```tsx
export type ResumeReviewChatOutputProps = {
  fresh: boolean;
  review: ReviewResult;
  rewrites: readonly ResumeReviewRewrite[];
};
```

This old call site is incorrect:

```tsx
<ResumeReviewChatOutput
  sessionId="storybook-resume-session"
  review={storybookResumeReview}
  replies={[]}
  fresh={false}
  onResult={() => undefined}
  onError={() => undefined}
  threadId="storybook-thread"
/>
```

The correct fix is not:

```tsx
<ResumeReviewChatOutput {...args} />
```

The correct fix is to remove the obsolete fields and provide the current required fields explicitly:

```tsx
<ResumeReviewChatOutput
  fresh={false}
  review={storybookResumeReview}
  rewrites={[]}
/>
```

If the values originate from Storybook args, destructure the known values and pass them explicitly:

```tsx
render: ({ fresh, review, rewrites }) => (
  <StorybookAppHarness>
    <ResumeReviewChatOutput
      fresh={fresh}
      review={review}
      rewrites={rewrites}
    />
  </StorybookAppHarness>
),
```

## Why the spread form is problematic

A prop spread can make a contract change less visible during review.

Consider:

```tsx
<ResumeReviewChatOutput {...args} />
```

A reviewer cannot determine from that call site which properties are required, which properties are being supplied, or whether obsolete properties remain in the source object.

It also makes future type changes harder to audit because the component boundary no longer documents its dependencies directly.

Explicit arguments provide several benefits:

- The target contract is visible at the call site.
- Removed properties are clearly removed rather than hidden inside another object.
- Newly required properties are visible in the diff.
- Type errors point to the exact property involved.
- Code review can verify that the caller and callee contracts agree.
- Refactors are less likely to accidentally forward unrelated state.
- The implementation cannot silently inherit additional properties added to the source object later.

## Example from the `ResumeReviewChatOutput` change

### Incorrect original state

The Storybook consumer still used an older component contract:

```tsx
<ResumeReviewChatOutput
  sessionId="storybook-resume-session"
  review={storybookResumeReview}
  replies={[]}
  fresh={false}
  onResult={() => undefined}
  onError={() => undefined}
  threadId="storybook-thread"
/>
```

TypeScript correctly reported that fields such as `sessionId` no longer existed.

The current component contract had become:

```tsx
type ResumeReviewChatOutputProps = {
  fresh: boolean;
  review: ReviewResult;
  rewrites: readonly ResumeReviewRewrite[];
};
```

### What not to do

Do not conceal the mismatch behind Storybook's aggregate `args` object:

```tsx
render: (args) => (
  <StorybookAppHarness>
    <ResumeReviewChatOutput {...args} />
  </StorybookAppHarness>
),
```

Although Storybook may infer the aggregate object from the component metadata, this removes useful visibility from the actual component invocation.

It turns an explicit contract correction into an indirect forwarding mechanism.

### What to do

Declare the valid Storybook args:

```tsx
const meta = {
  component: ResumeReviewChatOutput,
  args: {
    fresh: false,
    review: storybookResumeReview,
    rewrites: [],
  },
} satisfies Meta<typeof ResumeReviewChatOutput>;
```

Then explicitly carry those values through the render boundary:

```tsx
render: ({ fresh, review, rewrites }) => (
  <StorybookAppHarness>
    <ResumeReviewChatOutput
      fresh={fresh}
      review={review}
      rewrites={rewrites}
    />
  </StorybookAppHarness>
),
```

This preserves Storybook controls while keeping the component contract explicit.

## Acceptable uses of `...args` or `...props`

Object spreading is not universally prohibited.

It can be appropriate when forwarding an intentionally open or library-defined contract where transparent forwarding is the actual design.

For example, a thin wrapper around a native element may intentionally forward native attributes:

```tsx
type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement>;

function Button({ className, ...props }: ButtonProps) {
  return (
    <button
      className={className}
      {...props}
    />
  );
}
```

Here, forwarding arbitrary `ButtonHTMLAttributes` is part of the declared contract.

Another valid case is immutable object construction:

```ts
const nextState = {
  ...currentState,
  status: 'complete',
};
```

This is not hiding a function or component boundary.

## When spreading should be rejected

Do not use a spread at a typed call boundary when any of the following are true:

- The target function or component has a small, known parameter set.
- The spread was introduced while fixing a TypeScript error.
- Properties were recently removed or renamed.
- The source object contains more fields than the destination requires.
- The change makes it harder to determine which values cross the boundary.
- The spread prevents reviewers from confirming that obsolete arguments were removed.
- The spread exists primarily because listing the arguments explicitly causes a type error.
- The source and destination types are maintained independently.
- A contract migration is in progress.

If explicit arguments fail type checking while a spread succeeds, treat that as a reason to investigate the types rather than a reason to keep the spread.

## Type-error workflow

When a typed call site fails:

1. Read the destination type or function signature.
1. Identify the exact current required properties.
1. Remove properties that no longer exist.
1. Add any newly required properties from their correct source.
1. Pass the values explicitly.
1. Run the type checker.
1. Do not introduce a spread solely to make the error disappear.

For example:

```tsx
type Props = {
  review: ReviewResult;
  rewrites: readonly ResumeReviewRewrite[];
  fresh: boolean;
};
```

Use:

```tsx
<Component
  review={review}
  rewrites={rewrites}
  fresh={fresh}
/>
```

Do not use:

```tsx
<Component {...values} />
```

unless forwarding the complete `values` contract is itself an intentional architectural requirement.

## Review guidance

When reviewing a change that introduces `...args` or `...props`, ask:

- What exact properties are being forwarded?
- Is forwarding arbitrary properties part of the destination contract?
- Would explicit arguments be clearer?
- Was the spread introduced while resolving a typing failure?
- Does the source object contain fields the destination should not receive?
- Could a future property added to the source object cross this boundary unintentionally?
- Does the spread make a contract migration harder to review?

If the spread exists only to avoid enumerating a known contract, prefer explicit arguments.

## Rule summary

Use spreads for intentional object composition or genuinely open forwarding contracts.

Do not use spreads as typing escape hatches.

For known component and function contracts, especially during contract migrations, explicitly pass every required value and remove every obsolete value.

A TypeScript error should be resolved by bringing the caller into agreement with the actual contract, not by obscuring the caller behind `...args`.
