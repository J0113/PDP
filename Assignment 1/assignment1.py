from mrjob.job import MRJob
from mrjob.step import MRStep

class RatingsBreakdown (MRJob):

    # 0. Initiallise MRJob with the steps.
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

    # 1. Map the Movie ID's
    def mapper(self, _, line):
        (userlD, movielD, rating, timestamp) = line.split('\t')
        yield movielD, 1

    # 2. Combine the Movie ID's with the amount of times it is in the file (aka count)
    def combiner(self, key, counts):
        yield key, sum(counts)

    # 3. Reduce to an count
    def reducer(self, key, values):
        yield None, (sum(values), key)
    
    # 4. Order from least to most amount of ratings
    def reducer_sort(self, _, values):
        for count, key in sorted(values):
            yield (int(key), int(count))

# Run if main.
if __name__ == '__main__':
    RatingsBreakdown.run() 