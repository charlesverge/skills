
//import mdast from "mdast-util-to-markdown";
/** @type {import('remark-cli').Options} */
const config = {
  settings: {
    bullet: '*',
    incrementListMarker: false,
  },
  plugins: [
    "remark-frontmatter",
    "remark-lint",
    [
      "remark-lint-no-file-name-irregular-characters",
      "\\.a-zA-Z0-9_-"
    ],
    [
      "remark-lint-file-extension",
      "md"
    ],
    "remark-lint-no-file-name-consecutive-dashes",
    "remark-lint-no-file-name-outer-dashes",
    [
      "remark-lint-list-item-spacing",
      false
    ],
    "remark-lint-no-consecutive-blank-lines",
    [
      "remark-lint-maximum-line-length",
      500
    ],
    "remark-lint-no-shell-dollars",
    "remark-lint-hard-break-spaces",
    [
      "remark-lint-heading-style",
      "atx"
    ],
    "remark-lint-heading-increment",
    [
      "remark-lint-no-duplicate-headings",
      false
    ],
    [
      "remark-lint-no-multiple-toplevel-headings",
      false
    ],
    [
      "remark-lint-maximum-heading-length",
      120
    ],
    [
      "remark-lint-no-heading-punctuation",
      false
    ],
    [
      "remark-lint-blockquote-indentation",
      2
    ],
    "remark-lint-no-blockquote-without-marker",
    [
      "remark-lint-ordered-list-marker-value",
      "one"
    ],
    [
      "remark-lint-unordered-list-marker-style",
      false
    ],
    [
      "remark-lint-ordered-list-marker-style",
      false
    ],
    [
      "remark-lint-list-item-indent",
      false
    ],
    "remark-lint-list-item-content-indent",
    [
      "remark-lint-code-block-style",
      "fenced"
    ],
    [
      "remark-lint-fenced-code-flag",
      {
        "allowEmpty": true
      }
    ],
    [
      "remark-lint-fenced-code-marker",
      "`"
    ],
    [
      "remark-lint-rule-style",
      "---"
    ],
    "remark-lint-no-table-indentation",
    "remark-lint-table-pipes",
    "remark-lint-table-pipe-alignment",
    [
      "remark-lint-table-cell-padding",
      "padded"
    ],
    "remark-lint-no-shortcut-reference-image",
    "remark-lint-no-shortcut-reference-link",
    "remark-lint-final-definition",
    "remark-lint-definition-case",
    "remark-lint-definition-spacing",
    [
      "remark-lint-link-title-style",
      "\""
    ],
    [
      "remark-lint-strong-marker",
      "*"
    ],
    [
      "remark-lint-emphasis-marker",
      "*"
    ],
    [
      "remark-lint-no-emphasis-as-heading",
      false
    ],
    "remark-gfm",
/*    [mdast, {"extensions": {
      "unsafe": {
        
      }
    }}]*/
  ],
};

export default config;

