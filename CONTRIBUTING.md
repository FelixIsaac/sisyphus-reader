# Contributing to *The Myth of Sisyphus* Project

Thank you for your interest in contributing to this open-source critical edition and reading companion!

This project bridges classical 20th-century continental philosophy and modern digital humanities. We welcome contributions that improve translation clarity, correct textual errors, enhance UI accessibility, or refine the "Philosophical Move" analytical keys.

---

## 1. The Core Standard: Dignified Modern Literary English

All contributions to the translation and annotations MUST adhere to the **Dignified Modern Literary English** register (in the standard of Penguin Classics or NYRB Classics, e.g., Matthew Ward or Robin Buss).

### The 6 Iron Laws of Lossless Translation:
1. **Invariant Logic:** Never drop a premise, soften a paradox, or skip a syllogism. Every logical pivot Camus makes must remain intact.
2. **Vocabulary Unmasking:** Translate dated Latinate vocabulary into clear, muscular English (*e.g.*, unmask "philosophical suicide" as *intellectual surrender*, "lucidity" as *radical mental clarity*, and "revolt" as *active defiance*).
3. **Syntactic De-nesting:** Untangle 1950s periodic clauses and inverted French sentence structures into direct, punchy sentences without diluting the philosophical weight.
4. **Relational Absurdity:** The Absurd is **never** "weirdness" or "goofiness." It is strictly the collision between the human hunger for purpose and the world's stubborn silence. Never use the word "absurd" as casual slang.
5. **Concrete Anchors:** Preserve every single physical metaphor Camus uses (the boulder, the hillside, the revolver, the streetcar, the mime, the stage curtain, the condemned man at dawn).
6. **Zero Motivational Platitudes:** Camus is not a self-help author. Never reduce existential revolt to pop-psychology, internet slang, or motivational platitudes.

---

## 2. Contribution Workflow

1. **Fork the Repository:** Create your own fork and work on a feature branch (`git checkout -b feature/refine-c3-p4`).
2. **Data Structure:** Edit the corresponding chapter file in `translations/<section_id>.json`.
   - Ensure the JSON schema remains valid.
   - Maintain 1-to-1 bijective correspondence between `orig_sentences` and `mod_sentences` so that interactive sentence highlighting works in the web reader.
3. **Rebuild & Verify:**
   Run the master build pipeline to verify that all editions compile without error:
   ```bash
   python3 build.py
   ```
4. **Submit a Pull Request:**
   - Clearly explain what changed and why.
   - Confirm that your changes comply with the Dignified Modern Literary English standard.
   - By submitting a pull request, you agree that your code contributions are licensed under the [MIT License](./LICENSE) and your editorial/translation contributions are licensed under [CC BY-NC-SA 4.0](./LICENSE).

---

## 3. Reporting Issues & Corrections

- If you spot a typo, a dropped sentence, or a misaligned sentence match, please open an Issue with the tag `[Typo]` or `[Alignment]`.
- If you believe an analytical key ("The Philosophical Move") can be clarified or improved, please cite the chapter and paragraph number (`e.g., c4-p7`).
