Vote
====
Vote is a voting system that relies on the versatility and speed of SurveyMonkey to get instant voting results. Combined with the vast number of algorithms contained in py-vote-core, Vote has the capability to meet all of your tallying needs - *without* long periods of manual labor.

```sh
$ vote.py -v
Elected candidate: Candidate A
Second choice support:
Candidate B: 13/26
Candidate C: 32/63
Candidate D: 56/67
```

Features
--------

* Wide algorithm base (relies on py-vote-core)
* Immediate results (brilliantly fast SurveyMonkey API)
* Growing range of useful analytics, such as second preferences
* Clean, easy-to-understand (and modify) code base

Installation
------------
  
First, obtain a SurveyMonkey API key and access token. Then:

```sh
git clone https://github.com/useanalias/vote
cd vote
mv config.ini.example config.ini
vim config.ini   # enter API key and access token
```
  
Usage
-----
It's as simple as it gets:

```sh
./vote.py (-v)
```

Verbose mode will give you additional analytics beyond the victor.
