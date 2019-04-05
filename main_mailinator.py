from pymailinator import wrapper
api_key = "723e0d4493234625b1cb59ca6dea2e1f"
inbox = wrapper.Inbox(api_key)

a = inbox.get("john")
print(a)



