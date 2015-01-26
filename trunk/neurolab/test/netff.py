﻿# coding: utf-8import unittestimport numpy as npimport neurolab as nlfrom neurolab.error import MSE, SSE, SAE, MAE, CEEfrom neurolab.train import train_gd, train_gdm, train_gda, train_gdx, train_rpropfrom neurolab.train import train_bfgs, train_cg, train_ncgclass TestFF(unittest.TestCase):        def check(self, funcs, test, goal):        size = 20        # Create train samples        x = np.linspace(-7, 7, size).reshape(size, 1)        y = np.sin(x) * 0.5                for func in funcs:            net = nl.net.newff([[-7, 7]],[5, 1])            if test == 'train' or test == 'train_reg':                net.trainf = func            if test == 'error':                net.errorf = func            if test == 'init':                for l in net.layers:                    l.initf = func                net.init()            # Train network            error = net.train(x, y, epochs=500, show=0, goal=goal)            if error[-1] >= goal:                # repeat train                net.init()                error = net.train(x, y, epochs=1000, show=0, goal=goal)            # Simulate network            out = net.sim(x)            # Tests            self.assertLessEqual(error[-1], error[0])            self.assertLess(error[-1], goal)            if test != 'train_reg':                self.assertEqual(error[-1], net.errorf(y, out))            self.assertLess(np.sum(np.abs(y - out)) / len(x), goal * 10)        def test_default(self):        funcs = [1, 2, 3]        self.check(funcs, None, 0.5)        def test_error(self):        funcs = [MSE(), SSE(), MAE()]        self.check(funcs, 'error', 0.5)        def test_error_sae(self):        funcs = [SAE()]        self.check(funcs, 'error', 5.0)        def test_error_cee(self):        size = 20        goal = 1        # Create train samples        x = np.linspace(-7, 7, size).reshape(size, 1)        y = np.sin(x) * 0.4 + 0.5                net = nl.net.newff([[-7, 7]],[5, 1])        net.layers[-1].transf = nl.trans.LogSig()        # Train network        error = net.train(x, y, epochs=500, show=0, goal=goal)        # Simulate network        out = net.sim(x)        # Tests        self.assertLessEqual(error[-1], error[0])        self.assertLess(error[-1], goal)        self.assertEqual(error[-1], net.errorf(y, out))        self.assertLess(np.sum(np.abs(y - out)) / len(x), goal * 10)        def test_train_gd(self):        funcs = [train_gd]        self.check(funcs, 'train', 1)        def test_train_gd_other(self):        funcs = [train_gdm, train_gda, train_gdx, train_rprop]        self.check(funcs, 'train', 0.5)        def test_train_spo(self):        funcs = [train_bfgs, train_cg, train_ncg]        self.check(funcs, 'train', 0.5)        def test_init(self):        funcs = [nl.init.initwb_reg,                nl.init.InitRand([-1.0, 1.0], 'wb'),                nl.init.InitRand([-.5, .5], 'wb'),                nl.init.initnw,                nl.init.initwb_lin]        self.check(funcs, 'init', 1)        def test_adapt(self):        funcs = [nl.train.trainer(nl.train.gd.TrainGD, adapt=False),                    nl.train.trainer(nl.train.gd.TrainGDM, adapt=False),                    nl.train.trainer(nl.train.gd.TrainGDA, adapt=False),                    nl.train.trainer(nl.train.gd.TrainGDX, adapt=False),                    nl.train.trainer(nl.train.gd.TrainRprop, adapt=False),                ]        self.check(funcs, 'train', 0.5)        def test_train_reg(self):        funcs = [nl.train.trainer(nl.train.gd.TrainGD, rr=0.5),                    nl.train.trainer(nl.train.gd.TrainGDM, rr=0.5),                    nl.train.trainer(nl.train.gd.TrainGDA, rr=0.5),                    nl.train.trainer(nl.train.gd.TrainGDX, rr=0.5),                    nl.train.trainer(nl.train.spo.TrainBFGS, rr=0.5),                    nl.train.trainer(nl.train.spo.TrainCG, rr=0.5),                    nl.train.trainer(nl.train.spo.TrainNCG, rr=0.5),                ]        self.check(funcs, 'train_reg', 1.5)    