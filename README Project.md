# Project README for CS340
**Author:** Arys Pena <br>
**Date:** 2021/08/23 <br>

###  How do you write programs that are maintainable, readable, and adaptable? Especially consider your work on the CRUD Python module from Project One, which you used to connect the dashboard widgets to the database in Project Two. What were the advantages of working in this way? How else could you use this CRUD Python module in the future?
Writing re-useable code is a key component of becoming a good software developer. Code that is easily generalizable should be made into a function with input parameters that can be used to make its output different. Using clear comments and docstrings makes your code readable and more maintainable for future developers. Using type hints makes the variables more understandable and maintainable as well. Clear and concise, yet descriptive variables names also makes the code more maintainable and easier to adapt in the future.

The Python CRUD module could easily be used for additional databases in the future by adjusting the __init__ function to not have a hard coded database connection string. By alternating that, it could connect to different databases and then read, write, update, and delete on different datasets.


### How do you approach a problem as a computer scientist? Consider how you approached the database or dashboard requirements that Grazioso Salvare requested. How did your approach to this project differ from previous assignments in other courses? What techniques or strategies would you use in the future to create databases to meet other client requests?
Each problem has it’s own unique set of factors that must be analyzed and accounted for. There is a wealth of knowledge and answers available for all to read, but to find these answers, first the problem must be identified. Once identified, the problem can be analyzed and broken down into smaller problems to tackle. This modular approach, combined with an iterative nature can tackle even the biggest problems. In the Grazioso Salvare project, I started by identifying the base requirements and decided on a set of ways to display the data. The widgets I chose were a data table, bar chart, and geo map. These three components allow the user to view the data in different ways. In the future, I would reuse the Mongo CRUD code for creating, connecting, and interacting with future databases.


### What do computer scientists do, and why does it matter? How would your work on this type of project help a company, like Grazioso Salvare, to do their work better?
Generally speaking, computer scientists analyze and develop solutions involving both computer hardware and software. Client and server development is something that can help improve the efficiency, safety, and reliability of many companies. Designing, implementing, maintaining, and analyzing these types of systems are all problems that a computer scientist may be able to help with. A skilled computer scientist can help to enhance the process in which a company operates.
