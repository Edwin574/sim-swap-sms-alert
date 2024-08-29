# sim-swap-sms-alert


### Description
This simple code helps you send an SMS using `cradlevoices.com` API to alert the user if the sim has been swapped.The SMS should give the customer the next course of actions.

#### The Endpoint

1. **/send_sms**: sends an sms using cradleVoices Api.

        - Token:generated from cradle voices API
        - message: The message you want to send based on the status
        - phone: The number you want to send the api to

2. **/listen_url**: gets the listen_url from Africa's talking Insights API respone and also the phone number that an sms is sent to.

        - listen_url: gotten from the Insights API that enable you to check for swapping status of a particular phone number. Remember this url maps a particuler transaction id for the first request you make to get the listen Url. 
        - phone: the particular phone number to notify.


### References

1. [SimSwap API](https://developers.africastalking.com/docs/insights/simswap)
2. [CradleVoices](https://cradlevoices.com/)


Your .env file should have:

 - API_TOKEN: from cradlevoices
 - SMS_API_ENDPOINT = "https://merchant.cradlevoices.com/"
