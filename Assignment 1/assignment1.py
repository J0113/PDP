from mrjob.job import MRJob
from mrjob.step import MRStep

class RatingsBreakdown (MRJob):

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper,
                combiner=self.combiner,
                reducer=self.reducer
            ),
			MRStep(
                reducer=self.reducer_sort
            )
        ] 

    def mapper(self, _, line):
        (userlD, movielD, rating, timestamp) = line.split('\t')
        yield movielD, 1

    def combiner(self, key, counts):
        yield key, sum(counts)

    def reducer(self, key, values):
        yield None, (sum(values), key)
        
    def reducer_sort(self, _, values):
        for count, key in sorted(values):
            yield (int(key), int(count))

if __name__ == '__main__':
    RatingsBreakdown.run() 