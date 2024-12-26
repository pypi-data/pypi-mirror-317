from typing import Optional

class TTS:
    def __init__(
        self,
        cosyvoice_path: str,
        load_jit: bool = True,
        load_onnx: bool = False,
        fp16: bool = True,
        spk: str = "粤语女",
        **kwargs
    ):
        from cosyvoice.cli.cosyvoice import CosyVoice

        self.cosyvoice = CosyVoice(
            cosyvoice_path, load_jit=load_jit, load_onnx=load_onnx, fp16=fp16, **kwargs
        )
        try:
            print(self.cosyvoice.list_avaliable_spks())
        except:
            print("Failed to list available speakers")
        
        self.spk = spk

    def get_tts(self, text, sample_rate: Optional[int] = None):
        import torchaudio

        tts_result = list(self.cosyvoice.inference_sft(text, self.spk, stream=False))[0][
            "tts_speech"
        ]
        if sample_rate is not None:
            return torchaudio.transforms.Resample(22050, sample_rate)(tts_result), sample_rate

        return tts_result, 22050

