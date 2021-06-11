# SQL

## This cog requires a little setup. 

### Installation

#### Install for Linux:

```bash
sudo apt-get install mysql-client mysql-server
mysql
mysql> CREATE USER 'yourusernamehere'@'localhost' IDENTIFIED BY 'yourpasswordhere';
mysql> exit
```

#### Install for Windows:

Install MySQL from [here](https://dev.mysql.com/downloads/installer/) and run the EXE.
When asked to select the packages to install, select MySQL Server and MySQL Shell.
On package setup, set up a user and password. This is how you will use the MySQL commands inside the bot.

#### Setup the cog

Once you install the SQL cog, you need to add your MySQL credentials. 
(In this example, [p] is your prefix)
```ini
[p]set api mysql username,yourusernamehere password,yourpasswordhere
[p] load sql
```

# SQL Changelog

## v1.0.0

#### Beginning commit, interact with