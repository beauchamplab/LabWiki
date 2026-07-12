---
layout: default
title: "AVHuBERT"
date_created: "2026-06-19"
parent: Resources and Data Sharing
grand_parent: Beauchamp
---

# AVHuBERT

> Quick Access
> - [Home](../index.md "Beauchamp")
> - [Publications](../Publications_and_Talks/Publications.md "Beauchamp:Publications")
> - [Resources](../Resources_and_Data_Sharing/DataSharing.md "Beauchamp:DataSharing")

_Date created: 2026-06-19_

Conversation with Li Zhu 2026-06-19

Thanks for your interest in our work! I have attached the inference loop (probability_prediction.txt) and the helper functions (common.txt) to this email. You should be able to use AVHuBERT in a pipeline like the original demo.ipynb using these two scripts, which contain all the modifications we made for our tasks.  

In the common.txt, you’ll find a function called “predict". This is the key function that we adapted from the original AVHuBERT repository for top prediction extraction + variant creation. In line 244 you’ll see the variants are created just by adding a pre-defined Gaussian noise to the target layers (with seeds of course).

And in probability_prediction.txt, you will need to define the variables for the prediction — beam_size_list , alpha_list (the variance of the Gaussian noise), tgt_layers (the top n layers you want to add noise), n_subjects (how many VAH variants you’d like) and permute_transformer (scramble all the weights in transformers). And the numbers in this file are what we used in our paper. 

![](../../../attachments/unclassified/Pasted%20image%2020260619102439.png)

Regarding finetuning, we used the one finetuned by the authors at Meta (the last AVHuBERT-large 433h model in this sheet). No extra training/finetuning was done by us.

The rest of the code can be found in [https://github.com/T4phage76/av_hubert.git](https://github.com/T4phage76/av_hubert.git "https://github.com/T4phage76/av_hubert.git"). The inference was set to run on CPU. If you want to run it on CUDA, you might want to uncomment the to_gpu helper function.
