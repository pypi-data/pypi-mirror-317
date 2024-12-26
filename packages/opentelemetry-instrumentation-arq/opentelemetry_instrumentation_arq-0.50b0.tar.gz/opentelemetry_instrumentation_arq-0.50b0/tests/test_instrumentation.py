import unittest

from arq import ArqRedis, cron, func
from opentelemetry.instrumentation.arq import ArqInstrumentor
from wrapt import BoundFunctionWrapper, ObjectProxy


async def test(ctx):
    return 2


class TestInstrument(unittest.IsolatedAsyncioTestCase):
    async def test_instrument(self) -> None:
        instrumentation = ArqInstrumentor()
        instrumentation.instrument()

        self.assertTrue(isinstance(ArqRedis.enqueue_job, BoundFunctionWrapper))

        test_cases = [cron(test), func(test)]

        for case in test_cases:
            self.assertEqual(await case.coroutine({}, *list(), **dict()), 2)
            self.assertTrue(case.coroutine, ObjectProxy)

        # test uninstrument
        instrumentation.uninstrument()
        test_cases = [cron(test), func(test)]
        self.assertFalse(isinstance(ArqRedis.enqueue_job, BoundFunctionWrapper))
        for case in test_cases:
            self.assertFalse(isinstance(case.coroutine, ObjectProxy))


if __name__ == "__main__":
    unittest.main()
