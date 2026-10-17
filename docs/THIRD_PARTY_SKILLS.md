# Third-party skill notices

The following skills are copied into `.agents/skills/` for repository-local agent guidance. Upstream references are pinned by repository commit and per-skill content hash so a later refresh can be reviewed as a separate change. Skills are guidance files; their presence does not install or grant access to the tools, credentials, or services they discuss.

| Skill | Upstream source snapshot | License / declared version | `skills-lock.json` content hash |
|---|---|---|---|
| `vercel-react-best-practices` | `vercel-labs/agent-skills` @ `063bee94c3f4df8453406c830b0a7df0f2860278` | MIT / 1.0.0 | `3219a1944e404ffc14d1d9d6aef6dd2e3855b81387ee0a044ccbfe14d34c2357` |
| `vercel-composition-patterns` | `vercel-labs/agent-skills` @ `063bee94c3f4df8453406c830b0a7df0f2860278` | MIT / 1.0.0 | `f98931159fa9c7fed043bcd18a891a46dcf89ababa38df13a4c5b7b30dc0ce07` |
| `fba` | `fastapi-practices/skills` @ `8d6155c2be880b3e3e2d359b67904e378eaf5f13` | MIT / no skill version declared | `6040ad4cc1db89d01682193e5edb5178d96642a27a0a4db5046f23221d315ae6` |
| `supabase` | `supabase/agent-skills` @ `c9be0e931b7930f7d02126d04774d904c381e7d7` | MIT / 0.1.2 | `211141fd078b4b3645803868528d54221bc7755d24d5c8af45a366785c151dba` |
| `supabase-postgres-best-practices` | `supabase/agent-skills` @ `c9be0e931b7930f7d02126d04774d904c381e7d7` | MIT / 1.1.1 | `e14e276241805c97dbcfe40dcbea1a3035269cc7293cac4b1832dda41a835e60` |
| `prompt-engineering-patterns` | `wshobson/agents` @ `044b4b21f083948e69ec878a7b07c8d0951a6ffa` | MIT / no skill version declared | `6a8cf3a5e9120641c1c1953c870c156377c57be4a806e1df6fc5f073a41cc639` |
| `design-system-patterns` | `wshobson/agents` @ `044b4b21f083948e69ec878a7b07c8d0951a6ffa` | MIT / no skill version declared | `e1d2631eab1a7113fb60e6df3ace05aac0ddce6207bceec87721119a8e1a1c78` |
| `rag-implementation` | `wshobson/agents` @ `044b4b21f083948e69ec878a7b07c8d0951a6ffa` | MIT / no skill version declared | `595e221310222b991452ac6d850097b466fbda46860c9ce933ddd56a0998dac9` |
| `webapp-testing` | `anthropics/skills` @ `dbd4588f9e1033efb41dad4bef2f7947c8993d44` | Apache-2.0 / bundled `LICENSE.txt` | `ad5b1fc52807e9afa4635e59218a026b164dc58b6c3f41b0f7c644dcd6ccf572` |
| `mcp-builder` | `anthropics/skills` @ `dbd4588f9e1033efb41dad4bef2f7947c8993d44` | Apache-2.0 / bundled `LICENSE.txt` | `826e46adf81e1372282e205c34e1a2ee876e72148007726e4a2512599d2fef7b` |
| `docker-project-foundations` | `docker/skills` @ `25f7e03184ce455ea1604bea00f7b40f95ca50e5` | Apache-2.0 | `6b2334b2c24910d177e1f80a0cc1f5135f2a9b33b722673873435736de36128f` |
| `docker-build-strategies` | `docker/skills` @ `25f7e03184ce455ea1604bea00f7b40f95ca50e5` | Apache-2.0 | `e6a297d613873cf74b030655ee8405ca4434980cfb0dfd412ac5aa4e213d3d5c` |
| `performance` | `addyosmani/web-quality-skills` @ `afa8da942115f2961fdbfa80807ea0b232ff6c00` | MIT / 2.0 | `ce9d36f139a1b2a6a8ac2cb222698963b8076d2dd8b41685e8e8ae589cdcf1e4` |

MIT terms and upstream copyright notices are reproduced in [LICENSE-MIT.txt](third_party_licenses/LICENSE-MIT.txt). Docker's Apache-2.0 license is reproduced in [LICENSE-APACHE-2.0-Docker.txt](third_party_licenses/LICENSE-APACHE-2.0-Docker.txt); Anthropic's skill folders retain their bundled Apache-2.0 `LICENSE.txt` files.

`web-design-guidelines` was previewed but not copied: neither the skill nor its upstream repository declared a license at review time. The review-only Codex prompting skill was not installed because it is not in `approved_install`.
