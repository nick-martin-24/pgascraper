# pgascraper

Setup
=========
pip install -r requirements.txt

Usage
================


Structures
==========
Tournament  
	- par:  
	- current_round: str  
	- tournament_name: str  
	- is_started: str  
	- is_finished: str  
	- round_state: str  
	- cut_line: int (converted from str)  
	- players: dict of Golfers  
  
Golfer
======
	- name: str  
	- status: str  
	- thru: str  
	- current_round: str  
	- today:  
	- total:  
	- total_strokes:  
	- rounds: list of Rounds  

Round
=====
	- strokes
	- to_par
	- tee_time


A Sub-Section
-------------

<here is a subsection>
Numbered list:
1. hello
2. goodbye

