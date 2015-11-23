# Project Gamma 
A Basic Simulated Trading Platform

Current State:
  - There is a basic/generic terminal that pulls realtime data from the yahoo_finance module. The available data can be found by
  calling the programs help function which will return a list of recognized functions and their result.
  - Terminal allows for basic portfolio logging, but lacks robustness and ease of access to data
  - Functionality is split between main.py/attributes.py and Process.py/Data.py
  - Process/Data files are where development is focused. Currently stable and functional, lacks front end interface that main.py supplies
  - Finaled development of backend Data IO with re-written functionality to better store data and facilitate ease of access to portfolio data.Stores quantity and real time liquid value of shares.

Next Update:
  - Develop front end for Process.py and Data.py files. Will offer a text based UI to track investments.  

Future:
  - After creating a responsive and functioning platform that can process changes in a Portfolio, will develop a stock recommendationg algorithm that compares weighted data from other portfolios.

This a simple, simulated stock trading platform built from the ground up using IPython, myplotlib, and yahoo_finance.
