import sys
import subprocess 
import time

def callTrace(serverName,max_hops = 30):

        hops = subprocess.run(
        ['traceroute','-m', str(max_hops), serverName],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True)
    #wait for 20 seconds
        time.sleep(20)
        host_unreachable = False
        #print(hops.stdout)
        output_lines = hops.stdout.splitlines()
        unique_hops = set()
    #check output lines 
        for line in output_lines:
            cleaned_line = line.strip()

            if cleaned_line and cleaned_line[0].isdigit():
            # Extract the hop number (the first part of the line)
                hop_number = cleaned_line.split()[0]  # Get the hop number as a string
                
                if hop_number.isdigit():
                    unique_hops.add(hop_number)  # Add the hop number directly to the set


        if output_lines:
            last_line = output_lines[-1].strip()
            if '* * *' in last_line:
                sys.stdout.write("Traceroute: failed ")
            else:
                 sys.stdout.write(f"{len(unique_hops)} hops to {serverName}\n")
            
            

            
def main():
    serverName = input("Enter a server name: \n")
    callTrace(serverName)

if __name__ == "__main__":
    main()
