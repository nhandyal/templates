# Typescript

## Getting started

**Preferred method: Use GTS**

[Google TypeScript Style](https://github.com/google/gts), known as GTS, is a style guide, linter, and automatic code corrector all in one. Using GTS will help you to quickly bootstrap a new TypeScript project and avoid focusing on small, organizational details to focus on designing your project.

```
npm i gts --save-dev
npx gts init
```

This generates everything needed to get started with TypeScript. Includes a tsconfig.json, linting setup, & package.json (if not present). Helpful npm scripts are added, example: npm run compile, or npm run check

**[Manual method](https://www.digitalocean.com/community/tutorials/typescript-new-project)**

```
npm i typescript --save
npx tsc --init
```

Init creates a typescript config in this folder.

**compiling code**

```
npx tsc
npx tsc -w # compiler watch mode
```

# VS-Code integration

Some pitfalls to watchout for to ensure everything is working as expected.

1. [Ensure TS extension is enabled](https://stackoverflow.com/a/56173789) in VS-Code. search `@builtin typescript` in the extensions view.
2. If there are multiple versions of typescript installed, specify the `typescript.tsdk` in settings.json. See [here](https://code.visualstudio.com/docs/typescript/typescript-compiling#_using-the-workspace-version-of-typescript).

# React + TypeScript

- [React + Typescript official docs](https://react.dev/learn/typescript)
