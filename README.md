# OpenTT
Open Test Taker - Interactive Python testing suite

###### Example usage:

- *No limit; -l N where N <= 0*
    - python main.py -f example.json [-l 0]

- *Limit; -l N where N > 0*
    - python main.py -f example.json -l 5

- *Random questions*
    - python main.py -f example.json -r

- *Shuffle answers*
    - python main.py -f example.json -s

- *Filter by chapter tag (subject to change; only if present)*
    - python main.py -f example.json -c 'value'

- *Filter by category tag (subject to change; only if present)*
    - python main.py -f example.json -g 'value'

- *Creating your own tests using the questions2json.py parser*
    - python questions2json.py -f <file> -t '<test_name>' -c '<chapter#>'

```python
###### Test Template
;questions
^\d+\s[ A-Za-z0-9_@.\/#&+-]*$ <-- marks question
^[A-Z]+\s[ A-Za-z0-9_@.\/#&+-?"\\$\\^]*$ <-- answer A
^[A-Z]+\s[ A-Za-z0-9_@.\/#&+-?"\\$\\^]*$
^[A-Z]+\s[ A-Za-z0-9_@.\/#&+-?"\\$\\^]*$
^[A-Z]+\s[ A-Za-z0-9_@.\/#&+-?"\\$\\^]*$ <-- answer B; repeat pattern of Q-A{n}
;answers
^[A-Z]+\s[A-Za-z]+\s[ A-Za-z0-9_@.\/#&+-?"\\$\\^]*$

Example:
;questions
1 What is 1+1?"
A 2
B 3
C 1
```
D 4
;answers
1 A
