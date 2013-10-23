# Python Does Countdown

Quoth [Wikipedia](https://en.wikipedia.org/wiki/Countdown_%28game_show%29):

> Countdown is a British game show involving word and number puzzles.
>
> The two contestants in each episode compete in three disciplines: eleven
> letters rounds, in which the contestants attempt to make the longest word
> possible from nine randomly chosen letters; three numbers rounds, in which
> the contestants must use arithmetic to reach a random target number from
> six other numbers; and the conundrum, a buzzer round in which the
> contestants compete to solve a nine-letter anagram.

I was watching the show and decided that it'd be easy for a computer to win it.

## Installing and Running

This project uses the [signal](http://docs.python.org/2/library/signal.html) Python library in a way that's incompatiable with Windows.  So, this only works on Unix machines.

You'll also need a dictionary file: a text file with one word per line.  The script will check for [`/usr/share/dict/words`](https://en.wikipedia.org/wiki/Words_%28Unix%29) by default, but if that file is not found, it will prompt for the path to your specific dictionary.  The included `conundrums.pickle` file was generated using my local `/usr/share/dict/words`; if you'd like to regenerate the conundrum puzzles, simply delete the Pickle file before running the scipt.

Other than that, the project is nothing particularly fancy.  Running the module will just kick off a random simulation of a game of *Countdown* that the computer will play against itself.  On my machine:

```
$ python --version
Python 2.7.3
$ git clone https://github.com/ajvondrak/countdown.git countdown
$ python -m countdown
```
