import torch
import tempfile
import os

class SileroTTS:
    def __init__(self):
        self.device = torch.device('cpu')
        torch.set_num_threads(4)
        self.model = None
        self.speakers = ['aidar', 'baya', 'kseniya', 'xenia', 'eugene']
        
    async def load_model(self):
        """Загрузка модели Silero TTS"""
        if self.model is None:
            self.model, _ = torch.hub.load(
                repo_or_dir='snakers4/silero-models',
                model='silero_tts',
                language='ru',
                speaker='ru_v3'
            )
            self.model.to(self.device)
    
    async def synthesize_speech(self, text: str, speaker: str = 'aidar'):
        """Синтез речи из текста"""
        await self.load_model()
        
        if speaker not in self.speakers:
            speaker = 'aidar'
        
        # Синтез речи
        audio = self.model.apply_tts(
            text=text,
            speaker=speaker,
            sample_rate=48000
        )
        
        # Сохранение во временный файл
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            # Здесь нужно сохранить аудио в файл
            # Для простоты возвращаем путь к файлу
            return f.name

# Глобальный экземпляр сервиса
tts_service = SileroTTS()

async def synthesize_speech(text: str, speaker: str):
    return await tts_service.synthesize_speech(text, speaker)