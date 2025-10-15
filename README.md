# Activity HAProxy Docs

- Documentation Astro : <https://docs.astro.build/en/getting-started/>
- Documentation Starlight : <https://starlight.astro.build/>

## Developpement local

1. Installer les dependances : `npm install`.
2. Lancer un serveur de dev : `npm run dev`.
3. Construire le site : `npm run build`.
4. Previsualiser la version de production : `npm run preview`.

## Deploiement sur GitHub Pages

Le workflow `.github/workflows/deploy-gh-pages.yml` publie automatiquement le dossier `dist/` sur GitHub Pages.  
Lorsque le site est heberge sur une URL de type `https://<utilisateur>.github.io/<repo>/`, Astro doit connaitre l'URL publique complete ainsi que le sous-chemin.  
Sans ces informations, les assets (CSS, JS, favicon, etc.) sont servis comme s'ils etaient a la racine du domaine, ce qui entraine les erreurs 404 observees dans la console (`_astro/...`, `index....css`, `favicon.svg`, ...).

### Configurer `astro.config.mjs`

Dans ce projet, il faut definir explicitement les proprietes `site` et `base` :

```js
export default defineConfig({
  site: 'https://manastria.github.io/activity-haproxy/',
  base: '/activity-haproxy/',
  // ...
});
```

- `site` pointe vers l'URL publique finale (avec la barre oblique finale).
- `base` correspond au nom du depot (precede d'une barre, avec une barre finale).

Apres avoir ajuste `astro.config.mjs`, committez la modification puis relancez le workflow GitHub Actions.  
Lors du prochain deploiement, les fichiers CSS et JS seront references avec le bon chemin et ne retourneront plus de 404.

### Verifier avant de pousser

1. `npm run build`
2. `npm run preview -- --host`
3. Ouvrir `http://localhost:4321/activity-haproxy/` et confirmer que la console ne signale plus d'erreurs 404.

Le site est publie sur : <https://manastria.github.io/activity-haproxy/>
