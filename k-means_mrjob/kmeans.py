from mrjob.job import MRJob
# MRJob is a python class which will be overloaded
from math import sqrt


class KMeans(MRJob):
    SORT_VALUES = True
    OUTPUT_PROTOCOL = mrjob.protocol.RawProtocol

    def dist_vec(self, v1, v2):
        return sqrt((v2[0] - v1[0]) * (v2[0] - v1[0]) + (v2[1] - v1[1]) * (v2[1] - v1[1]))

    def mapper(self, _, lines):
        centroids = self.get_centroids()
        for val in lines.split('\n'):
            x, y = val.split(', ')
            point = [float(x), float(y)]
            min_dist = float('inf')
            class_ = 0
            for i in range(3):
                dist = self.dist_vec(point, centroids[i])
                if dist < min_dist:
                    min_dist = dist
                    class_ = i
            yield class_, point

    def configure_options(self):
        super(KMeans, self).configure_options()
        self.add_file_option('--c')

    def get_centroids(self):
        f = open(self.options.c, 'r')
        centroids = []
        for line in f.read().split('\n'):
            if line:
                x, y = line.split(', ')
                centroids.append([float(x), float(y)])
        f.close()
        return centroids

    def reducer(self, k, v):
        count = 0
        x = y = 0.0
        for t in v:
            count += 1
            x += t[0]
            y += t[1]
        print(str(k) + ", " + str(x / count) + ", " + str(y / count))

    def combiner(self, k, v):
        count = 0
        x = y = 0.0
        for t in v:
            x += t[0]
            y += t[1]
            count += 1
        yield k, (x / count, y / count)


if __name__ == '__main__':
    KMeans.run()
