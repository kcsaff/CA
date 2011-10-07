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
import topologies.torus, topologies.rectangle
import simple
import rules.water, rules.life, rules.redox, rules.rivers


class World(simple.typed_object):
    generation = 0
    _scratch_charts = None
    _compiled_rule = None
    _compiled_topology = None

    def __init__(self):
        simple.typed_object.__init__(self, 'world')
        self.toys = self.toys or set()
    
    def __setattr__(self, attr, value):
        simple.typed_object.__setattr__(self, attr, value)
        if attr == 'rule':
            self.compile_rule()
        elif attr == 'topology':
            self.compile_topology()
    
    def _stitch(self):
        self.charts[0].stitch(self.charts)
        
    def _evolve_check(self):
        if self.rule is None:
            raise RuntimeError

        if self.algorithm.rule != self.rule:
            self.compile_rule()
        if self._compiled_topology != self.topology:
            self.compile_topology()

        if (self.generation == 0
                or not self._scratch_charts 
                or self.charts[0].shape != self._scratch_charts[0].shape
                or self.charts[0].dtype != self._scratch_charts[0].dtype):
            self._stitch()
            self._create_scratch_charts()
        
    def evolve(self, generations = 1):
        self._evolve_check()
            
        for _ in range(generations):
            for chart, scratch in zip(self.charts, self._scratch_charts):
                self.algorithm(chart, scratch)
            self.charts, self._scratch_charts = self._scratch_charts, self.charts
            self._stitch()
            for toy in self.toys:
                toy.evolve(self)
            self.generation += 1
        
    def _create_scratch_charts(self):
        self._scratch_charts = [chart.copy() for chart in self.charts]
            
    def set(self, point, state):
        mapped_point = self.charts[0].map_point(point)
        for chart in self.charts: #This can't be _quite_ right.
            chart[tuple(mapped_point)] = state   
            
    def get(self, point):
        mapped_point = self.charts[0].map_point(point)
        return self.charts[0][mapped_point]    

    def compile_rule(self):
        self.algorithm = registry.get.compile_rule(self.rule)
        self.algorithm.rule = self.rule
        if self.charts:
            self.charts = [registry.get.convert_chart(chart, self.algorithm)
                           for chart in self.charts]
        elif self.topology:
            self.charts = [registry.get.create_chart(self.algorithm, self.topology)]

    def compile_topology(self):
        if self.charts:
            self.charts = [registry.get.change_topology(chart, self.topology)
                           for chart in self.charts]
        elif self.algorithm:
            self.charts = [registry.get.create_chart(self.algorithm, self.topology)]
        self._compiled_topology = self.topology
            
def default():
    result = World()
    result.topology = topologies.torus.torus(640, 480)
    result.rule = rules.life.brain()#rules.redox.redox() #rules.life.brain()
    return result          
  
def water():
    result = World()
    result.topology = topologies.rectangle.rectangle(640, 480)
    result.rule = rules.water.water()
    return result

def rivers():
    result = World()
    result.topology = topologies.torus.fall(640, 480, fall=100)
    result.rule = rules.rivers.rivers()
    return result
