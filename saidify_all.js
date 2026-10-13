const fs = require("fs");
const path = require("path");
const { saidifyUrn } = require("saidify");

const inputDir = "data/processed";
const outputDir = "data/curated";

fs.mkdirSync(outputDir, { recursive: true });

const files = fs.readdirSync(inputDir)
    .filter(f => f.endsWith(".json"));

for (const file of files) {
    const inputPath = path.join(inputDir, file);

    const data = JSON.parse(
        fs.readFileSync(inputPath, "utf8")
    );

    const [urn, sad] = saidifyUrn(data, "identifier");

    const outputPath = path.join(outputDir, file);

    fs.writeFileSync(
        outputPath,
        JSON.stringify(sad, null, 2)
    );

    console.log(`✓ ${file}`);
    console.log(`  ${urn}`);
}