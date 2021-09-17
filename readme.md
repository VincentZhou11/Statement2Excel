# Attribution
Thanks to Tomek Korbak for his Shunting-yard implementation for order of operations
 
https://tomekkorbak.com/2020/03/25/implementing-shunting-yard-parsing/
# How to use:

There are two programs: ```basic_conversion.py``` and ```shunting_yard_modified.py```. ```shunting_yard_modified.py``` is preferred over ```basic_conversion.py``` because ```shunting_yard_modified.py``` uses a modified Djikstra's Shunting-yard algorithim while ```basic_conversion.py``` is a naive algorithim that I made up. ```shunting_yard_modified.py``` should be more robust and respect order of precedence for logical operators, according to [Wikipedia](https://en.wikipedia.org/wiki/Logical_connective#Order_of_precedence).

The program will ask for 2 prompts at first.
##1st Prompt
~~~
Column mapping:
~~~
Here, input a JSON object string. This will act like a  dictionary that maps boolean names to column letters. The key is the name of the boolean and the value is the column letter (Do not include row number). Do not include newlines. This is case-sensitive.
```
{"boolean_name":"column_letter", "boolean_name2":"column_letter2, ...}
```
##2nd Prompt
~~~
Input row #:
~~~
Here, input the row number. You should set the row number to the first row in your table. In Excel/Google Sheets (or whatever spreadsheet program), use the fill handle to automatically fill the formulas to rest of the column.
##Main Prompt
~~~
Input statement:
~~~
Here, input the statements. The program will only recognize these symbols:```∧ ∨ → ↔ ⊕ ¬```. Parenthesis are allowed. Only enter one statement at a time. This prompt is in an infinite loop and can only be terminated by typing ```x```. The ```basic_conversion.py``` program doesn't follow order of precedence for logical operators and assumes left to right precedence without parenthesis. The ```shunting_yard_modified.py``` program will follow the order of precedence according to [Wikipedia](https://en.wikipedia.org/wiki/Logical_connective#Order_of_precedence).
# Requirements:
Python 3+ Environment. No additional packages required.
