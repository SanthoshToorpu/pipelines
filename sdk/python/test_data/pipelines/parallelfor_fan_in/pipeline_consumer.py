from typing import List

from kfp import compiler
from kfp import dsl


@dsl.component
def double(num: int) -> int:
    return 2 * num


@dsl.component
def add(nums: List[List[int]]) -> int:
    import itertools
    return sum(itertools.chain(*nums))


@dsl.pipeline
def add_pipeline(nums: List[List[int]]) -> int:
    return add(nums=nums).output


@dsl.pipeline
def math_pipeline() -> int:
    with dsl.ParallelFor([1, 2, 3]) as f:
        t = double(num=f)

    return add_pipeline(nums=dsl.Collected(t.output)).output


if __name__ == '__main__':
    compiler.Compiler().compile(
        pipeline_func=math_pipeline,
        package_path=__file__.replace('.py', '.yaml'))
