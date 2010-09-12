# Copyright (C) 2010 by Kevin Saff

# This file is part of the CA scanner.

# The CA scanner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# The CA scanner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with the CA scanner.  If not, see <http://www.gnu.org/licenses/>.

import numpy
import registry
from topology import torus
from cascading_object import cascading_object
import rules.water, rules.life

def _default_chart():
    chart = numpy.zeros(shape=(640, 480), dtype=numpy.uint8)
    chart[:,:] = numpy.random.randint(0, 2, size=chart.shape)
    return chart

def _water_chart():
    chart = numpy.zeros(shape=(640, 480), dtype=numpy.float)
    chart[:,:] = numpy.random.rand(*chart.shape)
    chart *= 255.9
    return chart
    
class World(cascading_object):
    _scratch_charts = None
    generation = 0
    compiled_rule = None
    
    def _stitch(self):
        self.topology.stitch(self.charts)
        
    def evolve(self, generations = 1):
        if self.compiled_rule != self.rule:
            self.compile_rule()

        if self.generation == 0:
            self._stitch()
            self._create_scratch_charts()
            
        for _ in range(generations):
            for chart, scratch in zip(self.charts, self._scratch_charts):
                self.algorithm(chart, scratch, self.table)
            self.charts, self._scratch_charts = self._scratch_charts, self.charts
            self._stitch()
            for toy in self.toys:
                toy.evolve(self)
            self.generation += 1
        
    def _create_scratch_charts(self):
        self._scratch_charts = [chart.copy() for chart in self.charts]
            
    def set(self, point, state):
        #print 'setting', point, state
        mapped_point = self.topology.map_point(point, self.charts[0])
        for chart in self.charts: #This can't be _quite_ right.
            chart[mapped_point] = state   
            
    def get(self, point):
        mapped_point = self.topology.map_point(point, self.charts[0])
        return self.charts[0][mapped_point]    

    def compile_rule(self):
        self.algorithm, self.table, _ = registry.get.compile_rule(self.rule)
            
def default():
    result = World(source='default')
    result.topology = torus
    result.charts = [_default_chart()]
    result.rule = rules.life.brain()
    result.toys = set()
    result.generation = 0
    return result          
  
def water():
    result = World(source='water')
    result.topology = torus
    result.charts = [_water_chart()]
    result.rule = rules.water.water()
    result.toys = set()
    result.generation = 0
    return result
