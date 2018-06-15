# m119
### Hexiwear
[Link to Hexiwear code](https://os.mbed.com/users/adrayv/code/Hexi_Final_Project/file/8a9b0eb4835d/main.cpp/)

Binary File for Hexiwear is called:
`Hexi_Final_Project_HEXIWEAR.bin`
___

### Pi to AWS Comm's
Download AWS IoT Core Python Development kit via https://github.com/aws/aws-iot-device-sdk-python
NOTE: DO NOT DO PIP INSTALL METHOD; instead, follow directions from "build from source" on site above. 
installing from PIP yields errors because Pip install is unstable.

if boto3 isn't installed, run "sudo python -m install boto3"
cd m119/basicPubSub

Type command below in Terminal to run Cognito script to push data from Pi to Python:
python basicPubSub_CognitoSTS.py -e a2w3x76c5t3np8.iot.us-west-2.amazonaws.com -r root-CA.crt -C us-west-2:1e1899db-7186-4aa1-9fd5-aa74e4792abb -id ECEM119Pi -t ECEM119 
