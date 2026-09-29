# Publication resources

Checked 7 September 2026. Titles link to publisher records where available. PDFs are hosted in `files/` and are never substituted with HTML redirects. The PDFs retain their original copyright and license notices.

## Local PDFs

| Paper | Local PDF | Source | SHA-256 |
|---|---|---|---|
| consistent-diffusion | [icml26-consistent-diffusion.pdf](../files/icml26-consistent-diffusion.pdf) | [download source](https://arxiv.org/pdf/2605.00161) | `f4db928e1cc2da5b10854b83d3843b8657f9e9de34bd4ac1ae5b8133f53ddc5b` |
| fallback-to-frontline | [acl26-fallback-to-frontline.pdf](../files/acl26-fallback-to-frontline.pdf) | [download source](https://aclanthology.org/2026.findings-acl.2124.pdf) | `b097b941533fb1017c13920ad9ff89c0306f523a41ad4009a4b39f26c28aba55` |
| escaping-mode-lottery | [arxiv26-escaping-mode-lottery.pdf](../files/arxiv26-escaping-mode-lottery.pdf) | [arXiv v1, CC BY 4.0](https://arxiv.org/pdf/2606.00544v1) | `d3dff98212cbe2bde3e7514cabfa39f99874aaa84e81e25de59760de9d6a7d24` |
| critical-thinking | [chi26-critical-thinking.pdf](../files/chi26-critical-thinking.pdf) | [download source](https://arxiv.org/pdf/2602.10222) | `298f22d20e246ad4eba8dd3588e0671c54ceb60cbdca4912582cf347a5206bac` |
| adaptive-ensembles | [aaai26-adaptive-ensembles.pdf](../files/aaai26-adaptive-ensembles.pdf) | [download source](https://arxiv.org/pdf/2602.20104) | `e2b7cc11e29b881c5a13fe0382a735cabed74b9c57f9d9a499b05eb1dfdf7e1c` |
| support-vector-effect | [kdd25-support-vector-effect.pdf](../files/kdd25-support-vector-effect.pdf) | Existing personal original; preserved unchanged | `ad83820861caa81e8fc83a2e62ca6433dff19771566b87d82713ce05e6a80b82` |
| mix-and-match | [hcomp24-mix-and-match.pdf](../files/hcomp24-mix-and-match.pdf) | [download source](https://mingyin.org/paper/HCOMP-24/mm.pdf) | `72c83b2c9e5b6c521db4a4d23ea82983751f6b65999b66c808b790483e5da23f` |
| behavior-aware-ai | [ijcai24-behavior-aware-ai.pdf](../files/ijcai24-behavior-aware-ai.pdf) | Existing personal original; preserved unchanged | `520ac6cae621badd8683102a7232a8701831ae5a9c5969047d0937adb100f425` |
| human-reactions | [icml23-workshop-human-reactions.pdf](../files/icml23-workshop-human-reactions.pdf) | Existing personal original; preserved unchanged | `4f5e627909dbaf16f1e03a2de0213adf17ed130efdd2fd8fe194f381adbef629` |
| phishcasting | [isi20-phishcasting.pdf](../files/isi20-phishcasting.pdf) | [download source](https://ahmedabbasi.com/wp-content/uploads/C/Mahmood_Phishcasting_IEEEISI2020.pdf) | `2f2452ed56f2f2f4747a830a48109e887250dbaa779f7fe35181cd90d25c2fdd` |
| phishing-prediction | [icdmw20-phishing-prediction.pdf](../files/icdmw20-phishing-prediction.pdf) | [download source](https://ahmedabbasi.com/wp-content/uploads/C/Mahmood_DeepGenerativeModels_ICDMW2020.pdf) | `6f21b121922fc610d4ce6af1d2bb1fedfacf459f95e12451b40734fcdcd5591f` |

The newly downloaded PDFs were opened with PDFKit and checked against their paper titles. The three pre-existing paper PDFs are used directly, without rewriting them.

## Verified public code

Each linked repository’s README explicitly names the corresponding paper:

- **escaping-mode-lottery**: [multi-response-training](https://github.com/shasanamin/multi-response-training), also linked from the paper.
- **fallback-to-frontline**: [llm-perspective-taking](https://github.com/shasanamin/llm-perspective-taking).
- **adaptive-ensembles**: [aaai26-adaptive-ai](https://github.com/shasanamin/aaai26-adaptive-ai).
- **support-vector-effect**: [sve](https://github.com/shasanamin/sve).
- **behavior-aware-ai**: [ijcai24-behavior-aware-ai](https://github.com/shasanamin/ijcai24-behavior-aware-ai).

SVE and LLM perspective-taking also link to these repositories from their PDFs. The public `shasanamin` repository list did not provide an identifiable code release for the other papers; related workshop versions are not assumed to have an identical implementation.

## Paper-record exceptions

- **Escaping the Mode Lottery:** listed as a preprint, with the title pointing to [arXiv:2606.00544](https://arxiv.org/abs/2606.00544). The record lists 30 May 2026 as the submission date; the citation therefore uses May 2026. No conference acceptance is implied.

- **Consistent Diffusion Language Models:** the [official ICML paper page](https://icml.cc/virtual/2026/poster/66178) matches the title, authors, and abstract. No ICML 2026 volume was listed in the [PMLR index](https://proceedings.mlr.press/) when checked. Replace `url` with its exact PMLR record once available.
- **2023 workshop papers:** titles use their exact [NeurIPS](https://neurips.cc/virtual/2023/83395) and [ICML](https://icml.cc/virtual/2023/27379) paper pages. These remain distinct from the later full papers.
- **2023 SVE workshop PDF:** the official page links to [OpenReview](https://openreview.net/forum?id=qiXTllMbUa), but its public PDF endpoint returned HTTP 403 and no separate author copy was located. `pdf_url` is intentionally omitted. Add the workshop manuscript to `files/` when available; do not silently substitute the later KDD paper.

## CV preprint update, 10 September 2026

| Paper | Local PDF | Source | SHA-256 |
|---|---|---|---|
| scale-invariant-instability | [arxiv26-scale-invariant-instability.pdf](../files/arxiv26-scale-invariant-instability.pdf) | [arXiv v1](https://arxiv.org/pdf/2609.09116v1) | `632290b1e26a80663e11790d4aaf1832c67205b10e9b70824e9f7ba6f3ad0365` |

The 35-page PDF was opened with PDFKit and its title, authors, arXiv identifier, and date verified. The CV links the public [normalized-optimization-dynamics repository](https://github.com/shasanamin/normalized-optimization-dynamics), also linked from the arXiv abstract.

The website publication record now uses the same verified title, author order, September 2026 date, local PDF, and public code link. It is listed as a preprint and selected for the homepage. Its illustration draws on Appendix G's distinction between weight-norm shrinkage and effective directional-step expansion, alongside the schedule control interpretation of the exact law. It is schematic geometry, not an experimental plot.

## CV preprint update, 29 September 2026

| Paper | Local PDF | Source | SHA-256 |
|---|---|---|---|
| simple-diffusion | [arxiv26-simple-diffusion.pdf](../files/arxiv26-simple-diffusion.pdf) | [arXiv v1](https://arxiv.org/pdf/2609.33947v1) | `adc54ca51ad814eb13a84bc28edbf37ae51a20be8ddc98ce3db92ae1bc91e5a6` |

The 38-page PDF was opened with PDFKit and its title, authors, arXiv identifier, and submission date verified. The CV lists it as P3 with its published title, “Simple Diffusion Language Models Are More Effective Few-Step Generators Than Reported,” and a September 2026 date.

The website publication record now uses the same citation and local PDF, with a copyable arXiv BibTeX entry. The paper links the public [more-effective-dlms repository](https://github.com/shasanamin/more-effective-dlms); its README matches the title and documents sampling experiments, the reusable GroupEval protocol/scorer, aggregate results, and finite-step theory verifiers. This is the website's Code destination. The release provides aggregates rather than raw generations, individual judgments, or model weights. News records are unchanged.
