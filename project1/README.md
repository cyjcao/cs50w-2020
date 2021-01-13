# Wiki

Design a Wikipedia-like online encyclopedia.
The project requirements can be found [here](https://cs50.harvard.edu/web/2020/projects/1/wiki/#:~:text=Entry%20Page:%20Visiting%20/wiki/TITLE,%20where%20TITLE%20is%20the%20title%20of%20an%20encyclopedia%20entry,%20should%20render%20a%20page%20that%20displays%20the%20contents%20of%20that%20encyclopedia%20entry.The%20view%20should%20get%20the%20content%20of%20the%20encyclopedia%20entry%20by%20calling%20the%20appropriate%20util%20function.If%20an%20entry%20is%20requested%20that%20does%20not%20exist,%20the%20user%20should%20be%20presented%20with%20an%20error%20page%20indicating%20that%20their%20requested%20page%20was%20not%20found.If%20the%20entry%20does%20exist,%20the%20user%20should%20be%20presented%20with%20a%20page%20that%20displays%20the%20content%20of%20the%20entry.%20The%20title%20of%20the%20page%20should%20include%20the%20name%20of%20the%20entry.Index%20Page:%20Update%20index.html%20such%20that,%20instead%20of%20merely%20listing%20the%20names%20of%20all%20pages%20in%20the%20encyclopedia,%20user%20can%20click%20on%20any%20entry%20name%20to%20be%20taken%20directly%20to%20that%20entry%20page.).
<br/>

To run this project on your local machine, first clone this repository into your machine.
<br/>
1. Install Django and [python-markdown2](https://github.com/trentm/python-markdown2):
```console
foo@my-machine:~$ pip install django markdown2
```
2. Change to project1 directory and start the Django development server:
```console
foo@my-machine:~/cs50w-2020$ cd project1/
foo@my-machine:~/cs50w-2020/project1$ python manage.py runserver
```
3. Open the host address in your browser, usually it will be 127.0.0.1:8000/ or localhost:8000/

<hr/>
