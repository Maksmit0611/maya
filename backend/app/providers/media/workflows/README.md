# ComfyUI workflow boundary

Phase 1 ships no executable ComfyUI graph. Add reviewed, versioned workflow JSON here when a production worker is configured. Workflows must expose a small named-input contract and must never be assembled by interpolating arbitrary user-provided graph JSON. Record the immutable workflow hash, model/version, seed, and provider response in job provenance. The current adapter returns a structured unavailable state until that review and implementation are complete.
