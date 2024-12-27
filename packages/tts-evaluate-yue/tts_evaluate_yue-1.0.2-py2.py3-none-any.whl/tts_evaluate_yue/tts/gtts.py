import tempfile
from typing import Optional


class TTS:
    def __init__(
        self,
        **kwargs
    ):
        pass

    def get_tts(self, text, sample_rate: Optional[int] = None):
        import gtts
        import torchaudio
        import soundfile as sf

        tts = gtts.gTTS(text)
        with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
            tts.save(f.name)
            f.seek(0)
            audio, sr = sf.read(f.name)
            if sample_rate is not None:
                audio = torchaudio.transforms.Resample(sr, sample_rate)(audio)
                sr = sample_rate
        return audio, sr