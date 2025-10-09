import express from 'express';
import swaggerUi from 'swagger-ui-express';
import YAML from 'yamljs';
import fs from 'fs';
import path from 'path';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT;

// === 1. Directory containing YAML files ===
const docsDir = path.resolve('./docs');

// === 2. Load all .yaml files ===
const files = fs.readdirSync(docsDir).filter(f => f.endsWith('.yaml'));

files.forEach(file => {
    const name = file.replace(/\.yaml$/, '');
    const filePath = path.join(docsDir, file);
    const swaggerDocument = YAML.load(filePath);

    app.use(`/docs/${name}`, swaggerUi.serve, swaggerUi.setup(swaggerDocument));
    console.log(`📘 Loaded Swagger doc: ${file} → http://localhost:${PORT}/docs/${name}`);
});

app.get('/', (_, res) => {
    res.send(`
    <h2>Available Swagger Docs:</h2>
    <ul>
      ${files.map(f => `<li><a href="/docs/${f.replace('.yaml', '')}">${f}</a></li>`).join('')}
    </ul>
  `);
});

app.get('/health', (_, res) => {
    res.status(200).send('OK');
});

app.listen(PORT);
