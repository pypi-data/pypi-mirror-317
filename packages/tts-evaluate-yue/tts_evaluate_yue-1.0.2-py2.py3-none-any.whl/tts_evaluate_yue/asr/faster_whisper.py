class ASR:
    def __init__(self, whisper_path: str):
        import faster_whisper

        self.whisper = faster_whisper.WhisperModel(
            model_size_or_path=whisper_path,
        )

    def get_asr(self, audio, language, **kwargs):
        if language is None or language == "auto":
            language = None
        asr_segements, info = self.whisper.transcribe(
            audio, language=language, **kwargs
        )
        asr_result = "".join([seg.text for seg in asr_segements])
        return asr_result, info.language
    