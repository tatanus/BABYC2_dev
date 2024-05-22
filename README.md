       ___      ___      ___    __   __    ___      ___                 _                     
      | _ )    /   \    | _ )   \ \ / /   / __|    |_  )     ___     __| |     ___     __ __  
      | _ \    | - |    | _ \    \ V /   | (__      / /     |___|   / _` |    / -_)    \ V /  
      |___/    |_|_|    |___/    _|_|_    \___|    /___|    _____   \__,_|    \___|    _\_/_  
    _|"""""| _|"""""| _|"""""| _| """ | _|"""""| _|"""""| _|     | _|"""""| _|"""""| _|"""""| 
    "`-0-0-' "`-0-0-' "`-0-0-' "`-0-0-' "`-0-0-' "`-0-0-' "`-0-0-' "`-0-0-' "`-0-0-' "`-0-0-' 


Written by - Adam Compton ([@tatanus](https://twitter.com/tatanus))

Requirements:
- Python 3.x (probably 3.10+)

Links:
 - Blog Post regarding BabyC2 can be found here: XXX
 - Video of a conference talk regarding BabyC2 can be found here: XXX
 - Code for "combined" C2 and protocols can be found here: XXX

Summary:
Baby C2 is a simple C2 written in Python. It is not intended to be used in a production environment.
It is intended to be used as a learning tool for those interested in learning about C2s.

This is the development version.

Provided here are various iterations of the code stepping through some of the different communication protcols.
|  |  |
| ------ | ----------- |
| 0_TCP_BASIC | This is a basic TCP listener accepting connections from netcat or similar tools. |
| 1_TCP_AGENT | This is a TCP listener and agent pair demonstrating a basic C2 with a deployable agent. |
| 2a_TCP_ENCRYPTED | This is a TCP listener and agent pair demonstrating a basic C2 with a deployable agent that uses a custom encryption scheme. |
| 2b_TCP_SSL | This is a TCP listener and agent pair demonstrating a basic C2 with a deployable agent that uses SSL for encryption. |
| 3_HTTP(s) | This is a HTTP listener and agent pair demonstrating a basic C2 with a deployable agent. |
| 4_SSH | This is a SSH listener and agent pair demonstrating a basic C2 with a deployable agent. |
| 5_TCP_More_Functionality | This is the same as 0_TCP or 1_TCP_AGENT but has additional sctructure and capabilities built in. |

Current Agent Capabilities include:
 - Upload – Upload a file to the system
 - Download – Download a file from the system
 - Back – Background the current agent
 - Kill – Kill the current agent
 
Future work:
 - Better encryption
 - Add more agents (js, c, c++, c#, hta, ps1, etc.)
 - load/execute Powershell scripts from attacker machine
 - .NET(CSharp) loader
 - AV evasion
 - socks proxy
 - peer-to-peer
 - Load/Run BOFs
 - Add Jitter/sleep to the agents

**Special thanks:**
 - Kevin CLark ([@GuhnooPlusLinux](https://twitter.com/GuhnooPlusLinux))