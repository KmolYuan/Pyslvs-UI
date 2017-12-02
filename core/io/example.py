# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

#TODO: Add examples as expression.

example_list = {
    "Crank rocker":"M[J[R, color[Green], P[0.0, 0.0], L[ground, link_0]], J[R, color[Green], P[12.92, 32.53], L[link_0, link_1]], J[R, color[Green], P[73.28, 67.97], L[link_1, link_2]], J[R, color[Green], P[33.3, 66.95], L[link_1]], J[R, color[Green], P[90.0, 0.0], L[ground, link_2]]]",
    "Jansen's linkage (Single)":"M[J[R, color[Green], P[0.0, 0.0], L[ground, link_0]], J[R, color[Green], P[9.61, 11.52], L[link_0, link_1, link_3]], J[R, color[Blue], P[-38.0, -7.8], L[ground, link_2, link_4]], J[R, color[Green], P[-35.24, 33.61], L[link_1, link_2]], J[R, color[Green], P[-77.75, -2.54], L[link_2, link_5]], J[R, color[Green], P[-20.1, -42.79], L[link_3, link_4, link_6]], J[R, color[Green], P[-56.05, -35.42], L[link_5, link_6]], J[R, color[Green], P[-22.22, -91.74], L[link_6]]]",
    "Jansen's linkage (Double)":"M[J[R, color[Green], P[0.0, 0.0], L[ground, link_0]], J[R, color[Green], P[9.61, 11.52], L[link_0, link_1, link_3, link_7, link_9]], J[R, color[Blue], P[-38.0, -7.8], L[ground, link_2, link_4]], J[R, color[Green], P[-35.24, 33.61], L[link_1, link_2]], J[R, color[Green], P[-77.75, -2.54], L[link_2, link_5]], J[R, color[Green], P[-20.1, -42.79], L[link_3, link_4, link_6]], J[R, color[Green], P[-56.05, -35.42], L[link_5, link_6]], J[R, color[Green], P[-22.22, -91.74], L[link_6]], J[R, color[Blue], P[38.0, -7.8], L[ground, link_8, link_10]], J[R, color[Green], P[56.28, 29.46], L[link_7, link_8]], J[R, color[Green], P[75.07, -23.09], L[link_8, link_11]], J[R, color[Green], P[31.18, -46.5], L[link_9, link_10, link_12]], J[R, color[Green], P[64.84, -61.13], L[link_11, link_12]], J[R, color[Green], P[4.79, -87.79], L[link_12]]]",
    "Crank slider":"M[J[R, color[Green], P[-26.625, 46.125], L[link_0, link_1]], J[RP, A[10.0], color[Green], P[0.0, 0.0], L[ground, link_0]], J[R, color[Green], P[-49.625, 4.125], L[ground, link_1]]]",
    #"":"",
}
