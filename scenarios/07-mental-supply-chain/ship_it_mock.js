const fs = require('fs');
const content = fs.readFileSync(0, 'utf-8');
fs.writeFileSync('shipped_issue.md', content);
console.log(`[Ship-It Mock] Successfully created ticket 'shipped_issue.md' with ${content.length} characters.`);
