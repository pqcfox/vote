Vote
====
Vote is a voting system that relies on the versatility and speed of [SurveyMonkey](https://www.surveymonkey.com) to get instant voting results. Combined with the vast number of algorithms contained in [python-vote-core](https://github.com/bradbeattie/python-vote-core), Vote has the capability to meet all of your tallying needs - *without* long periods of manual labor.

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

* Extensive algorithm base from [python-vote-core](https://github.com/bradbeattie/python-vote-core)
* Immediate results with brilliantly fast [SurveyMonkey API](https://developer.surveymonkey.com/)
* Growing range of useful analytics, such as voter's second preferences
* Clean, easy-to-understand (and modify) code base

Installation
------------
  
First, [obtain a SurveyMonkey API key and access token](https://developer.surveymonkey.com/mashery/guide_oauth). Then:

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

Verbose mode will give you additional analytics (not just the victor).
