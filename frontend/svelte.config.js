// TODO: understand why this has to be cjs style
// https://github.com/sveltejs/language-tools/issues/699
// https://github.com/sveltejs/language-tools/blob/master/docs/preprocessors/scss-less.md
const sveltePreprocess = require('svelte-preprocess');

module.exports = {
    preprocess: sveltePreprocess()
}
