# pgascraper

Setup
=========
pip install -r requirements.txt

Usage
================


Structures
==========
Tournament  
	- name: str  
	- par: str  
	- current_round: int  
	- is_started: bool  
	- is_finished: bool  
	- round_state: str  
	- cut_line: int (converted from str)  
	- players: dict of Golfers  
  
Golfer
======
	- status: str  
	- current_round: int  
	- thru: TBD ('None' until tournament starts)  
	- today: TBD ('None' until tournament starts)  
	- total:  int  
	- total_strokes: TBD ('None' until tournamnet starts)
	- rounds: list of Rounds  

Round
=====
	- strokes: TBD ('None' until tournament starts)
	- to_par: yet to be defined
	- tee_time: str  


A Sub-Section
-------------

<here is a subsection>
Numbered list:
1. hello
2. goodbye

