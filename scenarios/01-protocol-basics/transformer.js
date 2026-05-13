#!/usr/bin/env node
/**
 * lab-mock-transformer
 * A simple Node.js script adhering to the Context-Pipe Protocol (CPP).
 * It reads stdin, appends a tag to every line, and writes to stdout.
 */

const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  terminal: false
});

rl.on('line', (line) => {
  if (line.trim()) {
    console.log(`[LAB-TEST-TRANSFORMED] ${line}`);
  }
});
