import porespy as ps
import scipy as sp


class SimulationTest():
    def setup_class(self):
        self.l = 100
        self.im = ps.generators.overlapping_spheres(shape=[self.l, self.l],
                                                    radius=5,
                                                    porosity=0.5)
        self.mip = ps.simulations.Porosimetry(self.im)
        self.blobs = ps.generators.blobs([self.l, self.l, self.l])
        self.rw = ps.simulations.RandomWalk(image=self.blobs)
        self.blobs_2d = ps.generators.blobs([self.l, self.l]).astype(int)
        self.rw_2d = ps.simulations.RandomWalk(image=self.blobs_2d, seed=True)

    def test_porosimetry(self):
        self.mip.run()
        assert self.mip.result.dtype == float

    def test_plot_drainage_curve(self):
        fig = self.mip.plot_drainage_curve()
        ax = fig.get_axes()[0]
        line = ax.lines[0]
        assert line.get_ydata()[0] == 1.0

    def test_plot_size_histogram(self):
        fig, counts, bins, bars = self.mip.plot_size_histogram()
        assert sp.sum(counts) == int(sp.sum(self.mip.result > 0))

    def test_random_walk(self):
        r'''
        All tests for RandomWalk are done in pytrax. We are just testing that
        the package imports ok and runs
        '''
        self.rw.run(nt=1000, nw=100, stride=1)
        assert sp.shape(self.rw.real_coords) == (1000, 100, 3)


if __name__ == '__main__':
    t = SimulationTest()
    t.setup_class()
    t.test_porosimetry()
    t.test_plot_drainage_curve()
    t.test_plot_size_histogram()
    t.test_random_walk()
