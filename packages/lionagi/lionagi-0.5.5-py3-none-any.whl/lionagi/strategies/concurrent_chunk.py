from typing import ClassVar

from lionagi.libs.func.types import bcall
from lionagi.libs.parse.types import to_list
from lionagi.protocols.operatives.instruct import Instruct, InstructResponse

from .concurrent import ConcurrentExecutor
from .params import ChunkStrategyParams


class ConcurrentChunkExecutor(ConcurrentExecutor):
    """Executor for concurrent chunked instruction processing.

    Breaks instructions into chunks and executes each chunk concurrently.
    """

    params: ChunkStrategyParams | None = None
    params_cls: ClassVar[type[ChunkStrategyParams]] = ChunkStrategyParams

    async def execute(
        self, res
    ) -> tuple[list[Instruct], list[InstructResponse]]:
        async with self.session.branches:
            instructs = []
            response_ = []
            if hasattr(res, "instruct_models"):
                instructs: list[Instruct] = res.instruct_models
                ress = []
                async for chunk_result in await bcall(
                    instructs,
                    self.instruct_concurrent_single,
                    execute_branch=self.execute_branch,
                    batch_size=self.params.chunk_size,
                    **self.params.rcall_params.to_dict(),
                ):
                    ress.extend(chunk_result)

                ress = to_list(ress, dropna=True, flatten=True)
                response_ = [r for r in ress if not isinstance(r, (str, dict))]
                response_ = to_list(
                    response_, unique=True, dropna=True, flatten=True
                )
            return instructs, response_
