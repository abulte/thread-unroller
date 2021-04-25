const { description } = require('../../package')
const glob = require('glob')

const threadsList = glob
  .sync('blog/threads/*.md')
  .map(f => f.split('/')[2])
  .filter(f => f !== 'index.md')

module.exports = {
  /**
   * Compatibility with github pages
   */
  base: '/twitter-threads-blog/',

  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#title
   */
  title: 'My blog, with twitter threads',
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#description
   */
  description: description,

  /**
   * Extra tags to be injected to the page HTML `<head>`
   *
   * ref：https://v1.vuepress.vuejs.org/config/#head
   */
  head: [
    ['meta', { name: 'theme-color', content: '#3eaf7c' }],
    ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }]
  ],

  /**
   * Theme configuration, here is the default theme configuration for VuePress.
   *
   * ref：https://v1.vuepress.vuejs.org/theme/default-theme-config.html
   */
  themeConfig: {
    repo: '',
    editLinks: false,
    docsDir: '',
    editLinkText: '',
    lastUpdated: false,
    nav: [
      {
        text: 'Threads',
        link: '/threads/',
      },
    ],
    sidebar: {
      '/threads/': [
        {
          title: 'Threads',
          collapsable: false,
          children: threadsList,
          // children: [
          //   '1385195772199714816.md',
          //   '1381281294865272833.md',
          // ]
        }
      ],
    }
  },

  /**
   * Apply plugins，ref：https://v1.vuepress.vuejs.org/zh/plugin/
   */
  plugins: [
    '@vuepress/plugin-back-to-top',
    '@vuepress/plugin-medium-zoom',
  ]
}
