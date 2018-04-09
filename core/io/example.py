# -*- coding: utf-8 -*-

"""All examples of Pyslvs."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

#TODO: Add examples as expression.

example_list = {
    "Ball lifter (Double six bar linkage)": "M[" +
        "J[R, color[Green], P[10.2, 10.4], L[ground, link_1]], " +
        "J[R, color[Green], P[7.44, 20.01], L[link_1, link_2, link_6]], " +
        "J[R, color[Green], P[-10.52, 11.21], L[link_2, link_3]], " +
        "J[R, color[Green], P[-28.48, 2.42], L[link_2, link_4]], " +
        "J[R, color[Green], P[-6.6, 0.0], L[ground, link_3]], " +
        "J[R, color[Green], P[-12.8, 0.0], L[ground, link_5]], " +
        "J[R, color[Green], P[-22.61, 12.64], L[link_4, link_5]], " +
        "J[R, color[Green], P[-56.1, 6.78], L[link_4]], " +
        "J[R, color[Green], P[43.78, 20.17], L[ground, link_7]], " +
        "J[R, color[Green], P[15.02, 40.85], L[link_6, link_7]], " +
        "J[R, color[Green], P[22.0284, 59.8421], L[link_6, link_8]], " +
        "J[R, color[Green], P[23.8, 0.0], L[ground, link_9]], " +
        "J[R, color[Green], P[35.64, 40.55], L[link_8, link_9]], " +
        "J[R, color[Green], P[8.73, 80.39], L[link_8]]" +
        "]",
    
    "Crank rocker": "M[" +
        "J[R, color[Green], P[0.0, 0.0], L[ground, link_1]], " +
        "J[R, color[Green], P[12.92, 32.53], L[link_1, link_2]], " +
        "J[R, color[Green], P[73.28, 67.97], L[link_2, link_3]], " +
        "J[R, color[Green], P[33.3, 66.95], L[link_2]], " +
        "J[R, color[Green], P[90.0, 0.0], L[ground, link_3]]" +
        "]",
    
    "Crank slider": "M[" +
        "J[R, color[Green], P[-67.38, 36.13], L[ground, link_1]], " +
        "J[R, color[Green], P[-68.925, 55.925], L[link_1, link_2]], " +
        "J[RP, A[0.0], color[Green], P[11.88, 0.0], L[ground, link_2]], " +
        "J[R, color[Green], P[50.775, 24.7908], L[link_3, link_4]], " +
        "J[R, color[Green], P[74.375, 7.625], L[ground, link_4]], " +
        "J[R, color[Green], P[11.88, 0.0], L[link_2, link_3]], " +
        "J[R, color[Green], P[93.1526, 56.4121], L[link_3]]]",
    
    
    "Jansen's linkage (Single)": "M[" +
        "J[R, color[Green], P[0.0, 0.0], L[ground, link_1]], " +
        "J[R, color[Green], P[9.61, 11.52], L[link_1, link_2, link_4]], " +
        "J[R, color[Blue], P[-38.0, -7.8], L[ground, link_3, link_5]], " +
        "J[R, color[Green], P[-35.24, 33.61], L[link_2, link_3]], " +
        "J[R, color[Green], P[-77.75, -2.54], L[link_3, link_6]], " +
        "J[R, color[Green], P[-20.1, -42.79], L[link_4, link_5, link_7]], " +
        "J[R, color[Green], P[-56.05, -35.42], L[link_6, link_7]], " +
        "J[R, color[Green], P[-22.22, -91.74], L[link_7]]" +
        "]",
    
    "Jansen's linkage (Double)": "M[" +
        "J[R, color[Green], P[0.0, 0.0], L[ground, link_1]], " +
        "J[R, color[Green], P[9.61, 11.52], L[link_1, link_2, link_4, link_8, link_10]], " +
        "J[R, color[Blue], P[-38.0, -7.8], L[ground, link_3, link_5]], " +
        "J[R, color[Green], P[-35.24, 33.61], L[link_2, link_3]], " +
        "J[R, color[Green], P[-77.75, -2.54], L[link_3, link_6]], " +
        "J[R, color[Green], P[-20.1, -42.79], L[link_4, link_5, link_7]], " +
        "J[R, color[Green], P[-56.05, -35.42], L[link_6, link_7]], " +
        "J[R, color[Green], P[-22.22, -91.74], L[link_7]], " +
        "J[R, color[Blue], P[38.0, -7.8], L[ground, link_9, link_11]], " +
        "J[R, color[Green], P[56.28, 29.46], L[link_8, link_9]], " +
        "J[R, color[Green], P[75.07, -23.09], L[link_9, link_12]], " +
        "J[R, color[Green], P[31.18, -46.5], L[link_10, link_11, link_13]], " +
        "J[R, color[Green], P[64.84, -61.13], L[link_12, link_13]], " +
        "J[R, color[Green], P[4.79, -87.79], L[link_13]]" +
        "]",
    
    "Arm": "M[J[R, color[Green], P[-34.25, -20.625], L[ground, link_1, link_2]], J[R, color[Green], P[29.75, 77.375], L[link_2, link_5, link_6]], J[R, color[Green], P[-54.0, 10.875], L[link_1, link_3]], J[R, color[Green], P[-86.25, -3.125], L[ground, link_4]], J[R, color[Green], P[-7.25, 94.625], L[link_4, link_5]], J[R, color[Green], P[57.0, 110.875], L[link_5, link_8]], J[R, color[Green], P[126.5, 56.125], L[link_7, link_8]], J[R, color[Green], P[114.5, 35.625], L[link_6, link_7]], J[R, color[Green], P[7.0, 131.125], L[link_3, link_6]], J[R, color[Green], P[163.5, 47.875], L[link_7]]]",
    
    #"": "",
}
