import os
import tqdm
import evaluate
import datasets
from tts_evaluate_yue import Normalizer
from tts_evaluate_yue.asr.huggingface import ASR
from tts_evaluate_yue.tts.gtts import TTS
from tts_evaluate_yue import load_cer

normalizer = Normalizer()
asr = ASR(

)
tts = TTS()
language = "yue"
spk = "粤语女"
dataset = datasets.load_dataset("tts_evaluate_yue", "yue")

cer_asr = load_cer()
cer_tts_asr = load_cer()

for one_sample in tqdm.tqdm(dataset):
    transcription = one_sample["raw_transcription"]
    audio = one_sample["audio"]["array"]

    # asr
    asr_result = asr.get_asr(audio, language=language)

    # tts
    tts_result, sr = tts.get_tts(transcription, sample_rate=16000)
    tts_asr_result = asr.get_asr(tts_result, language=language)

    cer_tts_asr.add(
        reference=normalizer.normalize(transcription),
        prediction=normalizer.normalize(tts_asr_result),
    )
    cer_asr.add(
        reference=normalizer.normalize(transcription),
        prediction=normalizer.normalize(asr_result),
    )

cer_tts_asr.compute(), cer_asr.compute()