# Third-party package patching is prohibited

Do not modify installed third-party packages to make their code, types, declarations, imports, exports, or runtime behavior work with this project.

The following patterns are prohibited:

- `patch-package` or equivalent post-install patching tools.
- Committed `patches/**` files that modify dependency contents.
- `postinstall`, `prepare`, or other install hooks that rewrite dependencies.
- Direct changes to files under `node_modules`.
- Local declaration patches that alter a dependency's published `.d.ts` files.
- Runtime monkey-patching or module replacement used to correct an incompatible dependency.
- TypeScript/compiler suppressions added solely because a dependency is being used incorrectly or through an incompatible API.

When a dependency produces a type, import, export, declaration, or runtime error, first identify how the project is using that module.

The required resolution is to fix the project at the dependency boundary by doing one of the following:

1. Use the dependency's supported public API correctly.
1. Import the symbol from its canonical supported module.
1. Use the correct API, type, component, primitive, or execution path for the installed dependency version.
1. Align related dependency versions when the project has installed an incompatible combination.
1. Upgrade or downgrade to a dependency release whose supported contract matches the project requirements.
1. Replace the dependency if no supported version provides the required contract.

Do not alter the dependency itself to preserve an incorrect or unsupported project-side usage.

If the module cannot be used through a supported public contract without patching its installed files, stop and report:

1. The failing dependency and version.
1. The project code that triggers the failure.
1. The supported dependency contract that differs from the current usage.
1. The project-side change required to use the module correctly.
1. Whether a dependency version change or replacement is required.

The source of truth must remain the dependency's published package plus the project's explicit use of its supported API. Installed dependency contents must remain reproducible directly from the package manager without repository-owned post-install modifications.
