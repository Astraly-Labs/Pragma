/*
AUTOGENERATED - DON'T EDIT
Your edits in this file will be overwritten in the next build!
Modify the docusaurus.config.js file at your site's root instead.
*/
export default {
  "title": "Pragma",
  "tagline": "Documentation and Guides",
  "url": "https://docs.pragmaoracle.com",
  "baseUrl": "/",
  "onBrokenLinks": "warn",
  "onBrokenMarkdownLinks": "ignore",
  "favicon": "img/favicon.png",
  "organizationName": "Astraly-Labs",
  "projectName": "Pragma",
  "trailingSlash": false,
  "themeConfig": {
    "image": "img/background.jpg",
    "metadata": [
      {
        "name": "twitter:card",
        "content": "summary"
      }
    ],
    "prism": {
      "additionalLanguages": [
        "solidity"
      ]
    },
    "algolia": {
      "apiKey": "10bd5a4750327624845152ae40c0c9c0",
      "indexName": "v3-docs",
      "appId": "I2FJIAZ9PU",
      "contextualSearch": true,
      "searchParameters": {},
      "searchPagePath": "search"
    },
    "navbar": {
      "title": "Pragma Docs",
      "logo": {
        "alt": "Pragma Logo",
        "src": "img/prg_dark_icon.png"
      },
      "items": [
        {
          "to": "/docs/introduction",
          "label": "Protocol",
          "position": "right",
          "className": "persistent"
        },
        {
          "label": "Feedbacks",
          "to": "https://kprem87muy4.typeform.com/to/ahJVbIeI",
          "position": "right",
          "className": "persistent"
        },
        {
          "href": "https://github.com/Astraly-Labs",
          "label": "GitHub",
          "position": "right",
          "className": "persistent"
        }
      ],
      "hideOnScroll": false
    },
    "colorMode": {
      "defaultMode": "dark",
      "disableSwitch": false,
      "respectPrefersColorScheme": false
    },
    "docs": {
      "versionPersistence": "localStorage"
    },
    "hideableSidebar": false,
    "autoCollapseSidebarCategories": false,
    "tableOfContents": {
      "minHeadingLevel": 2,
      "maxHeadingLevel": 3
    }
  },
  "presets": [
    [
      "@docusaurus/preset-classic",
      {
        "docs": {
          "path": "docs",
          "remarkPlugins": [
            null
          ],
          "rehypePlugins": [
            null
          ],
          "routeBasePath": "/docs",
          "sidebarPath": "/Users/matthall/Documents/Empiric/docs/sidebars.js",
          "includeCurrentVersion": false,
          "versions": {
            "V3": {
              "banner": "none"
            }
          }
        },
        "blog": {
          "remarkPlugins": [
            null
          ],
          "rehypePlugins": [
            null
          ],
          "path": "blog/",
          "blogTitle": "Engineering Blog",
          "blogSidebarCount": 0
        },
        "googleAnalytics": {
          "trackingID": "UA-128182339-7",
          "anonymizeIP": true
        },
        "theme": {
          "customCss": "/Users/matthall/Documents/Empiric/docs/src/css/custom.css",
          "customCss2": "/Users/matthall/Documents/Empiric/docs/src/css/colors.css"
        }
      }
    ]
  ],
  "stylesheets": [
    {
      "href": "https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css",
      "type": "text/css",
      "integrity": "sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM",
      "crossorigin": "anonymous"
    }
  ],
  "baseUrlIssueBanner": true,
  "i18n": {
    "defaultLocale": "en",
    "locales": [
      "en"
    ],
    "localeConfigs": {}
  },
  "onDuplicateRoutes": "warn",
  "staticDirectories": [
    "static"
  ],
  "customFields": {},
  "plugins": [],
  "themes": [],
  "titleDelimiter": "|",
  "noIndex": false
};