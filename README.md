# scrapeutils

Setup
=========
pip install -r requirements.txt

Usage
================


Structures
==========
Tournament
----------  
	- name: str  
	- setup_year: str
	- actual_year: int
	- par: int  
	- current_round: int  
	- is_started: bool  
	- is_finished: bool  
	- round_state: str  
	- cut_line: int (converted from str)  
	- penalty: int (initialized to None)  
	- players: dict of Golfers  
  
Golfer
------
	- status: str  
	- current_round: int  
	- thru: TBD ('None' until tournament starts)  
	- today: str ('None' until tournament starts)  
	- total: int  
	- total_strokes: TBD ('None' until tournamnet starts)
	- rounds: list of Rounds  

Round
-----
	- strokes: TBD ('None' until tournament starts)
	- to_par: yet to be defined
	- tee_time: str  

