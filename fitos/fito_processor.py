from tqdm import tqdm
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
import time

class Processor():
    def __init__(self, number_workers= min(32, 5 * cpu_count())):
        if number_workers <= 0:
            raise ValueError(f"number_workers must be positive, got {number_workers}")
        self.number_workers = number_workers

    def run(self, entities,_process, description_process='Processing entities', description_unit='entity'):
        start_time = time.perf_counter()
        results = []
        progress = lambda it: tqdm(
            it,
            total= len(entities),
            desc= description_process,
            unit= description_unit,
        )

        if self.number_workers <= 1:
            for item in progress(entities):
                results.append(_process(item))
            return results

        with ThreadPool(processes=self.number_workers) as pool:
            for result in progress(pool.imap(_process, entities)):
                results.append(result)
            pool.close()
            pool.join()

        end_time = time.perf_counter()
        return {
                    'results': results,
                    'message': f'Elapsed load time: {(end_time - start_time):.4f} seconds',
                }