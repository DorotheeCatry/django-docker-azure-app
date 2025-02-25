/**
 * Configuration minimale pour Tailwind CSS dans un projet Django.
 * Si vous avez besoin de la configuration complète, consultez :
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
        /**
         * HTML : Chemins vers les fichiers de templates Django contenant des classes Tailwind CSS.
         */

        /* Templates dans l'application thème (<nom_de_app>/templates), ex. base.html. */
        '../templates/**/*.html',

        /*
         * Répertoire principal des templates du projet (BASE_DIR/templates).
         * Ajustez cette ligne en fonction de la structure de votre projet.
         */
        '../../templates/**/*.html',

        /*
         * Templates dans d'autres applications Django (BASE_DIR/<nom_de_app>/templates).
         * Ajustez cette ligne en fonction de la structure de votre projet.
         */
        '../../**/templates/**/*.html',

        /**
         * JS : Si vous utilisez Tailwind CSS dans des fichiers JavaScript, décommentez les lignes suivantes
         * et assurez-vous que les modèles correspondent à la structure de votre projet.
         */
        /* JS 1 : Ignorer les fichiers JavaScript dans le dossier node_modules. */
        // '!../../**/node_modules',
        /* JS 2 : Traiter tous les fichiers JavaScript du projet. */
        // '../../**/*.js',

        /**
         * Python : Si vous utilisez des classes Tailwind CSS dans des fichiers Python,
         * décommentez la ligne suivante et ajustez le modèle ci-dessous à votre structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            // Ajoutez ici vos personnalisations de thème (couleurs, typographie, etc.)
            colors: {
                accent: {
                    100: '#E5E7EB', // Couleur claire pour les bordures
                    500: '#6B7280', // Couleur pour le texte secondaire
                    600: '#4B5563', // Couleur pour les icônes et hover
                    700: '#374151', // Couleur principale pour le texte
                },
            },
            boxShadow: {
                elegant: '0 4px 6px rgba(0, 0, 0, 0.1)', // Ombre élégante
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' : Plugin pour un style minimal des formulaires.
         * Si vous préférez un style personnalisé, commentez cette ligne.
         */
        require('@tailwindcss/forms'),

        /**
         * '@tailwindcss/typography' : Plugin pour des styles typographiques avancés.
         */
        require('@tailwindcss/typography'),

        /**
         * '@tailwindcss/aspect-ratio' : Plugin pour gérer les ratios d'aspect des éléments.
         */
        require('@tailwindcss/aspect-ratio'),
    ],
};