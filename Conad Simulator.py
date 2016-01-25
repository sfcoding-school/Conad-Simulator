#!/usr/bin/python
import simpy
from random import randint, gauss, expovariate
from copy import deepcopy
from matplotlib import pyplot as plt
import numpy as np

class ConadSimulator:
    def __init__(self, n_registers, duration, stable_at = 0):
        self.env = simpy.Environment()
        self.n_registers = n_registers
        self.duration = duration
        self.stable_at = stable_at
        self.registers = list()
        for i in xrange(n_registers):
            self.registers.append(simpy.Resource(self.env, capacity = 1))
        self.c_queue = 0
        self.c_registers = 0
        self.c_out = 0
        self.ti = list()
        self.ts = list()
        self.tw = list()
    def start(self):
        self.env.process(self.entrance())
        self.env.run(until = self.duration)
    def customer(self):
        arrival = self.env.now
        j = randint(0, self.n_registers - 1)
        with self.registers[j].request() as c:
            yield c
            if self.env.now > self.stable_at:
                self.tw.append(self.env.now - arrival)
            c_ts = -1
            while c_ts < 0:
                c_ts = gauss(94, 44)
            if self.env.now > self.stable_at:
                self.c_queue -= 1
                self.c_registers += 1
            yield self.env.timeout(c_ts)
            if self.env.now > self.stable_at:
                self.ts.append(c_ts)
                self.c_registers -= 1
                self.c_out += 1
    def entrance(self):
        i = 1
        while True:
            self.env.process(self.customer())
            if self.env.now > self.stable_at:
                self.c_queue += 1
            i += 1
            c_ti = expovariate(1.0 / 25)
            if self.env.now > self.stable_at:
                self.ti.append(c_ti)
            yield self.env.timeout(c_ti)
    def statistics(self):
        print
        print
        print "####################################"
        print "###         Statistics           ###"
        print "####################################"
        print
        total = self.c_queue + self.c_registers + self.c_out
        print "Total customers number: ", total
        print "Enqueued customers number: ", self.c_queue
        print "Customer at the cash registers: ", self.c_registers
        print "Completed customers number: ", self.c_out
        ti = np.mean(self.ti)
        tw = np.mean(self.tw)
        ts = np.mean(self.ts)
        lambd = 1 / (self.n_registers * ti)
        mu = 1 / ts
        rho = lambd / mu
        print "Mean arrival time: ", ti
        print "Mean response time: ", tw + ts
        print "Mean service time: ", ts
        print "Mean waiting time: ", tw
        print "Mean utilization: ", (float(sum(self.ts)) / (self.n_registers * self.duration))
        print "Mean throughput: ", (float(self.c_out / sum(self.ts)))
        print "Lambda: ", lambd
        print "Mu: ", mu
        print "Rho: ", rho,
        if rho < 1:
            print " -> Stable"
        else:
            print " -> Unstable"

def stabilize(n_registers, duration, p):
    results = [list() for i in xrange(p)]
    total_mean = 0
    instable = True
    iteration = 0
    cont = 5
    total = list()
    while instable:
        iteration += 1
        for i in xrange(p):
            sim = ConadSimulator(n_registers, iteration * duration)
            sim.start()
            results[i] = deepcopy(sim.tw)
        old_mean = total_mean
        means = [np.mean(results[i]) for i in xrange(p)]
        total_mean = np.mean(means)
        total.append(total_mean)
        if abs(old_mean - total_mean) < 0.02 * total_mean:
            cont -= 1
            if cont == 0:
                instable = False
        else:
            cont = 5
    print "Stabilized at iteration %d" % iteration
    print "Mean: %lf" % total_mean
    p10 = np.percentile(means, 10)
    p90 = np.percentile(means, 90)
    print "10° percentile: %lf" % p10
    print "90° percentile: %lf" % p90
    plt.plot([i for i in xrange(len(total))], total, "rx")
    plt.hold(True)
    plt.axhline(y = total_mean, color = "black", linestyle = "--")
    plt.ylabel("Mean E(Tw)")
    plt.xlabel("Iteration")
    plt.legend(["Mean of means"], loc = 4)
    plt.show()
    return [iteration, total_mean, p10, p90]

def repeated_measures(n_registers, duration, values, p):
    outside = 0
    inside = 0
    results= list()
    for i in xrange(p):
        j = randint(values[0] / 2, values[0])
        simulator = ConadSimulator(n_registers, (values[0] + j) * duration, values[0] * duration)
        simulator.start()
        total_mean = np.mean(simulator.tw)
        results.append(total_mean)
        if total_mean >= values[2] and total_mean <= values[3]:
            inside += 1
        else:
            outside += 1
    print "Experiments between P10 and P90: %d" % inside
    print "Experiments out of range: %d" % outside
    plt.plot([i for i in xrange(len(results))], results, "rx")
    plt.hold(True)
    plt.axhline(y = values[1], color = "black", linestyle = "--")
    plt.axhline(y = values[2], color = "black", linestyle = "--")
    plt.axhline(y = values[3], color = "black", linestyle = "--")
    plt.ylabel("Mean E(tw)")
    plt.xlabel("Experiments")
    plt.legend(["Tw", "Mean", "P10", "P90"])
    plt.show()
    if outside <= 0.1 * p:
        print "Validated!"
        return True
    else:
        print "Not validated..."
        return False

values = stabilize(5, 1000, 100)
repeated_measures(5, 1000, values, 100)
#simulator = ConadSimulator(5, 1000)
#simulator.start()
#simulator.statistics()
