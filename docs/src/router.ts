import express from 'express';
import path from "path";
import fs from "fs";
import YAML from "yamljs";
import swaggerUi from "swagger-ui-express";
const router = express.Router();

// === 1. Directory containing YAML files ===
const docsDir = path.resolve('./docs');

// === 2. Load all .yaml files ===
const files = fs.readdirSync(docsDir).filter(f => f.endsWith('.yaml'));

files.forEach(file => {
    const name = file.replace(/\.yaml$/, '');
    const filePath = path.join(docsDir, file);
    const swaggerDocument = YAML.load(filePath);

    router.use(`/${name}`, swaggerUi.serve, swaggerUi.setup(swaggerDocument));
});

router.get('/', (_, res) => {
    res.send(`
    <h2>Available Swagger Docs:</h2>
    <ul>
      ${files
        .map(f => {
            const name = f.replace('.yaml', '');
            return `<li><a href="/docs/${name}/">${name}</a></li>`;
        })
        .join('')}
    </ul>
  `);
});


router.get('/health', (_, res) => {
    res.status(200).send('OK');
});

export default router;
