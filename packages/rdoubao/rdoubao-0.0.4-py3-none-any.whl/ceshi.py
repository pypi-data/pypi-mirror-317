

# 豆包

def zcb():
    import winreg
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\FileSystem", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, "LongPathsEnabled", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(registry_key)
        print("LongPathsEnabled 已成功设置为 1")
    except PermissionError:
        print("拒绝访问：请以管理员身份运行此脚本。")
    except Exception as e:
        print(f"修改注册表时出错: {e}")
def pipanzhuang():
    print('pip install volcengine-python-sdk')


def doubao(content):
    from volcenginesdkarkruntime import Ark
    client = Ark(api_key="8da1eb82-6942-48ca-be1a-e037f2fece63")

    completion = client.chat.completions.create(
        model="ep-20241223232214-ttpt9",
        messages=[
            {"role": "user", "content": content},
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
