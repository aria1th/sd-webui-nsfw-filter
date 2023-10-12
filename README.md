# sd-webui-nsfw-filter
immediate nsfw protection for your colab, based on nsfwjs(https://github.com/infinitered/nsfwjs)
onnx runtime converted model by DeepGHS (https://huggingface.co/deepghs/imgutils-models/blob/main/nsfw/nsfwjs.onnx)

# How to use
Just installing (and enabling) the extension activates NSFW filter.
The detected result images will be blurred, both in result image file, and result views.

Example generated with GhostMix:
(Maybe blur strength was not enough...)
![image](https://github.com/aria1th/sd-webui-nsfw-filter/assets/35677394/156b6d78-1e82-4967-a419-6382dfb58cbf)

# Cautions
**The extension may not be able to totally block the results!**
Especially, it is mainly developed for 3d or real adult images.

Which means it has bias on trained dataset, it cannot block **'really dangerous images'**, thus, you might have to preprocess prompt with another extension for real safety.
