# -*- coding: utf-8 -*-

def startRep(PORT):
    import os, timeit
    from ..calculation.algorithm import generateProcess
    import zmq
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect(PORT) #tcp://localhost:8000
    print(PORT)
    print("Worker {} is awaiting orders...".format(os.getpid()))
    while True:
        type_num, mechanismParams, GenerateData, algorithmPrams = socket.recv_multipart()
        alg = 'Genetic' if type_num==0 else 'Firefly' if type_num==1 else "Differtial Evolution"
        print("Receive target:")
        print("Algorithm: "+alg)
        print("Through: {}".format(mechanismParams['targetPath']))
        print(mechanismParams)
        print(GenerateData)
        print(algorithmPrams)
        print("Start Algorithm...")
        t0 = timeit.default_timer()
        TnF, FP = generateProcess(type_num, mechanismParams, GenerateData, algorithmPrams)
        t1 = timeit.default_timer()
        time_spand = t1-t0
        mechanism = {
            'Algorithm':alg,
            'time':time_spand,
            'Ax':FP[0], 'Ay':FP[1],
            'Dx':FP[2], 'Dy':FP[3],
            'L0':FP[4], 'L1':FP[5], 'L2':FP[6], 'L3':FP[7], 'L4':FP[8],
            'mechanismParams':mechanismParams,
            'GenerateData':GenerateData,
            'algorithmPrams':algorithmPrams,
            'TimeAndFitness':TnF}
        print('total cost time: {:.4f} [s]'.format(time_spand))
        socket.send(mechanism, time_spand)
