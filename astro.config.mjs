import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// 1) If deploying to GitHub Pages under a project repo, set `site` + `base`.
//    Example:
//    site: 'https://<user>.github.io/<repo>/',
//    base: '/<repo>/',
// 2) For a root domain or Infomaniak hosting, you can omit `base` and set `site` to your full URL.
export default defineConfig({
  site: 'https://manastria.github.io/activity-haproxy/',
  base: '/activity-haproxy/', // only for GitHub project pages
  integrations: [
    starlight({
      title: 'Activites SISR',
      locales: { root: { label: 'Francais', lang: 'fr' } },
      sidebar: [
        { label: 'Accueil', link: '/' },
        {
          label: 'Activites',
          // Auto-generate the group from files under src/content/docs/activities
          autogenerate: { directory: 'activities', collapsed: false },
        },
      ],
      editLink: {
        baseUrl:
          'https://github.com/manastria/activity-haproxy/edit/master/',
      },
      tableOfContents: {
        heading: 'Sommaire',
        // Include all headings from the content files
        // include: ['h1', 'h2', 'h3'],
        minHeadingLevel: 2,
        maxHeadingLevel: 4,
      },
      customCss: ['./src/styles/details-callout.css'],
      // Add your analytics/scripts if needed using the `head` option.
    }),
  ],
});
