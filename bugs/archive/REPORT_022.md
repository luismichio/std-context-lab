# Bug Report 022: Hardcoded Version String in Rust Core

**Date:** 2026-05-24
**Scenario:** Update & Version Verification
**Status:** Closed (Verified)

---

## 1. Version Discrepancy (MAJOR)

### Description
The `cpipe` Rust binary reported version `0.4.0` even after the source code and `Cargo.toml` were updated to `v0.4.3`. This caused confusion during verification and made it appear as if the update had failed.

### Evidence
- `Cargo.toml` version: `0.4.3`
- `cpipe --version` output: `cpipe 0.4.0`
- GitHub Release Tag: `v0.4.3`

### Root Cause
In `target_repos/context-pipe/crates/cpipe/src/main.rs`, the version was hardcoded using the clap attribute:
```rust
#[command(version = "0.4.0")]
```
This attribute does not automatically synchronize with the package version in `Cargo.toml`.

### Resolution
The version string was patched to use the `CARGO_PKG_VERSION` environment variable provided by Cargo at build time:
```rust
#[command(version = env!("CARGO_PKG_VERSION"))]
```
The binary was then rebuilt and verified to report `0.4.3`.

---

## 2. Impact on Lab
Version verification is unreliable when strings are hardcoded. This leads to redundant update attempts and difficulty in confirming that security patches or features are correctly deployed.

### Recommended Fix
Standardize on `env!("CARGO_PKG_VERSION")` for all Rust-based CLI tools in the project to ensure a single source of truth (the `Cargo.toml` file).
