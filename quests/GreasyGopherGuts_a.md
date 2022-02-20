Grep can be used to look for certain keywords/lines inside a file. The man page shows which parameters are available. The later steps are easier to solve if you're using regular expressions and/or piping a command output to another command.   
The quizme binary offers some help to get the proper grep statements:

``` bash
# What port does 34.76.1.22 have open?
elf@372b805671ad:~$ grep 34.76.1.22 bigscan.gnmap 
Host: 34.76.1.22 ()     Status: Up
Host: 34.76.1.22 ()     Ports: 62078/open/tcp//iphone-sync///      Ignored State: closed (999)

# What port does 34.77.207.226 have open?
elf@372b805671ad:~$ grep 34.77.207.226 bigscan.gnmap 
Host: 34.77.207.226 ()     Status: Up
Host: 34.77.207.226 ()     Ports: 8080/open/tcp//http-proxy///      Ignored State: filtered (999)

# How many hosts appear "Up" in the scan?
elf@372b805671ad:~$ grep "Status: Up" bigscan.gnmap | wc
  26054  130270  967583

# How many hosts have a web port open?  (Let's just use TCP ports 80, 443, and 8080)
elf@b603d20214a1:~$ grep -E "(80/open)|(443/open)|(8080/open)" bigscan.gnmap | wc
  14372  180190 2539348

# How many hosts with status Up have no (detected) open TCP ports?
elf@b603d20214a1:~$ grep "Status: Up" bigscan.gnmap | wc ; grep "/open" bigscan.gnmap | wc
  26054  130270  967583
  25652  321396 4731570
# 26054 - 25652 = 402

# What's the greatest number of TCP ports any one host has open?
elf@9bb355913c98:~$ cat bigscan.gnmap | grep "/open" | awk -F',' '{print NF-1}' | sort | uniq
0
1
10
11
2
..
9
# Max is 11(+1) = 12
```