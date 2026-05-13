from .use_cases.process_message import ProcessMessageUseCase
from .use_cases.get_stats import GetStatsUseCase
from ..domain.ports import IAIProvider, IMessageRepository

class ApplicationServices:
    """Фасад для всех use cases"""
    
    def __init__(self, ai: IAIProvider, repo: IMessageRepository):
        self.process_message = ProcessMessageUseCase(ai, repo)
        self.get_stats = GetStatsUseCase(repo)