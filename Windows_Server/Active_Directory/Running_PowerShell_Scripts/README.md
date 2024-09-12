# Running PowerShell scripts
## Set execution-policy

By default there is a security feature that doesn't allow Windows to run PS scripts, in order to be able to run our scripts we have to change the execution policy.
First we open Windows PowerShell Integrated Scripting Environment (ISE) as Administrator from the start menu. PowerShell ISE lets developers run PowerShell commands and create, test and refine PowerShell scripts without operating directly in the traditional PowerShell command-line interface.

![PS ISE](Screenshots/PS_ISE.png)

From the PS ISE we can change th execution policy with the command **set execution-policy unrestricted**, we are using unrestricted in this case because it's a lab environment but in real world scenarios it is best to set the execution policy to **RemoteSigned**, so that 
locally created scripts can be run without a digital signature while any scripts downloaded from the internet are required to be signed by a trusted publisher.
 
![PS ExecutionPolicy](Screenshots/PS_executionPolicy.png)

## Analyzing the script

Now that we can run our script, I will use as an example a script that allows us to generate 1000 users (with respective first, last name and password), automating the process instead of doing it manually.

![PS script](Screenshots/PS_script.png)

The first thing to do is define our variables: <br>
- **$PASSWORD_FOR_USERS = "Password1"** 
    - will be the password for each account <br>
- **$USER_FIRST_LAST_LIST = Get-Content .\names.txt**
    - takes all the names from the ![names.txt](PS_script/names.txt) and stores them inside the variable as an array.

- **$password = ConvertTo-SecureString $PASSWORD_FOR_USERS -AsPlainText -Force** 
    - takes the plain text we stored in $PASSWORD_FOR_USERS (Password1) and turns it into an object that powershell can use as a secure password (it will be used when we will create the users in AD). <br>
- **New_ADOrganizationalUnit -Name _USERS -ProtectedFromAccidentalDeletion $false** 
    - creates the OU called _USERS <br>
- **foreach ($n in $USER_FIRST_LAST_LIST) {...}** 
    - is a for loop that takes every element in the $USER_FIRST_LAST_LIST and runs the whole block of code for each individual user in this list <br>
- **$first = $n.Split(" ")[0].ToLower()** and **$last = $n.Split(" ")[1].ToLower()** 
    - are going to respectively split the name at the space (" ") dividing the first from last name and storing both in a variable (first at index [0] and last at index[1]) <br>
- **$username = "$($first.Substring(0,1))$($last)".ToLower()** 
    - creates a username by taking the first character from $first and the whole $last name (for example if the name is "Vito Faretina", the username will be "vfaretina") <br>
- **Write-Host "Creating user: $($username)" -BackgroundColor Black -ForegroundColor Cyan** 
    - outputs to the terminal that it's creating the username <br>
- **New-AdUser** 
    - creates a user and stores it in the _USERS OU in Active Directory, the rest of the command are the parameters for the user: 
	
	**-AccountPassword $password** <br> 
	- gives the user the password stored in $password (which is the "Password1" we initially stored in $PASSWORD_FOR_USERS)
    
    **-GivenName $first** <br> 
	- sets the first name of the user 
	
	**-Surname $last** <br> 
	- sets the last name
	
	**-DisplayName $username**, **-Name $username**, **-EmployeeID $username** <br>
	- are all going to use the username defined in $username
	
    **- PasswordNeverExpires $true** <br>
	- (not recommended in real world scenarios) sets the password to never expire
	
	**-Path "ou=_USERS,$(([ADSI]"").distinguishedName)"** <br>
	- tells the script to store this user in the _USERS OU
	
	**-Enabled $true** <br> 
	- activates the user account 

## Running the script

Once the script is set, in order to run it it is best if we enter the folder where the script is located, in this case my script is in a folder on the Desktop. <br>
To access the script for powershell run **cd path\to\directory**, in this case **cd C:\Users\a-vfaretina\Desktop\AD_PS-master**

![PS cd directory](Screenshots/PS_cd_directory.png)

To run the script simply type the name of the script with its full path, in this case **C:\Users\a-vfaretina\Desktop\AD_PS-master\1_CREATE_USERS.ps1**. <br>
Once the script starts it will display the various users it's creating.

![PS run script](Screenshots/PS_run_script.png) 

If we open the Active Directory Users and Computer windows we can see that the **_USERS** OU has been created and it's populated with all the users we created with the script.

![PS users](Screenshots/PS_users.png)
