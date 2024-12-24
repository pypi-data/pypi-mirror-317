# mykurve library

Unofficial async library to retrieve details of https://api.mykurve.com/ or https://www.mykurve.com/ account
This was done for personal project but feel free to use on your own risk 

Hope will be useful to someone and if there is any issues (what I think there is...) please open PR or issue will 
try to help/fix in mean time

## Note
- This will work only if you don't have 2FA enabled (2FA is still **NOT** supported)

### TODO:
- handle 2FA 

### How to use 

```python
import asyncio

from mykurve import MyKurveApi
from mykurve.data_classes import TimeRange

userName = "<your_account>"
password = "your_password"

async def main():
    api = MyKurveApi()

    token = await api.get_token(userName, password)
    print(token)

    account = await api.get_accounts(token.access_token)
    print(account)

    account_info = await api.get_account_info(token.access_token, account.accounts[0].accountNumber)
    print(account_info)

    dashboard = await api.get_dashboard(token.access_token, account.accounts[0].accountNumber)
    print(dashboard)

    dashboard = await api.get_consumption_graph(token.access_token, account.accounts[0].accountNumber, TimeRange.DAY, 0)
    print(dashboard)


if __name__ == "__main__":
    asyncio.run(main())
```

If you like what I'm doing please support me <br/>
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/ddb0515)