kakaushka_themes
===================

The bot remembers the topics you want to discuss later. I created it for friends group chat. We store the topics in it and then discuss them live drinking chocolate (kakaushka) or at lunch.

## Example ##

`/touch Apple released Android compatibility layer for iPhone`

Bot answer:
`Theme №1 created`

`/touch NSA has been suspected of data capture by embedding hardware backdoor in wires`

Bot answer:
`Theme №2 created`

`/ls`

Bot answer:

`1. Apple released Android compatibility layer for iPhone (Firstname Lastname)`

`2. NSA has been suspected of data capture by embeding hardware backdoor in wires (Firstname Lastname)`


## How to run ##
- install requirements
- rename `example_config.py` to `config.py`
- place your token in `config.py`
- make sure MongoDB is running
- execute `bot.py`

To run tests, execute `python -m unittest discover`. They require MongoDB to be running.
