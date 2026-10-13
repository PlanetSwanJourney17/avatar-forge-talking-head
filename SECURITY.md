# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | yes       |
| 0.3.x   | security fixes only |
| < 0.3   | no        |

## Reporting a vulnerability

Do **not** open a public issue for security problems. Email
`security@avatar-forge.dev` with:

- A description of the issue and its impact.
- Reproduction steps or a proof-of-concept.
- The affected version(s) and platform.

We aim to acknowledge within 72 hours and ship a patch within 14 days for
confirmed high-severity issues.

## Scope

In scope:
- Arbitrary code execution via crafted model weights, `.afproj` project files,
  or audio/face inputs.
- Path traversal in the render output writer.
- Privilege issues in the Windows CUDA/audio adapters.

Out of scope:
- Results of running untrusted third-party plugins (see below).
- Denial of service from intentionally oversized inputs on your own machine.

## Third-party plugins

`avatar-forge-talking-head` loads plugins from `%APPDATA%/avatar-forge/plugins`.
Plugins run with full user privileges. Only install plugins you trust. We do
not sandbox plugin code.

## Model weights

Only load `.onnx` / `.safetensors` weights from sources you trust. The loader
does not execute pickle payloads, but ONNX graphs can still be adversarial.