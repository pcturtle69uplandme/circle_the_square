require("dotenv").config({ path: require("path").join(__dirname, "..", "..", ".env"), quiet: true });
const { fal } = require("@fal-ai/client");

if (!process.env.FAL_KEY) {
  console.error("FAL_KEY not set. Run fal-tools/set-fal-key.ps1 first (copy your key to the clipboard, then run it).");
  process.exit(1);
}

fal.config({ credentials: process.env.FAL_KEY });

module.exports = { fal };
