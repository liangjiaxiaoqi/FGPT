<!-- # FGPT
FGPT can assist in EEG decoding based on the Transformer framework, serving as a scalable approach. We will update the code shortly.
-->

# Frequency-Gated Prompting for Enhancing Transformer-based EEG Decoding

🎉🎉🎉 **News:** Our paper has been officially accepted by ***IEEE Journal of Biomedical and Health Informatics***! 🎉🎉🎉

This repository contains the official implementation of **FGPT**. In this work, we propose a lightweight approach termed Frequency-Gated Prompted Transformer (FGPT) designed for efficient electroencephalogram (EEG) decoding. FGPT can assist in EEG decoding based on the Transformer framework, serving as a scalable approach. We will update the code shortly.

---

## ✨ Motivation

In EEG decoding, Transformer models have garnered significant attention due to their exceptional temporal modeling capabilities; however, their lack of perception for critical frequency-domain features within EEG signals constrains further performance enhancement. Most existing methods rely on complex network structures or multi-branch parallel architectures, which lead to significant computational redundancy and disrupt the continuity of the EEG sequence structure. To address this issue, we propose a parameter-efficient, lightweight modeling paradigm using sparse frequency tokens.

<div align="center">
  <img src="image/gagraphic.jpg" alt="Figure 1" width="80%">
  <p><em>Figure 1: Sparse frequency tokens are used for prompt fine-tuning of the Transformer network for EEG decoding, enabling global frequency component modeling while preserving the temporal-spatial integrity of the original sequence.</em></p>
</div>

---

## 🚀 Model Architecture

Our FGPT utilizes sparse token prompt learning based on gated fusion to model the frequency components of Transformers while avoiding disrupting the spatio-temporal continuity of the original sequence. It adaptively represents global EEG rhythms by introducing learnable sparse frequency prompt tokens and synergistically embedding them with the original EEG sequence into the Transformer's self-attention computation.

<div align="center">
  <img src="assets/figure2.png" alt="Figure 2" width="80%">
  <p><em>Figure 2: The computational process for different tokens after embedding sparse frequency prompts into the attention layer, and the removal of sparse frequency prompt operations.</em></p>
</div>

---

## 📊 Experimental Results

Extensive experiments demonstrate that FGPT improves the decoding performance and robustness of evaluated Transformer-based models on multiple baselines.

* **Cognitive Attention (Dataset A):** FGPT elevated the average accuracy of EEG-ViT, EEG-Conformer, and EEG-Deformer by 1.74%, 1.56%, and 3.87%, respectively.
* **Fatigue Driving (Dataset B):** The introduction of FGPT enhanced the performance across different backbone models.
* **Mental Cognitive Work (Dataset C):** FGPT elevated the F1-macro scores with average gains of 1.51%, 1.59%, and 3.90% across the three evaluated models.
* **Computational Efficiency:** Integrating FGPT incurs only minimal additional overhead across models, achieving substantial performance enhancements at a negligible resource cost.

<div align="center">
  <img src="assets/figure3.png" alt="Figure 3" width="80%">
  <p><em>Figure 3: Accuracy-Computation Complexity scatter plot comparison of three Transformer-Based EEG decoding models before and after applying FGPT.</em></p>
</div>

---

## 🛠️ Usage

### Preparations
```bash
# Clone the repository
git clone [https://github.com/liangjiaxiaoqi/FGPT.git](https://github.com/liangjiaxiaoqi/FGPT.git)
cd FGPT
