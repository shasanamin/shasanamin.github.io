# Publication citations

Checked 10 September 2026. The site keeps BibTeX beside each paper in `_data/publications.yml`; `bibtex_source` records its provenance. Both publication lists render the same record. Citation text is escaped into a read-only field, with a native disclosure and optional clipboard enhancement.

Google Scholar could not be retrieved through the available access. These entries therefore use official exports or verified primary metadata, rather than claiming to reproduce Scholar exports.

| Papers | Source and treatment |
| --- | --- |
| ACL Findings | [ACL Anthology BibTeX](https://aclanthology.org/2026.findings-acl.2124.bib), including the published DOI, pages, editors, and book title. |
| IJCAI 2024 | [Publisher BibTeX](https://www.ijcai.org/proceedings/2024/bibtex/344), including the DOI, pages, and editor. |
| CHI 2026 | [ACM-deposited Crossref metadata](https://api.crossref.org/works/10.1145/3772318.3790785). Name order follows the paper and the existing author record; Harry Yizhou Tian is encoded as `Tian, Harry Yizhou`, consistent with his ACL author entry. |
| AAAI 2026 | [Publisher-deposited metadata](https://api.crossref.org/works/10.1609/aaai.v40i21.38786). Export as an article in the proceedings journal, volume 40, number 21, pages 17337–17346. |
| HCOMP 2024 | [Publisher record](https://ojs.aaai.org/index.php/HCOMP/article/view/31604) and its Crossref deposit. Correct the truncated `Syed Hasan Amin Mahmoo` to `Syed Hasan Amin Mahmood`, verified on the first page of the local paper PDF. Volume 12, number 1, pages 95–104. |
| KDD 2025 | [ACM-deposited Crossref record](https://api.crossref.org/works/10.1145/3690624.3709295), including the V.1 proceedings title and pages 1020–1031. |
| ISI 2020 | [IEEE-deposited Crossref record](https://api.crossref.org/works/10.1109/ISI49825.2020.9280509), pages 1–6. Full names follow the paper; family names Mahmood and Abbasi are encoded consistently with the other citations. |
| ICDMW 2020 | [IEEE-deposited Crossref record](https://api.crossref.org/works/10.1109/ICDMW51313.2020.00073), verified by exact title, pages 496–505. |
| ICML 2026 | [Official conference record](https://icml.cc/virtual/2026/poster/66178). Conference citation with verified authors, title, year, and URL; no unverified PMLR volume or page range. |
| NeurIPS 2023 workshop | [Official workshop poster record](https://neurips.cc/virtual/2023/83395). Workshop named explicitly; no fabricated main-conference proceedings or page range. |
| ICML 2023 workshop | [Official workshop poster record](https://icml.cc/virtual/2023/27379). Workshop named explicitly; no fabricated proceedings or page range. |
| Mode lottery | [arXiv:2606.00544](https://arxiv.org/abs/2606.00544), as `@misc` with eprint, archivePrefix, primaryClass, and arXiv DOI. |
| Scale-invariant optimization | [arXiv:2609.09116](https://arxiv.org/abs/2609.09116), using the same preprint convention. |
| Simple diffusion (added 29 September 2026) | [arXiv:2609.33947](https://arxiv.org/abs/2609.33947), using the same preprint convention; title and Hasan Amin, Ming Yin, Rajiv Khanna author order checked against the v1 PDF. Primary class is `cs.CL`. |

The human-readable listing keeps event dates; BibTeX describes the publication record. They need not use identical phrasing. Stable paper IDs, title destinations, PDF/code links, author order, and thumbnails are unaffected by citation presentation.

Original validation (10 September 2026): all 13 entries parsed with the locally available bibtex-ruby parser (no new site dependency). Root and `/preview` builds passed the site checker. Browser checks covered mobile/desktop, both themes, keyboard focus and disclosure, exact clipboard text, denied/unavailable clipboard fallback, no-JavaScript access, and reading progress after expansion.

Addition validation (29 September 2026): all 14 entries parse. The new record appears in both the complete list and the ten selected homepage papers. Browser checks at 1440, 390, and 320px in both themes verify its image, author/title/resource links, keyboard disclosure, exact clipboard contents, and absence of horizontal overflow or script errors. A dark, no-JavaScript `/preview` check verifies the native disclosure and byte-identical paper download. The subsequent publishing pass corrected the unrelated nugget ID to `freedom-or-loneliness`; both root and `/preview` builds now pass the output checker. The 27 Jekyll behavior checks pass.
