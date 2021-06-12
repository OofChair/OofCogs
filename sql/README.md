# SQL

## This cog requires a little setup. 

### Installation

#### Install for Linux:

```bash
sudo apt-get install mysql-client mysql-server
mysql
mysql> CREATE USER 'yourusernamehere'@'localhost' IDENTIFIED BY 'yourpasswordhere';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'oee'@'localhost';
mysql> exit
```
##### After you finish installing, check [Setup the cog](./README.md#setup-the-cog) to learn how to setup this cog.

#### Install for Windows:

Install MySQL from [here](https://dev.mysql.com/downloads/installer/) and run the EXE.<br>
When the installer launches, you should see this:
![Home page of MySQL](https://pays.host/uploads/60eea31d-e3b8-4226-afed-de21458e50b4/CQjOSAHc.png)<br>
Select "Server only" and click next. After you click Next, you should see this: ![Installation page of MySQL](https://pays.host/uploads/60eea31d-e3b8-4226-afed-de21458e50b4/aec5MSu3.png)<br>Click "Execute" and let it install. Once it finishes, click Next. After you click Next, you should see a page that looks like this:<br>![Config](https://pays.host/uploads/60eea31d-e3b8-4226-afed-de21458e50b4/h2gsSitE.png)<br>Click Next. On the "Type and Networking" page, just click Next to keep the default settings. After you click Next, you should see this:<br>![Authentication](https://pays.host/uploads/60eea31d-e3b8-4226-afed-de21458e50b4/WYgMiLzN.png)<br>If it's not already set as "Use Strong Password Encryption for Authentication", set it to that. Click Next.<br>![](https://pays.host/uploads/60eea31d-e3b8-4226-afed-de21458e50b4/nMYFvZPg.png)<br>Set the root password, and then create a new user. Click Add User, and you should see this: ![](https://pays.host/uploads/60eea31d-e3b8-4226-afed-de21458e50b4/MHVW5aAg.png)<br>Set your username and password here. This will be used for MySQL credentials for the cog. After you add the username and password, click OK. The page should look similar to this: ![](https://pays.host/uploads/60eea31d-e3b8-4226-afed-de21458e50b4/WCCUsIyR.png)<br>If it does, the user has been created. If not, create the user again. Once the user has been created, click Next. On the Windows Service screen, keep the defaults and click Next. After that, you should see a page like this: ![](https://pays.host/uploads/60eea31d-e3b8-4226-afed-de21458e50b4/NWtnGAsw.png)<br>Click Execute to set up MySQL with your user and the settings you selected earlier. Once there are green checks next to all the steps, click Finish. You should see this after: ![](https://pays.host/uploads/60eea31d-e3b8-4226-afed-de21458e50b4/AxYTAgFG.png)<br>Click Finish, and now you can [setup the cog](./README.md#setup-the-cog)

#### Setup the cog

Once you install the SQL cog, you need to add your MySQL credentials. 
(In this example, [p] is your prefix)
```ini
[p]set api mysql username,yourusernamehere password,yourpasswordhere
[p] load sql
```

# SQL Changelog

## v1.0.4

#### Update directions so all databases can be viewed

## v1.0.3

#### Highlight setup in install_msg

## v1.0.2

#### Release the cog :D

## v1.0.1

#### Get SQL cog ready for review on PR 

## v1.0.0

#### Beginning commit, interact with MySQL