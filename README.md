# Multi Thread Port Scanner
![alt text](https://raw.githubusercontent.com/kleosdc/mt-port-scanner/main/latest-1.0.1.PNG)
## Required modules
```python
pip install clipboard
pip install colorama
```
## Usage
```python
python imscan.py
```
* Copy the desired IP Address for scan before running the script.  
* The script has a simple IP checker that validates the IP Address provided.
  
* The script works in the following way:  
  
 Once ran it gets the text of your clipboard because it is assuming that you already copied the desired IP Address for the scannable machine.  
   
 If the clipboard contains an IP Address it will display the address and ask the user whether they want to check the IP Address or continue to scan. 
   
 It defaults to 'No Change' for faster experience.  
   
 You can now user -y to specify that you want to skip the part where you decide whether you want to change the IP Address of the machine that you are trying to scan.
   
 You can now user -P10000 to specify the range of ports you wish to scan.
