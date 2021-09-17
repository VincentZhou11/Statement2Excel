# How to use:
The program will ask for 2 prompts at first
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
Here, input the row number. You should set the row number to the first row in your table and, later, use the fill handle to automatically fill the converted formulas to rest of the column.
##Main Prompt
~~~
Input statement:
~~~
Here, input the statements. The program will only recognize these symbols:```∧ ∨ → ↔ ⊕ ¬```. Only enter one statement at a time. This prompt is in an infinite loop and can only be terminated manually.
# Requirements:
Python 3+ Environment. No additional packages required.
