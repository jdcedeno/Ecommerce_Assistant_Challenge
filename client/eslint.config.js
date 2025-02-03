import js from "@eslint/js"
import globals from "globals"
import reactHooks from "eslint-plugin-react-hooks"
import reactRefresh from "eslint-plugin-react-refresh"
import tseslint from "typescript-eslint"
import prettierPlugin from "eslint-plugin-prettier"
import prettierConfig from "eslint-config-prettier"

// ---
// 1. Base configurations: recommended configs from @eslint/js and typescript-eslint.
//    These may be objects or arrays, so we ensure we spread them into our exported array.
const baseConfigs = [
  js.configs.recommended,
  ...tseslint.configs.recommended, // Spread in case it"s an array.
]

// ---
// 2. Custom TypeScript/TSX configuration.
//    Note that we are not using "extends" here; we only set our custom options.
const tsConfig = tseslint.config(
  { ignores: ["dist"] },
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
    },
    plugins: {
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      "react-refresh/only-export-components": [
        "warn",
        { allowConstantExport: true },
      ],
    },
  }
)

// Ensure tsConfig is an array (flatten it if necessary)
const tsConfigArray = Array.isArray(tsConfig) ? tsConfig : [tsConfig]

// ---
// 3. Prettier integration.
//    This object tells ESLint to run Prettier as an ESLint rule and use the given options.
const prettierRuleConfig = {
  plugins: {
    prettier: prettierPlugin,
  },
  rules: {
    "prettier/prettier": [
      "error",
      {
        // Prettier options: use double quotes (singleQuote: false) plus other settings.
        singleQuote: false,
        trailingComma: "es5",
        semi: false,
        printWidth: 80,
        tabWidth: 2,
        jsxSingleQuote: false,
      },
    ],
  },
}

// ---
// 4. Prettier configuration from eslint-config-prettier disables conflicting ESLint rules.
//    It might be an object or an array, so we flatten it.
const prettierConfigArray = Array.isArray(prettierConfig)
  ? prettierConfig
  : [prettierConfig]

// ---
// 5. Export a flat array of configuration objects.
export default [
  ...baseConfigs,
  ...tsConfigArray,
  prettierRuleConfig,
  ...prettierConfigArray,
]
